"""
RAG 入门第一步：理解 Embedding
把文本变成向量，计算相似度
"""

import numpy as np

# ========== 第1步：理解什么是向量 ==========

# 文本本身计算机无法理解，需要转成数字
# "你好" → [0.1, 0.2, 0.3, ...] (很多个浮点数)

# 模拟两个句子的向量（实际要用模型生成）
# 这里用简化版让你理解概念

sentence_a = "如何提升代码质量"
sentence_b = "提高程序可维护性的方法"
sentence_c = "今天天气真好"

# 模拟向量（实际有 768/1024/1536 维，这里用 5 维演示）
vec_a = np.array([0.9, 0.8, 0.7, 0.1, 0.2])   # "代码质量"相关
vec_b = np.array([0.85, 0.75, 0.65, 0.15, 0.25])  # "程序维护"相关（和A很像）
vec_c = np.array([0.1, 0.2, 0.1, 0.9, 0.8])   # "天气"相关（和A、B都不一样）

print("=" * 50)
print("🎯 RAG 入门：文本相似度计算")
print("=" * 50)

print(f"\n句子A: {sentence_a}")
print(f"向量A: {vec_a}")

print(f"\n句子B: {sentence_b}")
print(f"向量B: {vec_b}")

print(f"\n句子C: {sentence_c}")
print(f"向量C: {vec_c}")

# ========== 第2步：计算余弦相似度 ==========

def cosine_similarity(a, b):
    """
    余弦相似度：计算两个向量的夹角
    1.0 = 完全相同
    0.0 = 完全无关
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

sim_ab = cosine_similarity(vec_a, vec_b)
sim_ac = cosine_similarity(vec_a, vec_c)
sim_bc = cosine_similarity(vec_b, vec_c)

print("\n" + "=" * 50)
print("📊 相似度计算结果")
print("=" * 50)

print(f"\nA vs B ('代码质量' vs '程序维护'):")
print(f"   相似度: {sim_ab:.3f} 🔥 非常相似！")

print(f"\nA vs C ('代码质量' vs '天气很好'):")
print(f"   相似度: {sim_ac:.3f} ❌ 不相似")

print(f"\nB vs C ('程序维护' vs '天气很好'):")
print(f"   相似度: {sim_bc:.3f} ❌ 不相似")

# ========== 第3步：理解语义搜索原理 ==========

print("\n" + "=" * 50)
print("🔍 语义搜索 vs 关键字搜索")
print("=" * 50)

print("""
用户搜索: "编程语言入门"

数据库内容:
  1. "Python 基础教程" 
  2. "Java 高级特性"
  3. "今天天气不错"

❌ SQL LIKE 搜索:
   SELECT * WHERE content LIKE '%编程语言入门%'
   → 找不到任何结果！（因为没有完全匹配的文字）

✅ 向量语义搜索:
   "编程语言入门" → [0.8, 0.7, 0.9, ...]
   "Python 基础教程" → [0.75, 0.65, 0.85, ...]  ← 相似度 0.92
   "Java 高级特性" → [0.70, 0.60, 0.80, ...]    ← 相似度 0.85
   "今天天气不错" → [0.1, 0.2, 0.1, ...]        ← 相似度 0.15
   
   → 返回前2条！语义相关，即使文字不完全匹配
""")

# ========== 第4步：实际用 ChromaDB 演示 ==========

print("=" * 50)
print("🗄️ ChromaDB 实战：真正的向量数据库")
print("=" * 50)

try:
    import chromadb
    
    # 创建客户端
    client = chromadb.Client()
    
    # 创建集合（类似 SQLAlchemy 的 Table）
    collection = client.create_collection(name="demo")
    
    # 添加文档（Chroma 自动做 Embedding）
    collection.add(
        documents=[
            "Python 是一种高级编程语言，语法简洁优雅",
            "FastAPI 是一个现代 Python Web 框架，性能极高",
            "SQLAlchemy 是 Python 的 ORM 工具，简化数据库操作",
            "Docker 是容器化平台，便于部署应用",
            "机器学习是人工智能的一个分支，让计算机从数据中学习",
        ],
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"],
        metadatas=[
            {"category": "语言"},
            {"category": "框架"},
            {"category": "数据库"},
            {"category": "运维"},
            {"category": "AI"},
        ]
    )
    
    print("\n✅ 已存入 5 段文档")
    
    # 语义检索
    query = "我想学 Python"
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    print(f"\n🔍 查询: '{query}'")
    print("\n最相似的 3 条结果:")
    for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
        print(f"  {i+1}. {doc}")
        print(f"     距离: {distance:.3f} (越小越相似)")
    
    # 再试一个查询
    query2 = "怎么部署应用"
    results2 = collection.query(
        query_texts=[query2],
        n_results=2
    )
    
    print(f"\n🔍 查询: '{query2}'")
    print("\n最相似的 2 条结果:")
    for i, (doc, distance) in enumerate(zip(results2['documents'][0], results2['distances'][0])):
        print(f"  {i+1}. {doc}")
        print(f"     距离: {distance:.3f}")

except Exception as e:
    print(f"\n⚠️ ChromaDB 演示出错: {e}")
    print("但这不影响你理解核心概念！")

print("\n" + "=" * 50)
print("🎉 总结")
print("=" * 50)
print("""
你刚才学到了:

1. Embedding: 文本 → 向量（一串数字）
2. 余弦相似度: 计算两个向量的相似程度
3. 语义搜索: 找"意思相近"的，不是"文字相同"的
4. ChromaDB: 专门存向量、做相似度搜索的数据库

下一步: 用真实的 Embedding 模型（OpenAI/ModelScope）生成向量
""")
