"""
本地 Embedding 模型封装
=======================
使用 sentence-transformers 本地运行，支持 MPS（Metal）硬件加速。
模型通过环境变量 EMBEDDING_MODEL_NAME 配置。
"""

from sentence_transformers import SentenceTransformer
import os

# 全局缓存，避免重复加载模型
_model = None
_device = None  # 缓存当前使用的设备


def _get_optimal_device() -> str:
    """
    检测并返回最优设备（MPS > CPU）。

    - MPS（Metal Performance Shaders）：Apple Silicon（M 系列芯片）的 GPU 加速
    - CPU：通用兜底方案

    首次调用会缓存结果，避免重复检测。
    """
    global _device
    if _device is not None:
        return _device

    try:
        import torch
        if torch.backends.mps.is_available():
            # 额外检查 MPS 是否兼容（某些 PyTorch 版本 MPS 可用但有 bug）
            try:
                # 用一个极小张量测试 MPS 是否真的能跑
                _ = torch.tensor([1.0, 2.0], device="mps")
                _device = "mps"
                print("[本地 Embedding] 设备检测: MPS ✅（Metal GPU 加速已启用）")
            except Exception:
                _device = "cpu"
                print("[本地 Embedding] 设备检测: MPS 可用但测试失败，回退到 CPU ⚠️")
        else:
            _device = "cpu"
            print("[本地 Embedding] 设备检测: MPS 不可用，使用 CPU 🖥️")
    except ImportError:
        _device = "cpu"
        print("[本地 Embedding] 设备检测: PyTorch 未安装，使用 CPU 🖥️")

    return _device


def get_embedding_model():
    """
    获取（或创建）本地 Embedding 模型（单例）。

    自动选择最优设备：
    - Apple Silicon: MPS GPU 加速
    - 其他 / 兼容性问题: CPU 兜底
    """
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-zh-v1.5")
        device = _get_optimal_device()

        print(f"[本地 Embedding] 加载模型: {model_name}")

        # 尝试用 MPS 加载，失败则回退到 CPU
        try:
            _model = SentenceTransformer(model_name, device=device)
            # 验证设备正确
            actual_device = str(_model.device)
            if device == "mps" and "mps" not in actual_device:
                print(f"[本地 Embedding] MPS 加载失败（实际设备: {actual_device}），回退到 CPU")
                _model = SentenceTransformer(model_name, device="cpu")
            else:
                print(f"[本地 Embedding] 模型已加载，运行在: {actual_device}")
        except Exception as e:
            print(f"[本地 Embedding] 使用 {device} 加载失败: {e}")
            print("[本地 Embedding] 回退到 CPU")
            _model = SentenceTransformer(model_name, device="cpu")
            print(f"[本地 Embedding] 模型已加载，运行在: cpu")

    return _model


def get_embedding(text: str) -> list[float]:
    """将文本转为向量（自动使用最优设备加速）"""
    model = get_embedding_model()
    return model.encode(text).tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """批量将文本转为向量"""
    model = get_embedding_model()
    return model.encode(texts).tolist()
