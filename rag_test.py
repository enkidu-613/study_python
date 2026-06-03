import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

# ModelScope API 配置（使用 OpenAI 兼容接口）
MODELSCOPE_API_KEY = os.getenv("MODELSCOPE_API_KEY")

MODEL_API_URL = os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1")

client = OpenAI(
    base_url=MODEL_API_URL,
    api_key=MODELSCOPE_API_KEY
)

def get_embedding(text: str) -> list[float]:
    """
    将文本转换为向量（Embedding）- 使用 ModelScope API (Qwen3-Embedding-8B)
    
    数学原理：
    ┌─────────────────────────────────────────────────────────────┐
    │  Text → [Tokenization] → [Neural Network] → Vector(多维)   │
    └─────────────────────────────────────────────────────────────┘
    
    本质：神经网络将语义编码为高维空间中的坐标点
    - 语义相近的文本 → 空间中距离相近的点
    - 语义不同的文本 → 空间中距离遥远的点
    """
    response = client.embeddings.create(
        model="Qwen/Qwen3-Embedding-8B",
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding

# ========== 测试 ==========
text1 = "如何提升代码质量"
text2 = "提高程序可维护性的方法"  
text3 = "今天天气真好"

vec1 = get_embedding(text1)
vec2 = get_embedding(text2)
vec3 = get_embedding(text3)

def cosine_similarity(a, b):
    """
    计算余弦相似度 - 衡量两个向量的方向接近程度
    
    ┌─────────────────────────────────────────────────────────────────┐
    │                        数学公式                                  │
    │                                                                 │
    │         A · B          Σ(aᵢ × bᵢ)                              │
    │  cos(θ) = ─────  =  ────────────────────────                    │
    │         ||A|| × ||B||    √(Σaᵢ²) × √(Σbᵢ²)                    │
    │                                                                 │
    │  其中:                                                          │
    │  • A · B = 向量点积（对应元素相乘后求和）                         │
    │  • ||A|| = 向量A的L2范数 = √(a₁² + a₂² + ... + aₙ²)            │
    │  • ||B|| = 向量B的L2范数 = √(b₁² + b₂² + ... + bₙ²)            │
    └─────────────────────────────────────────────────────────────────┘
    
    几何意义：
    • cos(θ) = 1  → 两个向量方向完全相同（最相似）
    • cos(θ) = 0  → 两个向量正交（无关联）
    • cos(θ) = -1 → 两个向量方向相反（最不相似）
    
    取值范围: [-1, 1]，越接近1表示越相似
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"句子1 vs 句子2: {cosine_similarity(vec1, vec2):.4f}")  # 应该很高 (~0.8)
print(f"句子1 vs 句子3: {cosine_similarity(vec1, vec3):.4f}")  # 应该很低 (~0.2)