import chromadb

# ┌─────────────────────────────────────────────────────────────┐
# │  第1步：创建 ChromaDB 客户端                                │
# │                                                             │
# │  ChromaDB 支持两种模式：                                     │
# │  1. 内存模式：数据存在内存，程序结束就没了                    │
# │  2. 持久化模式：数据存到磁盘，下次还能用                      │
# └─────────────────────────────────────────────────────────────┘

# 内存模式（学习阶段先用这个，简单）
client = chromadb.Client()

# 持久化模式（实际项目用这个）
# client = chromadb.PersistentClient(path="./chroma_db")

# ┌─────────────────────────────────────────────────────────────┐
# │  第2步：创建 Collection（集合）                             │
# │                                                             │
# │  Collection = 数据库里的"表"                                │
# │  每个 Collection 存一组相关的向量和文本                      │
# │                                                             │
# │  参数说明：                                                  │
# │  • name: 集合名称                                            │
# │  • metadata: 集合的配置信息                                  │
# │    - "hnsw:space": "cosine" → 用余弦相似度做检索             │
# └─────────────────────────────────────────────────────────────┘

collection = client.create_collection(
    name="my_knowledge",
    metadata={"hnsw:space": "cosine"}  # 指定用余弦相似度
)

print(f"✅ Collection 创建成功: {collection.name}")

# ┌─────────────────────────────────────────────────────────────┐
# │  第3步：添加数据（文档 + 向量）                              │
# │                                                             │
# │  这里先用手动向量演示，后面会接 Embedding API                │
# │                                                             │
# │  参数说明：                                                  │
# │  • ids: 每条数据的唯一标识（字符串）                         │
# │  • documents: 原始文本                                       │
# │  • embeddings: 对应的向量（列表的列表）                      │
# │  • metadatas: 额外信息（可选）                               │
# └─────────────────────────────────────────────────────────────┘

# 模拟3个文本的向量（实际应该用 Embedding API 生成）
# 为了演示，用简化向量：维度=4，值代表语义方向
documents = [
    "苹果是一种水果，味道酸甜可口",
    "香蕉是黄色的热带水果",
    "Python 是一种编程语言"
]

# 简化向量（实际应该是 1024 维的 Embedding）
# 这里用人工构造的向量来演示概念：
# - 水果相关文档的向量在某几个维度值相近
# - 编程语言的向量方向不同
embeddings = [
    [0.9, 0.8, 0.1, 0.2],   # 苹果 → 水果语义
    [0.85, 0.75, 0.15, 0.1], # 香蕉 → 水果语义（方向相近）
    [0.1, 0.2, 0.9, 0.8]    # Python → 编程语义（方向不同）
]

collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {"category": "水果", "source": "百科"},
        {"category": "水果", "source": "百科"}, 
        {"category": "编程", "source": "教程"}
    ]
)

print(f"✅ 添加 {len(documents)} 条数据成功")

# ┌─────────────────────────────────────────────────────────────┐
# │  第4步：语义检索（核心功能！）                               │
# │                                                             │
# │  输入一个查询向量，返回最相似的 Top-K 结果                   │
# │  底层就是计算余弦相似度，排序返回                            │
# └─────────────────────────────────────────────────────────────┘

# 查询："我喜欢吃甜的水果" → 构造一个水果方向的查询向量
query_embedding = [0.88, 0.82, 0.12, 0.15]  # 方向接近水果

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2,  # 返回最相似的2条
    include=["documents", "distances", "metadatas"]
)

print("\n🔍 查询结果：")
for i, (doc, distance, metadata) in enumerate(zip(
    results["documents"][0],
    results["distances"][0],
    results["metadatas"][0]
)):
    # ChromaDB 的 cosine 距离 = 1 - 相似度，所以越小越相似
    similarity = 1 - distance
    print(f"  排名{i+1}: {doc}")
    print(f"    相似度: {similarity:.4f} (距离: {distance:.4f})")
    print(f"    元数据: {metadata}")
    print()

# ┌─────────────────────────────────────────────────────────────┐
# │  第5步：验证 — 查询编程相关的内容                            │
# │                                                             │
# │  用不同方向的查询向量，应该返回 Python 文档                  │
# └─────────────────────────────────────────────────────────────┘

query_embedding_code = [0.15, 0.1, 0.85, 0.9]  # 方向接近编程

results2 = collection.query(
    query_embeddings=[query_embedding_code],
    n_results=2,
    include=["documents", "distances", "metadatas"]
)

print("🔍 编程相关查询结果：")
for i, (doc, distance, metadata) in enumerate(zip(
    results2["documents"][0],
    results2["distances"][0],
    results2["metadatas"][0]
)):
    similarity = 1 - distance
    print(f"  排名{i+1}: {doc}")
    print(f"    相似度: {similarity:.4f}")
    print(f"    元数据: {metadata}")
