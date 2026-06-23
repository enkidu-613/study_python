"""
本地 Embedding 模型统一封装

支持的硬件后端（自动检测，按优先级）:
1. CUDA      (NVIDIA GPU)
2. MPS       (Apple Silicon)
3. DirectML  (Windows AMD/Intel)
4. CPU       (兜底)
"""

import os
import platform
import logging
import threading
from typing import Optional

import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_model: Optional[SentenceTransformer] = None
_device_info: Optional[dict] = None
_load_lock = threading.Lock()

TIER_DISPATCH = {
    "cuda_high":  {"model": "BAAI/bge-large-zh-v1.5", "batch_size": 64},
    "cuda_low":   {"model": "BAAI/bge-base-zh-v1.5",  "batch_size": 16},
    "mps":        {"model": "BAAI/bge-base-zh-v1.5",  "batch_size": 32},
    "directml":   {"model": "BAAI/bge-base-zh-v1.5",  "batch_size": 16},
    "cpu":        {"model": "BAAI/bge-small-zh-v1.5", "batch_size": 8},
}


def _try_tensor(device_str: str) -> bool:
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
    global _device_info
    if _device_info is not None:
        return _device_info

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

    elif torch.backends.mps.is_available() and _try_tensor("mps"):
        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
        chip = platform.machine() or "Apple Silicon"
        info = {
            "tier": "mps",
            "device_str": "mps",
            "name": f"MPS: {chip}",
        }

    elif os.name == "nt":
        try:
            import torch_directml
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

    if info["tier"] == "cpu":
        logger.info(f"[device] fallback to CPU ({platform.processor() or 'unknown'})")
    else:
        logger.info(f"[device] detected: {info['name']} (tier={info['tier']})")

    _device_info = info
    return info


def _get_model_name(tier: str) -> str:
    return os.getenv("EMBEDDING_MODEL_NAME") or TIER_DISPATCH[tier]["model"]


def _get_batch_size(tier: str) -> int:
    env = os.getenv("EMBEDDING_BATCH_SIZE")
    return int(env) if env else TIER_DISPATCH[tier]["batch_size"]


def _load_model(model_name: str, device: str) -> SentenceTransformer:
    model = SentenceTransformer(model_name, device=device)
    actual = str(model.device)

    if device != "cpu" and device not in actual:
        logger.warning(f"loaded on {actual} (expected {device}), fallback to CPU")
        model = SentenceTransformer(model_name, device="cpu")
        actual = "cpu"

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
    global _model
    if _model is not None:
        return _model

    with _load_lock:
        if _model is not None:
            return _model

        info = _detect_device()
        model_name = _get_model_name(info["tier"])
        device = info["device_str"]

        logger.info(f"[model] loading {model_name} on {info['name']}")

        try:
            _model = _load_model(model_name, device)
        except (RuntimeError, torch.OutOfMemoryError) as e:
            logger.error(f"load on {device} failed: {e}")
            if info["tier"] != "cpu":
                fallback_model = TIER_DISPATCH["cpu"]["model"]
                logger.warning(f"fallback to CPU model: {fallback_model}")
                _model = _load_model(fallback_model, "cpu")
            else:
                raise
        except Exception as e:
            logger.error(f"load on {device} failed: {e}")
            logger.warning("fallback to CPU")
            _model = _load_model(model_name, "cpu")

        return _model


def get_embedding(text: str) -> list[float]:
    model = get_embedding_model()
    return model.encode(text, convert_to_numpy=True).tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    bs = _get_batch_size(_device_info["tier"])
    return model.encode(texts, batch_size=bs, convert_to_numpy=True).tolist()


def model_info() -> dict:
    info = _detect_device()
    return {
        "device": info,
        "model_name": _get_model_name(info["tier"]) if _model is None else str(_model),
        "loaded": _model is not None,
        "batch_size": _get_batch_size(info["tier"]),
    }


from langchain_core.embeddings import Embeddings


class LocalLangChainEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return get_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        return get_embedding(text)


_local_lc_embeddings = None


def get_langchain_embeddings() -> "LocalLangChainEmbeddings":
    global _local_lc_embeddings
    if _local_lc_embeddings is None:
        _local_lc_embeddings = LocalLangChainEmbeddings()
    return _local_lc_embeddings
