"""
本地 Embedding 模型封装
=======================
使用 sentence-transformers 本地运行，无需外部 API。
模型通过环境变量 EMBEDDING_MODEL_NAME 配置。
"""

from sentence_transformers import SentenceTransformer
import os

# 全局缓存，避免重复加载模型
_model = None


def get_embedding_model():
    """获取（或创建）本地 Embedding 模型（单例）"""
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-zh-v1.5")
        print(f"[本地 Embedding] 加载模型: {model_name}")
        _model = SentenceTransformer(model_name)
    return _model


def get_embedding(text: str) -> list[float]:
    """将文本转为向量"""
    model = get_embedding_model()
    return model.encode(text).tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """批量将文本转为向量"""
    model = get_embedding_model()
    return model.encode(texts).tolist()
