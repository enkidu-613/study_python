"""
LangChain RAG 路由：纯 LangChain 原生实现
==========================================

完整替代 rag_router.py（手搓版）的所有接口，尽可能使用 LangChain 原生功能。
不可替代的部分（Token 估算、SQLite 存储）保留推荐实现。

【接口对照】
| 手搓版接口                    | 本文件 LangChain 实现           | 原生度 |
|------------------------------|-------------------------------|--------|
| POST /rag/documents          | POST /langchain-rag/documents | 🟡 80% |
| POST /rag/search             | POST /langchain-rag/search    | 🟢 95% |
| POST /rag/chat               | POST /langchain-rag/chat      | 🟡 70% |
| POST /rag/estimate-tokens    | POST /langchain-rag/estimate-tokens | 🔴 tiktoken |

【各功能 LangChain 覆盖情况】
✅ 文本切片      → RecursiveCharacterTextSplitter
✅ Embedding     → OpenAIEmbeddings
✅ 向量存储      → Chroma.from_documents() / add_documents()
✅ 语义检索      → vectorstore.similarity_search_with_score()
✅ RAG 链        → LCEL (retriever → prompt → llm)
✅ 流式输出      → chain.astream() + StreamingResponse
⚠️ 上下文截断    → 手写 truncate_context（LangChain 无原生组件，且因 SQLite 回查阻断管道无法 RunnableLambda 包装）
⚠️ 推理链处理    → 手动 AIMessageChunk（不用 StrOutputParser）
❌ SQLite 存储    → 保留 SQLAlchemy（LangChain 无 ORM 集成）
❌ Token 估算     → 保留 tiktoken（LangChain 无独立组件）
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from numpy import number
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import AsyncIterator
import json
import os

from dotenv import load_dotenv

# ========== LangChain 核心组件 ==========
from langchain_openai import OpenAIEmbeddings          # Embedding（不变）
from langchain_deepseek import ChatDeepSeek            # 替代 ChatOpenAI，原生支持 DeepSeek 推理链
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document as LCDocument

from langchain_core.messages import AIMessageChunk
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 复用 ChromaDB 客户端（与手搓版共享同一个数据库目录）
import chromadb

# ========== 保留组件（LangChain 无原生替代） ==========
import tiktoken                           # Token 估算

from database import get_db               # SQLite 依赖注入
from models import Document, DocumentChunk  # SQLAlchemy ORM

# ========== 初始化配置 ==========
load_dotenv()

MODELSCOPE_BASE_URL = "https://api-inference.modelscope.cn/v1"
MODELSCOPE_API_KEY = os.getenv("MODELSCOPE_API_KEY")
LLM_MODEL = "deepseek-ai/DeepSeek-V3.2"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"

# 上下文窗口配置
MAX_CONTEXT_TOKENS = 2000
MAX_INPUT_TOKENS = 6000
MAX_OUTPUT_TOKENS = 2000

# ---------- 1. Embedding 模型（LangChain 原生封装） ----------
embedding_model = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_base=MODELSCOPE_BASE_URL,
    openai_api_key=MODELSCOPE_API_KEY,
)

# ---------- 2. LLM（langchain-deepseek 原生支持推理链） ----------
llm = ChatDeepSeek(
    model=LLM_MODEL,
    api_base=MODELSCOPE_BASE_URL,
    api_key=MODELSCOPE_API_KEY,
    temperature=0.7,
    streaming=True,
    model_kwargs={"extra_body": {"thinking": {"type": "enabled"}}},
)

# ---------- 3. VectorStore（LangChain 原生封装） ----------
chroma_client = chromadb.PersistentClient(path="./chroma_db")

vectorstore = Chroma(
    client=chroma_client,
    collection_name="documents",
    embedding_function=embedding_model,
)

# ---------- 4. Retriever（LangChain 原生封装） ----------
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# ---------- 5. TextSplitter（LangChain 原生） ----------
# 替代手搓版的 split_text()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
)


# ========== 工具函数 ==========

def estimate_tokens(text: str, model: str = "cl100k_base") -> int:
    """Token 估算（LangChain 无原生替代，保留 tiktoken）"""
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))


def format_docs(docs) -> str:
    """把检索结果格式化为 Prompt 上下文"""
    formatted = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "未知来源")
        title = doc.metadata.get("title", "未命名")
        formatted.append(f"[{i}] 来源：《{title}》（{source}）\n{doc.page_content}")
    return "\n\n".join(formatted)


def truncate_context(formatted_context: str, max_tokens: int = MAX_CONTEXT_TOKENS) -> str:
    """
    Token 感知的上下文截断。
    按块（每块是一个资料片段）累积，超过上限即停止。

    LangChain 说明：LCEL 没有内置的 "截断到 N token" 组件，
    且因 /chat 接口中 SQLite 回查阻断了管道，此函数以纯函数方式直接调用。
    """
    if not formatted_context:
        return "没有检索到相关文档。"

    blocks = formatted_context.split("\n\n")
    result_blocks = []
    current_tokens = 0

    for block in blocks:
        block_tokens = estimate_tokens(block)
        if current_tokens + block_tokens > max_tokens:
            break  # 超预算即停，results 已按相似度排序
        result_blocks.append(block)
        current_tokens += block_tokens

    return "\n\n".join(result_blocks) if result_blocks else "没有检索到相关文档。"


# ========== Prompt 模板（LangChain 原生） ==========
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

# ========== LCEL 链：检索 → 格式化（不含 LLM，因为 chat 需要手动注入 db） ==========
# 全局定义的纯检索链，供需要无状态查询的场景使用
retrieval_chain = retriever | (lambda docs: format_docs(docs))


# ========== FastAPI 路由 ==========
router = APIRouter(prefix="/langchain-rag", tags=["LangChain RAG"])


# ========== Pydantic 模型（与手搓版一致） ==========

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
    """通用响应包装"""
    code: int = 200
    status: str = "success"
    content: dict | list | str | bool | int | float | None = None


class ChatRequest(BaseModel):
    query: str
    n_results: int = 3


class EstimateTokensRequest(BaseModel):
    text: str


# ==================== 接口 1：存入文档 ====================

@router.post("/documents", summary="存入文档（LangChain 切片 + 双存储）")
def add_document(doc: DocumentIn, db: Session = Depends(get_db)):
    """
    与手搓版 POST /rag/documents 功能一致：

    【LangChain 原生部分】
    - RecursiveCharacterTextSplitter 切片 → 替代手写 split_text()
    - Chroma.add_documents() 一键 Embedding + 存向量 → 替代手写 get_embedding() + collection.add()

    【保留手写部分】
    - SQLAlchemy ORM 存 Document + DocumentChunk 到 SQLite
      （LangChain 没有 SQLAlchemy 集成，保留手写实现）
    """
    # 1. SQLite：完整文档（手写 SQLAlchemy）
    document = Document(title=doc.title, content=doc.content, source=doc.source)
    db.add(document)
    db.commit()
    db.refresh(document)

    # 2. LangChain 原生：RecursiveCharacterTextSplitter 切片
    chunk_texts = text_splitter.split_text(doc.content)

    # 3. 并行构建数据
    lc_docs = []       # LangChain Document 对象（给 ChromaDB）
    chroma_ids = []    # ChromaDB 文档 ID

    for i, chunk_text in enumerate(chunk_texts):
        # 3a. SQLite：存切片元数据（手写）
        chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=i,
            content=chunk_text,
            embedding_id=f"doc{document.id}_chunk{i}"
        )
        db.add(chunk)

        # 3b. LangChain Document：metadata 存够信息，减少后续 SQLite 回查
        lc_docs.append(LCDocument(
            page_content=chunk_text,
            metadata={
                "document_id": document.id,
                "chunk_index": i,
                "title": doc.title,
                "source": doc.source,
            }
        ))
        chroma_ids.append(f"doc{document.id}_chunk{i}")

    # 4. 提交 SQLite
    db.commit()

    # 5. LangChain 原生：一键存入 ChromaDB（自动 Embedding + 存储）
    try:
        vectorstore.add_documents(lc_docs, ids=chroma_ids)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ChromaDB 存储失败（ID 可能重复，请勿重复提交相同文档）: {str(e)}"
        )

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


# ==================== 接口 2：语义检索 ====================

@router.post("/search", summary="语义检索（LangChain 原生）")
def search(query: SearchIn, db: Session = Depends(get_db)):
    """
    与手搓版 POST /rag/search 功能一致：

    【LangChain 原生部分】
    - vectorstore.similarity_search_with_score() → 替代手写 get_embedding() + collection.query()

    【保留手写部分】
    - SQLite 回查（验证切片存在 + 获取精确 title）
      （LangChain 无 SQLAlchemy 集成）

    【分数说明】
    ChromaDB 使用 cosine 距离，返回值是 distance（0=相同, 2=完全相反）。
    转换为相似度：similarity = 1 - distance
    """
    # 1. LangChain 原生：语义检索（一行替代手搓版的 get_embedding + query）
    results_with_scores = vectorstore.similarity_search_with_score(
        query.query,
        k=query.n_results,
    )

    if not results_with_scores:
        return []

    # 2. 解析结果（SQLite 回查增强）
    output = []
    for doc, score in results_with_scores:
        metadata = doc.metadata
        doc_id = metadata.get("document_id")
        chunk_idx = metadata.get("chunk_index")
        similarity = round(1 - score, 4)  # cosine distance → similarity

        # 回查 SQLite 验证并获取精确信息
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

        output.append(SearchResult(
            title=title,
            chunk_content=chunk_content,
            similarity=similarity,
            document_id=doc_id or 0,
            chunk_index=chunk_idx or 0,
        ))

    return ApiResponse(
        code=200,
        status="success",
        content=output
    )


# ==================== 接口 3：RAG 流式问答 ====================

@router.post("/chat", summary="RAG 流式问答（LangChain 检索 + 推理链保留）")
async def langchain_chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    与手搓版 POST /rag/chat 功能一致：

    【LangChain 原生部分】
    - retriever.invoke() → 语义检索
    - LCEL 链 (prompt | llm) → Prompt 拼装 + LLM 调用
    - chain.astream() → 流式输出

    【保留手写部分】
    - SQLite 回查增强 metadata
    - Token 感知的上下文截断（truncate_context）
    - 推理链保留（AIMessageChunk.additional_kwargs.reasoning_content）
      不用 StrOutputParser() 因为它会丢弃推理内容

    【StreamingResponse 对比】
    手搓版：手动构造 OpenAI client → 手动 yield SSE
    本文件：chain.astream() 自动流式，外层只包装 SSE 格式
    """
    # 1. LangChain 原生语义检索（使用请求中的 n_results 动态控制检索数量）
    docs = vectorstore.similarity_search(req.query, k=req.n_results)

    # 2. SQLite 回查增强 metadata（手写，LangChain 无此集成）
    for doc in docs:
        doc_id = doc.metadata.get("document_id")
        if doc_id:
            db_doc = db.query(Document).filter(Document.id == doc_id).first()
            if db_doc:
                doc.metadata["title"] = db_doc.title
                doc.metadata["source"] = db_doc.source or "未知来源"

    # 3. 格式化 + Token 截断
    context = format_docs(docs)
    context = truncate_context(context)

    # 4. LCEL 链：不带 StrOutputParser，保留 AIMessageChunk 以支持推理链
    chain = RAG_PROMPT | llm  # 注意：不用 StrOutputParser()

    async def generate() -> AsyncIterator[str]:
        try:
            total_input = estimate_tokens(context) + estimate_tokens(req.query)
            if total_input > MAX_INPUT_TOKENS:
                error_data = {
                    "type": "error",
                    "content": "输入总 Token 数量超过最大限制，请减少检索结果数量或精简问题。"
                }
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
                return

            done_thinking = False

            # chain.astream() 返回 AIMessageChunk（因为没挂 StrOutputParser）
            async for chunk in chain.astream(
                {"context": context, "question": req.query},
                config={"max_tokens": MAX_OUTPUT_TOKENS}
            ):
                if isinstance(chunk, AIMessageChunk):
                    # 推理链（DeepSeek 的 thinking content）
                    reasoning = chunk.additional_kwargs.get("reasoning_content", "")
                    answer = chunk.content

                    if reasoning:
                        data = {"type": "thinking", "content": reasoning}
                        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

                    if answer:
                        if not done_thinking:
                            divider = {"type": "divider", "content": "\n\n === Final Answer ===\n"}
                            yield f"data: {json.dumps(divider, ensure_ascii=False)}\n\n"
                            done_thinking = True
                        data = {"type": "answer", "content": answer}
                        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

            # 来源信息
            sources = []
            for i, doc in enumerate(docs, start=1):
                title = doc.metadata.get("title", "未命名")
                source = doc.metadata.get("source", "未知来源")
                sources.append(f"[{i}] 《{title}》（{source}）")

            if sources:
                source_data = {
                    "type": "sources",
                    "content": f"\n\n【参考来源】\n" + "\n".join(sources)
                }
                yield f"data: {json.dumps(source_data, ensure_ascii=False)}\n\n"

            done_data = {"type": "done"}
            yield f"data: {json.dumps(done_data, ensure_ascii=False)}\n\n"

        except Exception as e:
            error_data = {"type": "error", "content": f"链执行出错: {str(e)}"}
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


# ==================== 接口 4：Token 估算 ====================

@router.post("/estimate-tokens", summary="估算 Token 数量（tiktoken，LangChain 无原生替代）")
def estimate_tokens_endpoint(req: EstimateTokensRequest):
    """
    与手搓版 POST /rag/estimate-tokens 完全一致。
    LangChain 没有独立的 Token 估算组件，保留 tiktoken。
    """
    return ApiResponse(
        code=200,
        status="success",
        content={"token_count": estimate_tokens(req.text)}
    )


# ==================== 接口 5：删除文档 ====================

@router.delete("/documents/{doc_id}", summary="删除文档（ChromaDB + SQLite 双删除）")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """
    根据文档 ID 删除文档，同时清理 ChromaDB 向量数据和 SQLite 记录。
    """
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail=f"文档 ID={doc_id} 不存在")

    # 1. 收集所有 chunk 的 embedding_id，从 ChromaDB 删除
    embedding_ids = [chunk.embedding_id for chunk in document.chunks]
    if embedding_ids:
        try:
            vectorstore.delete(ids=embedding_ids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ChromaDB 删除失败: {str(e)}")

    # 2. 从 SQLite 删除（cascade 自动删除关联的 chunks）
    title = document.title
    db.delete(document)
    db.commit()

    return ApiResponse(
        code=200,
        status="success",
        content={
            "message": "文档删除成功",
            "document_id": doc_id,
            "title": title,
            "deleted_chunks": len(embedding_ids),
        }
    )


# ==================== 接口 6：健康检查 ====================

@router.get("/health", summary="LangChain RAG 健康检查")
def health_check():
    """检查 LangChain 各组件是否正常加载"""
    try:
        count = vectorstore._collection.count()
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