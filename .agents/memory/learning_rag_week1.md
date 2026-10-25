# 🚀 RAG 第一周：向量数据库入门实战

> **适合 ADHD 的向量数据库学习指南**  
> 基于你已经掌握的：Python、FastAPI、SQLAlchemy → 快速迁移到向量数据库

---

## 🧠 一、核心概念：从 SQLAlchemy 到 Vector DB

既然你已经熟练掌握了 SQLAlchemy（关系型数据库），我们用类比法来快速击穿向量数据库的核心逻辑。

| 概念 | 关系型数据库 (MySQL/SQLite) | 向量数据库 (Chroma) | 一句话理解 |
| :--- | :--- | :--- | :--- |
| **核心存储** | 结构化数据 (行/列) | 向量 + 元数据 | 向量是一串浮点数，代表文本的"语义指纹" |
| **数据集合** | Table (表) | Collection (集合) | 类似于一个列表容器 |
| **检索单位** | Entity / Point | 一条记录 | 包含 ID、向量、原始文本、元数据 |
| **核心能力** | 精确查询 (`LIKE`, `=`) | 近似最近邻搜索 (ANN) | **关键区别**：字面匹配 vs 语义理解 |
| **索引结构** | B+树 | HNSW / IVF | HNSW 是目前 99% RAG 场景的最优索引 |

### 🎯 一句话总结

> **向量数据库** = 专门存一串数字，并能快速找到"最像"的那几串的数据库。

**在 RAG 中的流程**：
```
文本 → Embedding模型 → 变成向量 → 存入向量库 → 语义检索 → 最相关文本 → 给LLM
```

---

## 📅 二、本周实战任务清单

### 🔹 Day 1-2：向量化与语义理解

**目标**：理解文本是如何变成数字的。

#### 任务 1：Embedding 初体验

使用 OpenAI 的 `text-embedding-3-small` 模型，写一个 Python 脚本：

```python
import numpy as np
from openai import OpenAI

client = OpenAI()

def get_embedding(text: str) -> list[float]:
    """将文本转换为向量"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# 测试语义理解
text1 = "如何提升代码质量"
text2 = "提高程序可维护性的方法"
text3 = "今天天气真好"

vec1 = get_embedding(text1)
vec2 = get_embedding(text2)
vec3 = get_embedding(text3)

# 计算余弦相似度
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"句子1 vs 句子2: {cosine_similarity(vec1, vec2):.4f}")  # 应该很高
print(f"句子1 vs 句子3: {cosine_similarity(vec1, vec3):.4f}")  # 应该很低
```

**思考点**：
- 句子1和句子2没有一个字相同，为什么相似度很高？
- 这就是**语义理解** vs **字面匹配**的本质区别！

---

### 🔹 Day 3-4：ChromaDB 入库与检索

**目标**：搭建本地向量库，完成数据的"存"与"取"。

#### 类比 SQLAlchemy → Chroma

| SQLAlchemy | Chroma | 作用 |
|------------|--------|------|
| `create_engine()` | `chromadb.Client()` | 创建连接 |
| `SessionLocal` | `PersistentClient` | 持久化存储 |
| `Base.metadata.create_all()` | `get_or_create_collection()` | 创建"表" |
| `session.add()` | `collection.add()` | 插入数据 |
| `session.query()` | `collection.query()` | 查询数据 |

#### 任务 2：Chroma 基础 CRUD

```python
import chromadb

# 1. 初始化客户端（类似 SQLAlchemy 的 Engine）
client = chromadb.PersistentClient(path="./chroma_db")

# 2. 创建集合（类似 SQLAlchemy 的 Table）
collection = client.get_or_create_collection(name="tech_docs")

# 3. 插入数据（类似 session.add()）
documents = [
    "FastAPI 是一个高性能的 Python Web 框架",
    "SQLAlchemy 是 Python 的 ORM 工具",
    "向量数据库用于语义检索",
    "Python 支持异步编程",
    "Docker 用于容器化部署"
]
ids = ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"]
metadatas = [
    {"category": "web"},
    {"category": "database"},
    {"category": "ai"},
    {"category": "language"},
    {"category": "devops"}
]

collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

# 4. 查询（注意：这是语义检索，不是 LIKE）
results = collection.query(
    query_texts=["我想学 Python"],
    n_results=3
)

print("查询结果：")
for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"  - {doc} (分类: {metadata['category']})")
```

#### 💡 对比实验

```python
# SQL LIKE 查询会漏掉什么？
# LIKE '%Python%' → 只能找到包含"Python"这几个字的
# 语义检索 → 能找到"编程语言"、"Pythonic"、"蟒蛇"等语义相关的
```

---

### 🔹 Day 5：生产级设计思维（关键进阶）

**目标**：理解生产环境的数据结构设计。

#### 设计你的 ChunkVector 结构

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChunkVector(BaseModel):
    """
    生产级向量记录结构
    设计原则：只冗余检索必须的字段
    """
    # 核心字段（必须）
    id: str                    # 主键，桥接关系库
    content: str               # 原文内容，省去回关系库查询
    vector: List[float]        # 向量（通常由库自动生成）
    
    # 标量过滤字段（检索前预过滤）
    knowledge_base_id: str     # 分区键，按知识库隔离
    document_id: str           # 支持按文档过滤
    enabled: bool = True       # 禁用标记
    
    # 可选元数据
    chunk_index: int           # 文档内的块序号
    token_count: Optional[int] = None  # 分词数量（统计用）
    
    # 注意：created_at/updated_at 等审计字段存在关系库，不在向量库冗余
```

#### 架构思想：双存储架构 (CQRS)

```
┌─────────────────┐     ┌─────────────────┐
│   关系数据库     │     │   向量数据库     │
│  (PostgreSQL)   │◄───►│   (Chroma)      │
│                 │     │                 │
│  • 写入/管理    │     │  • 语义检索     │
│  • 事务一致性   │     │  • ANN 搜索     │
│  • 权限控制     │     │  • 相似度计算   │
└─────────────────┘     └─────────────────┘
         │                       │
         └──────────┬────────────┘
                    ▼
            ┌───────────────┐
            │    RAG 应用    │
            └───────────────┘
```

**为什么分离？**
- 向量库不适合频繁写入和事务
- 关系库不适合相似度计算
- 各司其职，专业的事交给专业的系统

---

## 🛠️ 三、动手实践：RAG 最小原型

结合你已有的 FastAPI 知识，写一个"记忆检索"接口。

```python
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 1. 初始化向量数据库（类似 Engine）
client = chromadb.PersistentClient(path="./db")

# 2. 创建集合（类似 Table）
collection = client.get_or_create_collection(name="tech_docs")


class DocumentIn(BaseModel):
    text: str
    doc_id: str
    category: str = "general"


class SearchQuery(BaseModel):
    query: str
    top_k: int = 3


@app.post("/ingest")
async def ingest_document(doc: DocumentIn):
    """将文档存入向量库 - 类似 POST /items"""
    try:
        collection.add(
            documents=[doc.text],
            ids=[doc.doc_id],
            metadatas=[{"category": doc.category}]
        )
        return {"status": "success", "id": doc.doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search_knowledge(query: SearchQuery):
    """语义检索 - 关键区别：不是 LIKE 查询，而是 ANN 搜索"""
    try:
        results = collection.query(
            query_texts=[query.query],
            n_results=query.top_k
        )
        
        # 格式化返回结果
        matches = []
        for doc, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            matches.append({
                "content": doc,
                "metadata": metadata,
                "similarity_score": 1 - distance  # 转换为相似度
            })
        
        return {
            "query": query.query,
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📋 四、本周检查清单

### Day 1-2 完成标准
- [ ] 成功运行 Embedding 脚本
- [ ] 理解余弦相似度的计算
- [ ] 体验语义相近但字面不同的句子

### Day 3-4 完成标准
- [ ] 安装 `chromadb` 并初始化成功
- [ ] 成功创建 Collection 并存入 5+ 条数据
- [ ] 实现语义查询并返回正确结果
- [ ] 对比 LIKE vs ANN 的差异

### Day 5 完成标准
- [ ] 设计 ChunkVector Pydantic 模型
- [ ] 理解双存储架构的设计思想
- [ ] 完成 FastAPI 最小原型

---

## 💡 五、本周核心收获

1. **ANN vs LIKE**：理解了为什么向量检索能解决传统搜索的"盲区"
2. **Chroma 实战**：掌握了向量库的基本 CRUD
3. **架构视野**：建立了"向量库管检索，关系库管数据"的双存储思维

---

## 🔮 下周预告：LangChain 集成

当你有了向量数据库这个"外挂大脑"后，下周我们将引入 LangChain：

- 自动化的文档切片 (Document Loader + Text Splitter)
- 将检索结果填入 Prompt (Prompt Template)
- 实现真正的 RAG (检索增强生成) 闭环

**准备工作**：
```bash
pip install chromadb openai fastapi uvicorn python-dotenv
```

---

## 🔗 参考资源

- [Chroma 官方文档](https://docs.trychroma.com/)
- [OpenAI Embedding 指南](https://platform.openai.com/docs/guides/embeddings)
- [腾讯云向量数据库设计](https://cloud.tencent.com/document/product/1709)
