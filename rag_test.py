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

# ========== 测试 ==========
text1 = "如何提升代码质量"
text2 = "提高程序可维护性的方法"  
text3 = "今天天气真好"

vec1 = get_embedding(text1)
vec2 = get_embedding(text2)
vec3 = get_embedding(text3)

# 计算余弦相似度
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"句子1 vs 句子2: {cosine_similarity(vec1, vec2):.4f}")  # 应该很高 (~0.8)
print(f"句子1 vs 句子3: {cosine_similarity(vec1, vec3):.4f}")  # 应该很低 (~0.2)