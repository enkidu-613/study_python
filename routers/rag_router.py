"""
FastAPI + Chroma 最小原型：将双存储架构封装为 API
=====================================================

提供两个接口：
  POST /rag/documents    → 存入文档（双存储）
  POST /rag/search       → 语义检索（双存储协作）

类比：把图书馆的"采编部"和"查询台"做成了自助服务机
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
import json
import tiktoken

# 数据库
from database import SessionLocal
from models import Document, DocumentChunk

# ChromaDB + Embedding
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

# ========== 初始化 ==========
load_dotenv()

# OpenAI 客户端（ModelScope）
MODEL_API_URL = os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2")

client = OpenAI(
    base_url=MODEL_API_URL,
    api_key=os.getenv("MODELSCOPE_API_KEY")
)

# ChromaDB 客户端（持久化模式，数据存在 ./chroma_db 目录）
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 获取或创建 Collection
collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

# ========== 上下文窗口配置 ==========
MAX_CONTEXT_TOKENS = 2000   # 资料片段上限
MAX_INPUT_TOKENS = 6000     # 总输入上限（System Prompt + User Query）
MAX_OUTPUT_TOKENS = 2000    # LLM 回答长度上限

# ========== 依赖注入：数据库会话 ==========
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== Pydantic 模型 ==========
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


# ========== Embedding 工具 ==========
def get_embedding(text: str) -> list[float]:
    """把文字转成 4096 维向量"""
    response = client.embeddings.create(
        model="Qwen/Qwen3-Embedding-8B",
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding


# ========== 文本切片 ==========
def split_text(text: str, chunk_size: int = 80, overlap: int = 10) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

# ========== 估算 Token =========
def estimate_tokens(text: str,model = "cl100k_base") -> int:
    """估算文本中包含的 Token 数量"""
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))

# ========== 路由 ==========
router = APIRouter(prefix="/rag", tags=["RAG 向量检索"])


@router.post("/documents", summary="存入文档（双存储）")
def add_document(doc: DocumentIn, db: Session = Depends(get_db)):
    """
    把一篇文档同时存入 SQLite 和 ChromaDB：
    1. SQLite 存完整文档 + 切片信息
    2. ChromaDB 存切片向量（用于语义检索）
    """
    # 1. 存入 SQLite：完整文档
    document = Document(title=doc.title, content=doc.content, source=doc.source)
    db.add(document)
    db.commit()
    db.refresh(document)

    # 2. 切片
    chunks = split_text(doc.content, chunk_size=80, overlap=10)

    # 3. 准备 ChromaDB 数据
    chroma_ids = []
    chroma_embeddings = []
    chroma_documents = []
    chroma_metadatas = []

    for idx, chunk_text in enumerate(chunks):
        # 3.1 SQLite 切片
        chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=idx,
            content=chunk_text,
            embedding_id=f"doc{document.id}_chunk{idx}"
        )
        db.add(chunk)

        # 3.2 生成向量
        vec = get_embedding(chunk_text)

        # 3.3 准备 ChromaDB 数据
        chroma_ids.append(f"doc{document.id}_chunk{idx}")
        chroma_embeddings.append(vec)
        chroma_documents.append(chunk_text)
        chroma_metadatas.append({
            "document_id": document.id,
            "chunk_index": idx,
            "title": doc.title
        })

    # 4. 提交 SQLite
    db.commit()

    # 5. 存入 ChromaDB
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
    """
    内部函数：执行语义检索（供 search 和 rag_chat 复用）
    """
    # 1. 查询转向量
    query_vec = get_embedding(query_text)

    # 2. ChromaDB 检索
    chroma_results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    # 3. 解析结果，回查 SQLite
    results = []
    metadatas = chroma_results.get("metadatas", [[]])[0]
    distances = chroma_results.get("distances", [[]])[0]

    if not metadatas:
        return results  # ChromaDB 没返回结果，直接空列表

    for i in range(len(metadatas)):
        metadata = metadatas[i]
        distance = distances[i]
        similarity = round(1 - distance, 4)

        doc_id = metadata["document_id"]
        chunk_idx = metadata["chunk_index"]

        # 回查 SQLite
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
    """
    语义检索接口：返回检索到的相关片段
    """
    return _semantic_search(query.query, query.n_results, db)


def build_system_prompt(results: List[SearchResult], max_context: int = MAX_CONTEXT_TOKENS) -> str:
    """
    把检索结果拼进 System Prompt
    """
    if not results:
        return "没有检索到与用户问题相关的资料。请礼貌地告诉用户：根据现有知识库无法回答该问题。"

    # 把每个片段格式化成带编号的内容块
    context_blocks = []
    #限制总的token数量
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
    """
    异步生成器：调用 LLM 并流式返回
    """
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
    """
    RAG 闭环接口：
    1. 语义检索
    2. 拼 System Prompt
    3. 流式调 LLM
    """
    # 1. 检索
    results = _semantic_search(req.query, req.n_results, db)

    # 2. 流式返回 LLM 回答
    return StreamingResponse(
        generate_rag_stream(req.query, results),
        media_type="text/event-stream"
    )

# 估算 Token 数量的路由
@router.post("/estimate-tokens", summary="估算文本中包含的 Token 数量")
def estimate_tokens_endpoint(req: EstimateTokensRequest):
    return {"token_count": estimate_tokens(req.text)}