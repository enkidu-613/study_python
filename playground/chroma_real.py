import chromadb
import numpy as np
from dotenv import load_dotenv
import os

# ========== 第0步：加载环境变量 ==========
load_dotenv()

# ========== 本地 Embedding（不再依赖外部 API）==========
from local_embedding import get_embedding

# ========== 第1步：创建 ChromaDB 客户端 ==========
# Client() = 内存模式，数据存在内存里，程序结束就没了
# 学习阶段用这个，简单，不用管文件路径
client_db = chromadb.Client()

# ========== 第2步：创建 Collection（集合）==========
# Collection = 数据库里的"一张表"
# 这张表里存：id、原始文本、向量、额外信息
collection = client_db.create_collection(
    name="fruit_knowledge",           # 表的名字
    metadata={"hnsw:space": "cosine"} # 用余弦相似度做检索
)

# ========== 第3步：准备要存入的文本 ==========
# 这些文本就是你想让数据库"记住"的内容
documents = [
    "苹果是一种水果，味道酸甜可口",
    "香蕉是黄色的热带水果",
    "Python 是一种编程语言"
]

# ========== 第4步：把文本转成向量（关键！）==========
# 使用本地 Embedding 模型
# 逐条转换，得到3个向量
embeddings = []
for doc in documents:
    vec = get_embedding(doc)
    embeddings.append(vec) #添加向量数组
    print(f"✅ '{doc[:15]}...' → 向量维度: {len(vec)}") #这里打印的vec的长度，多少长度代表多少维度

# ========== 第5步：把数据存入 Collection ==========
# collection.add() 的参数：
#   ids:         每条数据的唯一编号（字符串列表）
#   documents:   原始文本（字符串列表）
#   embeddings:  对应的向量（列表的列表）
#   metadatas:   额外标签信息（字典列表，可选）

collection.add(
    ids=["doc1", "doc2", "doc3"],      # 编号：doc1, doc2, doc3
    documents=documents,                # 原始文本
    embeddings=embeddings,              # 向量（从API获取的）
    metadatas=[                         # 额外信息（可选）
        {"category": "水果"},
        {"category": "水果"},
        {"category": "编程"}
    ]
)
print(f"\n✅ 成功存入 {len(documents)} 条数据到 Collection")

# ========== 第6步：语义检索 ==========
# 现在问数据库："我喜欢吃甜的水果" 和哪条最像？
query_text = "我喜欢吃甜的水果"
query_vec = get_embedding(query_text)  # 把查询也转成向量

results = collection.query(
    query_embeddings=[query_vec],       # 查询向量（列表包裹）
    n_results=2,                        # 返回最相似的2条
    include=["documents", "distances", "metadatas"]
)

# ========== 第7步：看结果 ==========
# ChromaDB 返回的 distance = 1 - 余弦相似度
# distance 越小 → 越相似
print(f"\n🔍 查询: '{query_text}'")
for i, (doc, distance, meta) in enumerate(zip(
    results["documents"][0],      # 返回的文本
    results["distances"][0],      # 返回的距离
    results["metadatas"][0]       # 返回的元数据
)):
    similarity = 1 - distance     # 距离转相似度
    print(f"  排名{i+1}: {doc}")
    print(f"    相似度: {similarity:.4f}")
    print(f"    标签: {meta}")
