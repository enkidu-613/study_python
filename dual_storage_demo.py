"""
双存储架构演示：SQLite + ChromaDB 协作
=========================================
类比：图书馆系统
- SQLite  = 藏书仓库（存完整书籍）
- ChromaDB = 索引卡片柜（存主题标签，快速查找）
"""

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

# SQLAlchemy 相关
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Document, DocumentChunk

# ========== 第0步：加载环境变量 ==========
load_dotenv()
client = OpenAI(
    base_url="https://api-inference.modelscope.cn/v1",
    api_key=os.getenv("MODELSCOPE_API_KEY")
)

# ========== 第1步：创建 ChromaDB 客户端 ==========
client_db = chromadb.Client()

# 创建 Collection（索引卡片柜）
collection = client_db.create_collection(
    name="document_chunks",
    metadata={"hnsw:space": "cosine"}
)

# ========== 第2步：Embedding 工具函数 ==========
def get_embedding(text: str) -> list[float]:
    """把文字转成向量（语义身份证）"""
    response = client.embeddings.create(
        model="Qwen/Qwen3-Embedding-8B",
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding


# ========== 第3步：文档切片函数 ==========
def split_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    """
    把长文本切成小片段
    类比：把一本厚书拆成若干章节

    chunk_size: 每片多少字
    overlap:    相邻两片重叠多少字（防止断句丢失上下文）
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)  # 步进 = 片长 - 重叠
    return chunks


# ========== 第4步：存入文档（双存储）==========
def add_document(title: str, content: str, source: str = ""):
    """
    把一篇文档同时存入两个数据库：
    1. SQLite → 存完整文档 + 切片信息
    2. ChromaDB → 存切片的向量（用于语义检索）
    """
    db = SessionLocal()
    try:
        # --- 4.1 存入 SQLite：完整文档 ---
        doc = Document(title=title, content=content, source=source)
        db.add(doc)
        db.commit()           # 先提交，拿到 doc.id
        db.refresh(doc)       # 刷新，获取自增ID
        print(f"📚 SQLite: 存入完整文档 id={doc.id}, title='{title}'")

        # --- 4.2 切片 ---
        chunks = split_text(content, chunk_size=80, overlap=10)
        print(f"✂️  切成 {len(chunks)} 个片段")

        # --- 4.3 逐片处理 ---
        chroma_ids = []
        chroma_embeddings = []
        chroma_documents = []
        chroma_metadatas = []

        for idx, chunk_text in enumerate(chunks):
            # 4.3.1 存入 SQLite：切片信息
            chunk = DocumentChunk(
                document_id=doc.id,
                chunk_index=idx,
                content=chunk_text,
                embedding_id=f"doc{doc.id}_chunk{idx}"
            )
            db.add(chunk)

            # 4.3.2 生成向量
            vec = get_embedding(chunk_text)

            # 4.3.3 准备 ChromaDB 数据
            chroma_ids.append(f"doc{doc.id}_chunk{idx}")
            chroma_embeddings.append(vec)
            chroma_documents.append(chunk_text)
            chroma_metadatas.append({
                "document_id": doc.id,
                "chunk_index": idx,
                "title": title
            })

            print(f"   片段{idx}: '{chunk_text[:30]}...' → 向量维度{len(vec)}")

        # --- 4.4 提交 SQLite 切片 ---
        db.commit()

        # --- 4.5 存入 ChromaDB：向量 ---
        collection.add(
            ids=chroma_ids,
            embeddings=chroma_embeddings,
            documents=chroma_documents,
            metadatas=chroma_metadatas
        )
        print(f"🎯 ChromaDB: 存入 {len(chroma_ids)} 个向量\n")

    finally:
        db.close()


# ========== 第5步：语义检索（双存储协作）==========
def semantic_search(query: str, n_results: int = 3):
    """
    双存储协作查询：
    1. ChromaDB 快速找到相关切片的 embedding_id
    2. SQLite 根据 embedding_id 取出完整信息
    """
    print(f"\n🔍 用户查询: '{query}'")
    print("=" * 50)

    # --- 5.1 查询转成向量 ---
    query_vec = get_embedding(query)

    # --- 5.2 ChromaDB 快速检索（只返回ID和相似度）---
    chroma_results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    # --- 5.3 解析 ChromaDB 结果 ---
    db = SessionLocal()
    try:
        results = []

        for i in range(n_results):
            metadata = chroma_results["metadatas"][0][i]
            distance = chroma_results["distances"][0][i]
            similarity = 1 - distance

            doc_id = metadata["document_id"]
            chunk_idx = metadata["chunk_index"]

            # --- 5.4 去 SQLite 查完整信息 ---
            chunk = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == doc_id,
                DocumentChunk.chunk_index == chunk_idx
            ).first()

            if chunk:
                document = db.query(Document).filter(Document.id == doc_id).first()
                results.append({
                    "rank": i + 1,
                    "similarity": similarity,
                    "chunk_content": chunk.content,
                    "chunk_index": chunk_idx,
                    "document_title": document.title if document else "未知",
                    "document_source": document.source if document else ""
                })

        # --- 5.5 展示结果 ---
        for r in results:
            print(f"\n  排名 {r['rank']} | 相似度: {r['similarity']:.4f}")
            print(f"  📄 来源: 《{r['document_title']}》第{r['chunk_index']}片段")
            print(f"  📝 内容: {r['chunk_content']}")

        return results

    finally:
        db.close()


# ========== 第6步：演示数据 ==========
if __name__ == "__main__":
    print("🚀 双存储架构演示开始")
    print("=" * 50)

    # 模拟两篇文档
    doc1 = """
Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。
它以简洁、易读的语法著称，非常适合初学者学习编程。
Python 广泛应用于 Web 开发、数据分析、人工智能等领域。
Django 和 Flask 是 Python 最流行的 Web 框架。
在数据科学领域，Python 配合 NumPy、Pandas 库几乎成为了行业标准。
"""

    doc2 = """
苹果是一种常见的水果，原产于中亚地区。苹果富含维生素 C 和膳食纤维，
对健康有很多好处。每天吃一个苹果，医生远离我，这句谚语广为人知。
苹果有很多品种，如红富士、青苹果、金帅等。不同品种的口感和甜度各不相同。
苹果还可以做成苹果派、苹果汁、苹果酱等各种美食。
在西方国家，苹果派是非常受欢迎的传统甜点。
"""

    # 存入文档1
    add_document(
        title="Python编程语言介绍",
        content=doc1.strip(),
        source="编程百科"
    )

    # 存入文档2
    add_document(
        title="苹果的营养与品种",
        content=doc2.strip(),
        source="水果百科"
    )

    # 语义检索测试
    print("\n" + "=" * 50)
    print("📋 测试1：查询编程相关内容")
    semantic_search("我想学习 Web 开发", n_results=2)

    print("\n" + "=" * 50)
    print("📋 测试2：查询水果相关内容")
    semantic_search("什么水果对健康好？", n_results=2)

    print("\n" + "=" * 50)
    print("📋 测试3：查询甜点相关内容")
    semantic_search("我想做甜点", n_results=2)
