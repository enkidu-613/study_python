import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://api-inference.modelscope.cn/v1",
    api_key=os.getenv("MODELSCOPE_API_KEY")
)

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="Qwen/Qwen3-Embedding-8B",
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ============================================================
#  实验1：看一个文本的向量长什么样（只显示前10个）
# ============================================================
print("=" * 60)
print("实验1：文本 → 向量长什么样？")
print("=" * 60)

text = "苹果是一种水果"
vec = get_embedding(text)

print(f"文本: '{text}'")
print(f"向量维度: {len(vec)}")
print(f"前10个数字: {[round(v, 4) for v in vec[:10]]}")
print(f"向量统计: 均值={np.mean(vec):.6f}, 最小值={np.min(vec):.4f}, 最大值={np.max(vec):.4f}")

# ============================================================
#  实验2：比较语义相近的文本
# ============================================================
print(f"\n{'=' * 60}")
print("实验2：相近语义 vs 不同语义")
print("=" * 60)

pairs = [
    ("苹果很好吃", "我喜欢吃苹果",       "都关于苹果"),
    ("苹果很好吃", "香蕉也很好吃",       "不同水果"),
    ("苹果很好吃", "Python 编程语言",    "完全不相关"),
]

base_text = "苹果很好吃"
base_vec = get_embedding(base_text)

for text, expected in [("我喜欢吃苹果", "都关于苹果"), ("香蕉也很好吃", "不同水果"), ("Python 编程语言", "完全不相关")]:
    vec2 = get_embedding(text)
    sim = cosine_similarity(base_vec, vec2)
    print(f"  '{base_text}' vs '{text}'")
    print(f"  → 相似度: {sim:.4f}  ({expected})")
    print()

# ============================================================
#  实验3：同一个词，不同上下文
# ============================================================
print("=" * 60)
print("实验3：多义词 — 同一个词在不同上下文中的向量")
print("=" * 60)

contexts = [
    "Python 是一种编程语言",
    "Python 是一种大蟒蛇",
    "我用 Python 写了一个网页",
    "动物园里有一条 python",
]

for text in contexts:
    vec = get_embedding(text)
    print(f"  '{text}'")
    print(f"  → 前5维: {[round(v, 4) for v in vec[:5]]}")
    print()

# 计算两两之间的相似度
print("  相似度矩阵:")
vecs = [get_embedding(t) for t in contexts]
labels = ["编程1", "蛇1", "编程2", "蛇2"]
for i in range(len(contexts)):
    for j in range(i+1, len(contexts)):
        sim = cosine_similarity(vecs[i], vecs[j])
        print(f"    '{labels[i]}' vs '{labels[j]}': {sim:.4f}")

# ============================================================
#  实验4：中英文混合
# ============================================================
print(f"\n{'=' * 60}")
print("实验4：跨语言 — 中英文语义是否接近？")
print("=" * 60)

cross_pairs = [
    ("苹果", "apple"),
    ("香蕉", "banana"),
    ("编程", "programming"),
    ("苹果", "banana"),
    ("编程", "apple"),
]

for cn, en in cross_pairs:
    sim = cosine_similarity(get_embedding(cn), get_embedding(en))
    bar = "█" * int(sim * 20)
    print(f"  '{cn}' vs '{en}': {sim:.4f} {bar}")