from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from app import embedding


class FakeArray:
    def __init__(self, value: list[float] | list[list[float]]):
        self.value = value

    def tolist(self):
        return self.value


@dataclass
class FakeModel:
    calls: list[dict[str, Any]] = field(default_factory=list)

    def encode(self, texts, **kwargs):
        self.calls.append({"texts": texts, **kwargs})
        if isinstance(texts, list):
            return FakeArray([[0.1, 0.2] for _ in texts])
        return FakeArray([0.1, 0.2])


@pytest.fixture(autouse=True)
def reset_embedding_state(monkeypatch):
    monkeypatch.setattr(embedding, "_model", None)
    monkeypatch.setattr(embedding, "_device_info", None)
    monkeypatch.setattr(embedding, "_loaded_model_name", None, raising=False)
    monkeypatch.setattr(embedding, "_loaded_device", None, raising=False)
    monkeypatch.delenv("EMBEDDING_BATCH_SIZE", raising=False)


def test_query_embedding_adds_instruction_and_normalizes(monkeypatch):
    model = FakeModel()
    monkeypatch.setattr(embedding, "get_embedding_model", lambda: model)

    result = embedding.get_query_embedding("退款需要几天内申请？")

    assert result == [0.1, 0.2]
    assert model.calls == [
        {
            "texts": "为这个句子生成表示以用于检索相关文章：退款需要几天内申请？",
            "convert_to_numpy": True,
            "normalize_embeddings": True,
        }
    ]


def test_document_embeddings_keep_original_text_and_normalize(monkeypatch):
    model = FakeModel()
    monkeypatch.setattr(embedding, "get_embedding_model", lambda: model)
    monkeypatch.setattr(
        embedding,
        "_detect_device",
        lambda: {"tier": "cpu", "device_str": "cpu", "name": "CPU"},
    )

    result = embedding.get_document_embeddings(["第一段", "第二段"])

    assert result == [[0.1, 0.2], [0.1, 0.2]]
    assert model.calls == [
        {
            "texts": ["第一段", "第二段"],
            "batch_size": 8,
            "convert_to_numpy": True,
            "normalize_embeddings": True,
        }
    ]


def test_empty_document_batch_returns_without_loading_model(monkeypatch):
    monkeypatch.setattr(
        embedding,
        "get_embedding_model",
        lambda: pytest.fail("empty batch must not load the model"),
    )

    assert embedding.get_document_embeddings([]) == []


def test_blank_query_is_rejected():
    with pytest.raises(ValueError, match="不能为空"):
        embedding.get_query_embedding("   ")


def test_invalid_batch_size_has_clear_error(monkeypatch):
    monkeypatch.setenv("EMBEDDING_BATCH_SIZE", "0")

    with pytest.raises(ValueError, match="正整数"):
        embedding._get_batch_size("cpu")


def test_blank_model_name_has_clear_error(monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL_NAME", "   ")

    with pytest.raises(ValueError, match="模型名称不能为空"):
        embedding._get_model_name()


def test_accelerator_failure_retries_same_model_on_cpu(monkeypatch):
    attempts: list[tuple[str, str]] = []
    expected_model = FakeModel()
    monkeypatch.setenv("EMBEDDING_MODEL_NAME", "example/fixed-model")

    monkeypatch.setattr(
        embedding,
        "_detect_device",
        lambda: {"tier": "mps", "device_str": "mps", "name": "MPS: arm64"},
    )

    def fake_load_model(model_name: str, device: str):
        attempts.append((model_name, device))
        if device == "mps":
            raise RuntimeError("MPS unavailable")
        return expected_model

    monkeypatch.setattr(embedding, "_load_model", fake_load_model)

    assert embedding.get_embedding_model() is expected_model
    assert attempts == [
        ("example/fixed-model", "mps"),
        ("example/fixed-model", "cpu"),
    ]
