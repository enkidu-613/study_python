"""本地 Embedding 模型的统一加载与编码入口。"""

from __future__ import annotations

import logging
import os
import platform
import threading # 标准库，用来创建和管理多个线程，让程序能“同时”做多件事
from typing import Any

import torch # 导入 PyTorch 库，一个深度学习计算框架
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"
DEFAULT_QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："

# 硬件只决定批量大小，不决定模型。否则建库和查询可能落入不同向量空间。
# 批量大小：对应的是模型一次并行处理多少文本，批量越大通常更快，但更占内存和显存，不影响模型名称，不影响向量维度
# 单条查询不会使用它，主要是影响批量文档编码
TIER_BATCH_SIZES = {
    "cuda_high": 64,
    "cuda_low": 16,
    "mps": 32,
    "directml": 16,
    "cpu": 8,
}

_model: SentenceTransformer | None = None
_device_info: dict[str, str] | None = None
_loaded_model_name: str | None = None
_loaded_device: str | None = None
_load_lock = threading.Lock() # 创建一个锁对象


def _try_tensor(device: Any) -> bool:
    """设备可用性探测函数，用来验证设备是否可用"""
    try:
        tensor = torch.tensor([1.0, 2.0], device=device) #1.在目标设备上创建张量
        _ = tensor * 2 #2.做一次简单张量运算
        if str(device).startswith("cuda"):
            torch.cuda.synchronize() #3，CUDA需要同步，确保指令真正执行完
        return True #4.都成功了 -> 设备可用
    except Exception as exc:
        logger.debug("device %s tensor test failed: %s", device, exc)
        return False


def _detect_device() -> dict[str, str]:
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
        if force not in tier_map: # 如果写入的值不是tier_map的任意一个，那么久返回报错
            choices = ", ".join(tier_map) #这里是拼接字符串
            raise ValueError(f"FORCE_DEVICE 必须是以下值之一: {choices}")

        _device_info = {
            "tier": tier_map[force],
            "device_str": force,
            "name": f"FORCE: {force}",
        }
        logger.info("[device] 强制指定: %s", force)
        return _device_info

    info = {"tier": "cpu", "device_str": "cpu", "name": "CPU"}

    if torch.cuda.is_available() and _try_tensor("cuda"):
        #torch.cuda.is_available() 检查 CUDA 是否可用，是PyTorch提供的方法
        try:
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            tier = "cuda_high" if vram_gb >= 6 else "cuda_low"
            info = {
                "tier": tier,
                "device_str": "cuda",
                "name": f"CUDA: {gpu_name} ({vram_gb:.1f}GB)",
            }
        except Exception as exc:
            logger.warning("CUDA info query failed: %s", exc)
            info = {
                "tier": "cuda_low",
                "device_str": "cuda",
                "name": "CUDA GPU",
            }
    elif torch.backends.mps.is_available() and _try_tensor("mps"):
        # torch.backends.mps.is_available() 检查 MPS 是否可用，是PyTorch提供的方法
        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
        info = {
            "tier": "mps",
            "device_str": "mps",
            "name": f"MPS: {platform.machine() or 'Apple Silicon'}",
        }
    elif os.name == "nt":
        # os.name == "nt" 检查当前操作系统是否为 Windows，如果系统在nt内，尝试直接使用 torch-directml
        # 因为mac和linux没有directml加速
        try:
            import torch_directml

            directml_device = torch_directml.device()
            if _try_tensor(directml_device):
                info = {
                    "tier": "directml",
                    "device_str": str(directml_device),
                    "name": f"DirectML: {directml_device}",
                }
        except ImportError:
            logger.debug("torch-directml is not installed")
        except Exception as exc:
            logger.warning("DirectML init failed: %s", exc)

    if info["tier"] == "cpu":
        logger.info("[device] fallback to CPU (%s)", platform.processor() or "unknown")
    else:
        logger.info("[device] detected: %s (tier=%s)", info["name"], info["tier"])

    _device_info = info
    return info


def _get_model_name() -> str:
    model_name = os.getenv("EMBEDDING_MODEL_NAME", DEFAULT_EMBEDDING_MODEL).strip()
    if not model_name:
        raise ValueError("EMBEDDING_MODEL_NAME 模型名称不能为空")
    return model_name


def _get_batch_size(tier: str) -> int:
    raw_value = os.getenv("EMBEDDING_BATCH_SIZE")
    if raw_value is None:
        return TIER_BATCH_SIZES[tier]

    try:
        batch_size = int(raw_value)
    except ValueError as exc:
        raise ValueError("EMBEDDING_BATCH_SIZE 必须是正整数") from exc

    if batch_size <= 0:
        raise ValueError("EMBEDDING_BATCH_SIZE 必须是正整数")
    return batch_size


def _load_model(model_name: str, device: str) -> SentenceTransformer:
    model = SentenceTransformer(model_name, device=device)
    model.encode(
        "test",
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    logger.info("[model] loaded OK, running on: %s", model.device)
    return model


def get_embedding_model() -> SentenceTransformer:
    global _model, _loaded_device, _loaded_model_name
    if _model is not None:
        # 如果模型加载过那就快速返回模型
        return _model

    with _load_lock:
        if _model is not None:
            return _model

        info = _detect_device()
        model_name = _get_model_name()
        device = info["device_str"]
        logger.info("[model] loading %s on %s", model_name, info["name"])

        try:
            model = _load_model(model_name, device)
            loaded_device = str(getattr(model, "device", device))
        except Exception as exc:
            if device == "cpu":
                raise RuntimeError(f"模型 {model_name} 在 CPU 上加载失败") from exc

            logger.warning(
                "[model] %s failed on %s: %s; retrying the same model on CPU",
                model_name,
                device,
                exc,
            )
            model = _load_model(model_name, "cpu")
            loaded_device = str(getattr(model, "device", "cpu"))

        _model = model
        _loaded_model_name = model_name
        _loaded_device = loaded_device
        return _model


def _validate_text(text: str, *, field_name: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{field_name}不能为空")
    return text.strip()


def _encode_one(text: str, *, is_query: bool) -> list[float]:
    clean_text = _validate_text(text, field_name="查询文本" if is_query else "文档文本")
    if is_query:
        instruction = os.getenv(
            "EMBEDDING_QUERY_INSTRUCTION",
            DEFAULT_QUERY_INSTRUCTION,
        )
        clean_text = f"{instruction}{clean_text}"

    model = get_embedding_model()
    return model.encode(
        clean_text,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()


def get_query_embedding(text: str) -> list[float]:
    """为检索查询生成向量；BGE 查询指令只在这里添加。"""

    return _encode_one(text, is_query=True)


def get_document_embedding(text: str) -> list[float]:
    """为单条文档生成归一化向量，保持文档原文不加查询指令。"""

    return _encode_one(text, is_query=False)


def get_document_embeddings(texts: list[str]) -> list[list[float]]:
    """批量生成文档向量。"""

    if not texts:
        return []

    clean_texts = [
        _validate_text(text, field_name=f"第 {index} 条文档文本")
        for index, text in enumerate(texts, start=1)
    ]
    model = get_embedding_model()
    tier = _detect_device()["tier"]
    return model.encode(
        clean_texts,
        batch_size=_get_batch_size(tier),
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()


def get_embedding(text: str) -> list[float]:
    """兼容旧调用；语义等同于文档向量。新代码应使用明确命名的函数。"""

    return get_document_embedding(text)


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """兼容旧调用；语义等同于批量文档向量。"""

    return get_document_embeddings(texts)


def model_info() -> dict[str, Any]:
    info = _detect_device()
    dimension = None
    if _model is not None:
        dimension = _model.get_sentence_embedding_dimension()

    return {
        "configured_model": _get_model_name(),
        "loaded_model": _loaded_model_name,
        "selected_device": info,
        "loaded_device": _loaded_device,
        "loaded": _model is not None,
        "dimension": dimension,
        "batch_size": _get_batch_size(info["tier"]),
        "normalize_embeddings": True,
        "query_instruction": os.getenv(
            "EMBEDDING_QUERY_INSTRUCTION",
            DEFAULT_QUERY_INSTRUCTION,
        ),
    }


class LocalLangChainEmbeddings(Embeddings):
    """把项目函数适配为 LangChain 的 Embeddings 接口。"""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return get_document_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        return get_query_embedding(text)


_local_lc_embeddings: LocalLangChainEmbeddings | None = None


def get_langchain_embeddings() -> LocalLangChainEmbeddings:
    global _local_lc_embeddings
    if _local_lc_embeddings is None:
        _local_lc_embeddings = LocalLangChainEmbeddings()
    return _local_lc_embeddings
