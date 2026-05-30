"""
FastAPI + Chroma 最小原型：将双存储架构封装为 API
=====================================================

提供两个接口：
  POST /rag/documents    → 存入文档（双存储）
  POST /rag/search       → 语义检索（双存储协作）

类比：把图书馆的"采编部"和"查询台"做成了自助服务机
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

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
client = OpenAI(
    base_url="https://api-inference.modelscope.cn/v1",
    api_key=os.getenv("MODELSCOPE_API_KEY")
)

# ChromaDB 客户端（持久化模式，数据存在 ./chroma_db 目录）
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 获取或创建 Collection
collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

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


@router.post("/search", response_model=List[SearchResult], summary="语义检索")
def search(query: SearchIn, db: Session = Depends(get_db)):
    """
    语义检索流程：
    1. 把查询转成向量
    2. ChromaDB 找相似向量（返回 metadatas + distances）
    3. 用 metadatas 里的 document_id 回查 SQLite 取完整信息
    """
    # 1. 查询转向量
    query_vec = get_embedding(query.query)

    # 2. ChromaDB 检索
    chroma_results = collection.query(
        query_embeddings=[query_vec],
        n_results=query.n_results,
        include=["metadatas", "distances"]
    )

    # 3. 解析结果，回查 SQLite
    results = []
    for i in range(query.n_results):
        metadata = chroma_results["metadatas"][0][i]
        distance = chroma_results["distances"][0][i]
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
