"""
本地 Embedding 模型统一封装（优化版）

============================

支持的硬件后端（自动检测，按优先级）:
1. CUDA      (NVIDIA GPU)        — torch.cuda
2. MPS       (Apple Silicon)       — torch.backends.mps
3. DirectML  (Windows AMD/Intel)  — torch-directml
4. CPU       (兜底)

特性:
- 线程安全单例加载（防止并发请求重复加载模型）
- 设备自动探测 + 实际张量测试
- 按设备能力自动选模型规模 / batch size
- 加载失败按 tier 降级（OOM 时大模型→小模型）
- 加载后 dummy inference 验证，避免"能加载但推理报错"
- 全部可通过环境变量覆盖
"""

import os
import platform
import logging
import threading
from typing import Optional

import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# 全局缓存
_model: Optional[SentenceTransformer] = None
_device_info: Optional[dict] = None
_load_lock = threading.Lock()  # 防止并发重复加载

# 设备能力档位 → 模型 / batch size 调度表
# 注：量化需额外依赖（optimum/bitsandbytes），这里预留配置但不自动启用
TIER_DISPATCH = {
    "cuda_high":  {"model": "BAAI/bge-large-zh-v1.5", "batch_size": 64},
    "cuda_low":   {"model": "BAAI/bge-base-zh-v1.5",  "batch_size": 16},
    "mps":        {"model": "BAAI/bge-base-zh-v1.5",  "batch_size": 32},
    "directml":   {"model": "BAAI/bge-base-zh-v1.5",  "batch_size": 16},
    "cpu":        {"model": "BAAI/bge-small-zh-v1.5", "batch_size": 8},
}


def _try_tensor(device_str: str) -> bool:
    """实际跑一个张量，验证设备真的能用"""
    try:
        t = torch.tensor([1.0, 2.0], device=device_str)
        _ = t * 2
        if device_str == "cuda":
            torch.cuda.synchronize()
        return True
    except Exception as e:
        logger.debug(f"device {device_str} tensor test failed: {e}")
        return False


def _detect_device() -> dict:
    """
    探测最优设备，返回 {tier, device_str, name}
    支持 FORCE_DEVICE 环境变量强制指定
    """
    global _device_info
    if _device_info is not None:
        return _device_info

    # 环境变量强制覆盖
    force = os.getenv("FORCE_DEVICE")
    if force:
        tier_map = {
            "cuda": "cuda_high",
            "mps": "mps",
            "directml": "directml",
            "cpu": "cpu",
        }
        tier = tier_map.get(force, "cpu")
        _device_info = {
            "tier": tier,
            "device_str": force,
            "name": f"FORCE: {force}",
        }
        logger.info(f"[device] 强制指定: {force}")
        return _device_info

    info = {"tier": "cpu", "device_str": "cpu", "name": "CPU"}

    # 1. CUDA
    if torch.cuda.is_available() and _try_tensor("cuda"):
        try:
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            tier = "cuda_high" if vram_gb >= 6 else "cuda_low"
            info = {
                "tier": tier,
                "device_str": "cuda",
                "name": f"CUDA: {gpu_name} ({vram_gb:.1f}GB)",
            }
        except Exception as e:
            logger.warning(f"CUDA info query failed: {e}")
            info = {"tier": "cuda_low", "device_str": "cuda", "name": "CUDA GPU"}

    # 2. MPS（Apple Silicon）
    elif torch.backends.mps.is_available() and _try_tensor("mps"):
        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
        chip = platform.machine() or "Apple Silicon"
        info = {
            "tier": "mps",
            "device_str": "mps",
            "name": f"MPS: {chip}",
        }

    # 3. DirectML（Windows 非 NVIDIA GPU）
    elif os.name == "nt":
        try:
            import torch_directml  # type: ignore
            dml = torch_directml.device()
            if _try_tensor(dml):
                info = {
                    "tier": "directml",
                    "device_str": str(dml),
                    "name": f"DirectML: {dml}",
                }
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"DirectML init failed: {e}")

    # 4. CPU 兜底
    if info["tier"] == "cpu":
        logger.info(f"[device] fallback to CPU ({platform.processor() or 'unknown'})")
    else:
        logger.info(f"[device] detected: {info['name']} (tier={info['tier']})")

    _device_info = info
    return info


def _get_model_name(tier: str) -> str:
    """环境变量优先，否则按档位选"""
    return os.getenv("EMBEDDING_MODEL_NAME") or TIER_DISPATCH[tier]["model"]


def _get_batch_size(tier: str) -> int:
    """环境变量优先，否则按档位选"""
    env = os.getenv("EMBEDDING_BATCH_SIZE")
    return int(env) if env else TIER_DISPATCH[tier]["batch_size"]


def _load_model(model_name: str, device: str) -> SentenceTransformer:
    """加载模型，带验证"""
    model = SentenceTransformer(model_name, device=device)
    actual = str(model.device)

    # 声称用 GPU 但实际没上去，回退 CPU
    if device != "cpu" and device not in actual:
        logger.warning(f"loaded on {actual} (expected {device}), fallback to CPU")
        model = SentenceTransformer(model_name, device="cpu")
        actual = "cpu"

    # dummy inference 验证：避免"能加载但推理报错"
    try:
        _ = model.encode("test", convert_to_numpy=True)
        logger.info(f"[model] loaded OK, running on: {actual}")
    except Exception as e:
        if actual != "cpu":
            logger.warning(f"dummy inference failed on {actual}: {e}, fallback to CPU")
            model = SentenceTransformer(model_name, device="cpu")
            _ = model.encode("test", convert_to_numpy=True)
            logger.info("[model] loaded OK on CPU")
        else:
            raise RuntimeError(f"模型在 CPU 上也无法推理: {e}")

    return model


def get_embedding_model() -> SentenceTransformer:
    """
    获取（或创建）本地 Embedding 模型（线程安全单例）
    """
    global _model
    if _model is not None:
        return _model

    with _load_lock:  # 防止并发重复加载
        if _model is not None:  # 双重检查
            return _model

        info = _detect_device()
        model_name = _get_model_name(info["tier"])
        device = info["device_str"]

        logger.info(f"[model] loading {model_name} on {info['name']}")

        try:
            _model = _load_model(model_name, device)
        except (RuntimeError, torch.OutOfMemoryError) as e:
            # OOM 时按 CPU tier 降级（大模型→小模型）
            logger.error(f"load on {device} failed: {e}")
            if info["tier"] != "cpu":
                fallback_model = TIER_DISPATCH["cpu"]["model"]
                logger.warning(f"fallback to CPU model: {fallback_model}")
                _model = _load_model(fallback_model, "cpu")
            else:
                raise
        except Exception as e:
            # 其他错误直接回退 CPU 同模型
            logger.error(f"load on {device} failed: {e}")
            logger.warning("fallback to CPU")
            _model = _load_model(model_name, "cpu")

        return _model


def get_embedding(text: str) -> list[float]:
    """单条文本 → 向量"""
    model = get_embedding_model()
    return model.encode(text, convert_to_numpy=True).tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """批量文本 → 向量列表（自动按设备能力选 batch_size）"""
    model = get_embedding_model()
    bs = _get_batch_size(_device_info["tier"])
    return model.encode(texts, batch_size=bs, convert_to_numpy=True).tolist()


def model_info() -> dict:
    """当前模型状态（挂到 /health 用）"""
    info = _detect_device()
    return {
        "device": info,
        "model_name": _get_model_name(info["tier"]) if _model is None else str(_model),
        "loaded": _model is not None,
        "batch_size": _get_batch_size(info["tier"]),
    }


# ---------- LangChain 兼容封装 ----------
from langchain_core.embeddings import Embeddings


class LocalLangChainEmbeddings(Embeddings):
    """把 local_embedding 的 SentenceTransformer 包装成 LangChain Embeddings 接口"""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return get_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        return get_embedding(text)


_local_lc_embeddings = None


def get_langchain_embeddings() -> "LocalLangChainEmbeddings":
    """惰性获取 LangChain 兼容的 Embedding 实例（底层复用 local_embedding 单例）"""
    global _local_lc_embeddings
    if _local_lc_embeddings is None:
        _local_lc_embeddings = LocalLangChainEmbeddings()
    return _local_lc_embeddings


# ---------- 自检 ----------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("设备自检")
    print("=" * 60)
    print(_detect_device())
    print()
    print("=" * 60)
    print("加载并跑一次推理")
    print("=" * 60)
    vecs = get_embeddings(["你好,世界", "本地 Embedding 测试"])
    print(f"output dim: {len(vecs[0])}")
    print(f"first 5 dims: {vecs[0][:5]}")
    print()
    print("=" * 60)
    print("model_info")
    print("=" * 60)
    print(model_info()) 