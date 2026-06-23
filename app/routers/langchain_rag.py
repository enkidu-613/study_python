"""
LangChain RAG 路由：纯 LangChain 原生实现

接口对照：
| 手搓版接口                    | 本文件 LangChain 实现           |
|------------------------------|-------------------------------|
| POST /rag/documents          | POST /langchain-rag/documents |
| POST /rag/search             | POST /langchain-rag/search    |
| POST /rag/chat               | POST /langchain-rag/chat      |
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import AsyncIterator
import json
import os

from dotenv import load_dotenv

from app.embedding import get_langchain_embeddings
from langchain_deepseek import ChatDeepSeek
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document as LCDocument

from langchain_core.messages import AIMessageChunk
from langchain_text_splitters import RecursiveCharacterTextSplitter

import chromadb

import tiktoken

from app.database import get_db
from app.models import Document, DocumentChunk

load_dotenv()

MODELSCOPE_BASE_URL = os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1")
MODELSCOPE_API_KEY = os.getenv("MODELSCOPE_API_KEY")
LLM_MODEL = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL_NAME", "Qwen/Qwen3-Embedding-8B")

MAX_CONTEXT_TOKENS = 2000
MAX_INPUT_TOKENS = 6000
MAX_OUTPUT_TOKENS = 2000

llm = ChatDeepSeek(
    model=LLM_MODEL,
    api_base=MODELSCOPE_BASE_URL,
    api_key=MODELSCOPE_API_KEY,
    temperature=0.7,
    streaming=True,
    model_kwargs={"extra_body": {"thinking": {"type": "enabled"}}},
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

_vectorstore = None


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            client=chroma_client,
            collection_name="documents",
            embedding_function=get_langchain_embeddings(),
        )
    return _vectorstore

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
)


def estimate_tokens(text: str, model: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))


def format_docs(docs) -> str:
    formatted = []
    for i, doc in enumerate(docs, start=1):
        title = doc.metadata.get("title", "未命名")
        source = doc.metadata.get("source", "未知来源")
        formatted.append(f"[{i}] 来源：《{title}》（{source}）\n{doc.page_content}")
    return "\n\n".join(formatted)


def truncate_context(formatted_context: str, max_tokens: int = MAX_CONTEXT_TOKENS) -> str:
    if not formatted_context:
        return "没有检索到相关文档。"

    blocks = formatted_context.split("\n\n")
    result_blocks = []
    current_tokens = 0

    for block in blocks:
        block_tokens = estimate_tokens(block)
        if current_tokens + block_tokens > max_tokens:
            break
        result_blocks.append(block)
        current_tokens += block_tokens

    return "\n\n".join(result_blocks) if result_blocks else "没有检索到相关文档。"


def _save_document_to_sqlite(doc, db: Session) -> Document:
    document = Document(title=doc.title, content=doc.content, source=doc.source)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def _save_chunks_to_sqlite(chunks_with_ids: list[dict], db: Session):
    for c in chunks_with_ids:
        chunk = DocumentChunk(
            document_id=c["document_id"],
            chunk_index=c["chunk_index"],
            content=c["content"],
            embedding_id=c["embedding_id"],
        )
        db.add(chunk)
    db.commit()


def _find_document_or_404(doc_id: int, db: Session) -> Document:
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail=f"文档 ID={doc_id} 不存在")
    return document


def _delete_document_from_sqlite(document: Document, db: Session):
    db.delete(document)
    db.commit()


def _enrich_metadata_from_sqlite(doc: LCDocument, db: Session):
    doc_id = doc.metadata.get("document_id")
    if not doc_id:
        return

    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if db_doc:
        doc.metadata["title"] = db_doc.title
        doc.metadata["source"] = db_doc.source or "未知来源"


def _build_chroma_data(
    chunk_texts: list[str],
    document_id: int,
    title: str,
    source: str,
) -> tuple[list[LCDocument], list[str]]:
    lc_docs = []
    chroma_ids = []

    for i, chunk_text in enumerate(chunk_texts):
        lc_docs.append(LCDocument(
            page_content=chunk_text,
            metadata={
                "document_id": document_id,
                "chunk_index": i,
                "title": title,
                "source": source,
            }
        ))
        chroma_ids.append(f"doc{document_id}_chunk{i}")

    return lc_docs, chroma_ids


def _save_to_chromadb(lc_docs: list[LCDocument], chroma_ids: list[str]):
    try:
        get_vectorstore().add_documents(lc_docs, ids=chroma_ids)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ChromaDB 存储失败（ID 可能重复，请勿重复提交相同文档）: {str(e)}"
        )


def _search_vectorstore(query: str, k: int) -> list[tuple[LCDocument, float]]:
    return get_vectorstore().similarity_search_with_score(query, k=k)


def _delete_from_chromadb(document: Document):
    embedding_ids = [chunk.embedding_id for chunk in document.chunks]
    if embedding_ids:
        try:
            get_vectorstore().delete(ids=embedding_ids)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"ChromaDB 删除失败: {str(e)}"
            )
    return embedding_ids


def _prepare_chunks_for_storage(
    chunk_texts: list[str],
    document: Document,
    doc_in,
    db: Session,
):
    lc_docs, chroma_ids = _build_chroma_data(
        chunk_texts=chunk_texts,
        document_id=document.id,
        title=doc_in.title,
        source=doc_in.source,
    )

    sqlite_chunks = []
    for i, chunk_text in enumerate(chunk_texts):
        sqlite_chunks.append({
            "document_id": document.id,
            "chunk_index": i,
            "content": chunk_text,
            "embedding_id": chroma_ids[i],
        })

    _save_chunks_to_sqlite(sqlite_chunks, db)

    _save_to_chromadb(lc_docs, chroma_ids)


def _parse_search_results(
    results_with_scores: list[tuple[LCDocument, float]],
    db: Session,
) -> list[dict]:
    output = []
    for doc, distance in results_with_scores:
        metadata = doc.metadata
        doc_id = metadata.get("document_id")
        chunk_idx = metadata.get("chunk_index")
        similarity = round(1 - distance, 4)

        if doc_id is not None and chunk_idx is not None:
            db_doc = db.query(Document).filter(Document.id == doc_id).first()
            db_chunk = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == doc_id,
                DocumentChunk.chunk_index == chunk_idx,
            ).first()

            title = db_doc.title if db_doc else metadata.get("title", "未知")
            chunk_content = db_chunk.content if db_chunk else doc.page_content
        else:
            title = metadata.get("title", "未知")
            chunk_content = doc.page_content

        output.append({
            "title": title,
            "chunk_content": chunk_content,
            "similarity": similarity,
            "document_id": doc_id or 0,
            "chunk_index": chunk_idx or 0,
        })

    return output


def _retrieve_context(
    query: str,
    k: int,
    db: Session,
) -> tuple[list[LCDocument], str]:
    docs = get_vectorstore().similarity_search(query, k=k)

    for doc in docs:
        _enrich_metadata_from_sqlite(doc, db)

    context = format_docs(docs)
    context = truncate_context(context)

    return docs, context


def _build_sources_text(docs: list) -> str:
    sources = []
    for i, doc in enumerate(docs, start=1):
        title = doc.metadata.get("title", "未命名")
        source = doc.metadata.get("source", "未知来源")
        sources.append(f"[{i}] 《{title}》（{source}）")

    if sources:
        return "\n\n【参考来源】\n" + "\n".join(sources)
    return ""


def _build_rag_chain():
    return RAG_PROMPT | llm


def _yield_sse(event_type: str, content: str):
    data = {"type": event_type, "content": content}
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def _check_token_budget(context: str, question: str) -> str | None:
    total_input = estimate_tokens(context) + estimate_tokens(question)
    if total_input > MAX_INPUT_TOKENS:
        return "输入总 Token 数量超过最大限制，请减少检索结果数量或精简问题。"
    return None


async def _generate_stream(
    context: str,
    question: str,
    docs: list[LCDocument],
) -> AsyncIterator[str]:
    chain = _build_rag_chain()
    done_thinking = False

    try:
        async for chunk in chain.astream(
            {"context": context, "question": question},
            config={"max_tokens": MAX_OUTPUT_TOKENS}
        ):
            if isinstance(chunk, AIMessageChunk):
                reasoning = chunk.additional_kwargs.get("reasoning_content", "")
                answer = chunk.content

                if reasoning:
                    yield _yield_sse("thinking", reasoning)

                if answer:
                    if not done_thinking:
                        yield _yield_sse("divider", "\n\n === Final Answer ===\n")
                        done_thinking = True
                    yield _yield_sse("answer", answer)

        sources_text = _build_sources_text(docs)
        if sources_text:
            yield _yield_sse("sources", sources_text)

        yield _yield_sse("done", "")

    except Exception as e:
        yield _yield_sse("error", f"链执行出错: {str(e)}")


RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个基于知识库的问答助手。下面是从知识库中检索到的与用户问题相关的资料片段。

【资料片段】
{context}

【回答要求】
1. 请提取以上资料中与用户问题相关的信息，整理归纳后回答用户。
2. 不要编造资料中没有的信息，不要用你自己的知识补充。
3. 只有当资料片段为空（显示为"没有检索到相关文档"）时，才回答"根据现有资料无法回答该问题。"。否则，资料中无论信息多少，都应基于它们给出回答。"""),
    ("human", "{question}"),
])

router = APIRouter(prefix="/langchain-rag", tags=["LangChain RAG"])


class DocumentIn(BaseModel):
    title: str
    content: str
    source: str = ""


class SearchIn(BaseModel):
    query: str
    n_results: int = 3


class SearchResult(BaseModel):
    title: str
    chunk_content: str
    similarity: float
    document_id: int
    chunk_index: int


class ApiResponse(BaseModel):
    code: int = 200
    status: str = "success"
    content: dict | list | str | bool | int | float | None = None


class ChatRequest(BaseModel):
    query: str
    n_results: int = 3


class EstimateTokensRequest(BaseModel):
    text: str


@router.post("/documents", summary="存入文档（LangChain 切片 + 双存储）")
def add_document(doc: DocumentIn, db: Session = Depends(get_db)):
    document = _save_document_to_sqlite(doc, db)

    chunk_texts = text_splitter.split_text(doc.content)

    _prepare_chunks_for_storage(chunk_texts, document, doc, db)

    return ApiResponse(
        code=200,
        status="success",
        content={
            "message": "文档存入成功",
            "document_id": document.id,
            "title": doc.title,
            "chunks_count": len(chunk_texts),
        }
    )


@router.post("/search", summary="语义检索（LangChain 原生）")
def search(query: SearchIn, db: Session = Depends(get_db)):
    results = _search_vectorstore(query.query, k=query.n_results)

    if not results:
        return []

    parsed = _parse_search_results(results, db)

    output = [SearchResult(**r) for r in parsed]

    return ApiResponse(code=200, status="success", content=output)


@router.post("/chat", summary="RAG 流式问答（LangChain 检索 + 推理链保留）")
async def langchain_chat(req: ChatRequest, db: Session = Depends(get_db)):
    docs, context = _retrieve_context(req.query, k=req.n_results, db=db)

    error_msg = _check_token_budget(context, req.query)
    if error_msg:
        async def error_stream():
            yield _yield_sse("error", error_msg)
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    return StreamingResponse(
        _generate_stream(context, req.query, docs),
        media_type="text/event-stream",
    )


@router.post("/estimate-tokens", summary="估算 Token 数量（tiktoken）")
def estimate_tokens_endpoint(req: EstimateTokensRequest):
    return ApiResponse(
        code=200,
        status="success",
        content={"token_count": estimate_tokens(req.text)}
    )


@router.delete("/documents/{doc_id}", summary="删除文档（ChromaDB + SQLite 双删除）")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    document = _find_document_or_404(doc_id, db)
    title = document.title

    deleted_ids = _delete_from_chromadb(document)

    _delete_document_from_sqlite(document, db)

    return ApiResponse(
        code=200,
        status="success",
        content={
            "message": "文档删除成功",
            "document_id": doc_id,
            "title": title,
            "deleted_chunks": len(deleted_ids),
        }
    )


@router.get("/health", summary="LangChain RAG 健康检查")
def health_check():
    try:
        count = get_vectorstore()._collection.count()
        return ApiResponse(
            code=200,
            status="ok",
            content={
                "vectorstore_docs": count,
                "llm_model": LLM_MODEL,
                "embedding_model": EMBEDDING_MODEL,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
