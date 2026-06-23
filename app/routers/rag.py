"""
FastAPI + Chroma 最小原型：将双存储架构封装为 API

提供接口：
  POST /rag/documents    → 存入文档（双存储）
  POST /rag/search       → 语义检索（双存储协作）
  POST /rag/chat         → RAG 流式问答
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
import json
import tiktoken

from app.database import SessionLocal
from app.models import Document, DocumentChunk

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_API_URL = os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2")

client = OpenAI(
    base_url=MODEL_API_URL,
    api_key=os.getenv("MODELSCOPE_API_KEY")
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

MAX_CONTEXT_TOKENS = 2000
MAX_INPUT_TOKENS = 6000
MAX_OUTPUT_TOKENS = 2000

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


class ChatRequest(BaseModel):
    query: str
    n_results: int = 3


class EstimateTokensRequest(BaseModel):
    text: str


from app.embedding import get_embedding


def split_text(text: str, chunk_size: int = 80, overlap: int = 10) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def estimate_tokens(text: str,model = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))

router = APIRouter(prefix="/rag", tags=["RAG 向量检索"])


@router.post("/documents", summary="存入文档（双存储）")
def add_document(doc: DocumentIn, db: Session = Depends(get_db)):
    document = Document(title=doc.title, content=doc.content, source=doc.source)
    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = split_text(doc.content, chunk_size=80, overlap=10)

    chroma_ids = []
    chroma_embeddings = []
    chroma_documents = []
    chroma_metadatas = []

    for idx, chunk_text in enumerate(chunks):
        chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=idx,
            content=chunk_text,
            embedding_id=f"doc{document.id}_chunk{idx}"
        )
        db.add(chunk)

        vec = get_embedding(chunk_text)

        chroma_ids.append(f"doc{document.id}_chunk{idx}")
        chroma_embeddings.append(vec)
        chroma_documents.append(chunk_text)
        chroma_metadatas.append({
            "document_id": document.id,
            "chunk_index": idx,
            "title": doc.title
        })

    db.commit()

    collection.add(
        ids=chroma_ids,
        embeddings=chroma_embeddings,
        documents=chroma_documents,
        metadatas=chroma_metadatas
    )

    return {
        "message": "文档存入成功",
        "document_id": document.id,
        "title": doc.title,
        "chunks_count": len(chunks)
    }


def _semantic_search(query_text: str, n_results: int, db: Session) -> List[SearchResult]:
    query_vec = get_embedding(query_text)

    chroma_results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    results = []
    metadatas = chroma_results.get("metadatas", [[]])[0]
    distances = chroma_results.get("distances", [[]])[0]

    if not metadatas:
        return results

    for i in range(len(metadatas)):
        metadata = metadatas[i]
        distance = distances[i]
        similarity = round(1 - distance, 4)

        doc_id = metadata["document_id"]
        chunk_idx = metadata["chunk_index"]

        chunk = db.query(DocumentChunk).filter(
            DocumentChunk.document_id == doc_id,
            DocumentChunk.chunk_index == chunk_idx
        ).first()

        if chunk:
            document = db.query(Document).filter(Document.id == doc_id).first()
            results.append(SearchResult(
                title=document.title if document else "未知",
                chunk_content=chunk.content,
                similarity=similarity,
                document_id=doc_id,
                chunk_index=chunk_idx
            ))

    return results


@router.post("/search", response_model=List[SearchResult], summary="语义检索")
def search(query: SearchIn, db: Session = Depends(get_db)):
    return _semantic_search(query.query, query.n_results, db)


def build_system_prompt(results: List[SearchResult], max_context: int = MAX_CONTEXT_TOKENS) -> str:
    if not results:
        return "没有检索到与用户问题相关的资料。请礼貌地告诉用户：根据现有知识库无法回答该问题。"

    context_blocks = []
    current_tokens = 0
    for i, r in enumerate(results, start=1):
        block = f"[{i}] 来源：《{r.title}》第{r.chunk_index}段（相关度：{r.similarity:.2f}）\n{r.chunk_content}"
        block_tokens = estimate_tokens(block)
        if current_tokens + block_tokens > max_context:
            break
        context_blocks.append(block)
        current_tokens += block_tokens


    context = "\n\n".join(context_blocks)

    prompt = f"""你是一个基于知识库的问答助手。请严格根据下面提供的资料片段回答用户问题。

【资料片段】
{context}

【回答要求】
1. 只基于上面的资料回答，不要编造资料中没有的信息。
2. 如果资料不足以回答问题，请明确说明"根据现有资料无法回答"。
3. 如果引用了某个片段，请在回答末尾标注来源，格式如：[来源：《标题》第N段]
4. 保持简洁清晰。"""

    return prompt


async def generate_rag_stream(query: str, results: List[SearchResult], max_input: int = MAX_INPUT_TOKENS):
    system_prompt = build_system_prompt(results)

    total_input = estimate_tokens(system_prompt) + estimate_tokens(query)
    if total_input > max_input:
        error_data = {"type": "error", "content": "输入总 Token 数量超过最大限制，请减少检索结果数量或精简问题。"}
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
        return
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
        max_tokens=MAX_OUTPUT_TOKENS,
        extra_body={"enable_thinking": True}
    )

    done_thinking = False

    for chunk in response:
        if chunk.choices:
            thinking = chunk.choices[0].delta.reasoning_content
            answer = chunk.choices[0].delta.content

            if thinking and thinking != '':
                data = {"type": "thinking", "content": thinking}
            elif answer and answer != '':
                if not done_thinking:
                    data = {"type": "divider", "content": "\n\n === Final Answer ===\n"}
                    done_thinking = True
                else:
                    data = {"type": "answer", "content": answer}
            else:
                continue

            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/chat", summary="RAG 知识库问答")
async def rag_chat(req: ChatRequest, db: Session = Depends(get_db)):
    results = _semantic_search(req.query, req.n_results, db)

    return StreamingResponse(
        generate_rag_stream(req.query, results),
        media_type="text/event-stream"
    )

@router.post("/estimate-tokens", summary="估算文本中包含的 Token 数量")
def estimate_tokens_endpoint(req: EstimateTokensRequest):
    return {"token_count": estimate_tokens(req.text)}
