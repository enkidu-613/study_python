from pydantic import SecretStr

import app.multimodal_vision_demo as vision


class FakeChatOpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def test_minimax_uses_explicit_vision_configuration(monkeypatch):
    monkeypatch.setenv("VISION_MODEL_NAME", "minimax/minimax-example")
    monkeypatch.setenv("VISION_API_KEY", "vision-key")
    monkeypatch.setenv("VISION_API_BASE", "https://openrouter.example/v1")
    monkeypatch.setattr(vision, "ChatOpenAI", FakeChatOpenAI)

    model = vision.build_vision_llm()

    assert model.kwargs["model"] == "minimax/minimax-example"
    assert model.kwargs["base_url"] == "https://openrouter.example/v1"
    assert isinstance(model.kwargs["api_key"], SecretStr)
    assert model.kwargs["api_key"].get_secret_value() == "vision-key"


def test_explicit_vision_endpoint_is_used_for_any_model(monkeypatch):
    monkeypatch.setenv("VISION_MODEL_NAME", "google/gemini-example")
    monkeypatch.setenv("VISION_API_KEY", "custom-key")
    monkeypatch.setenv("VISION_API_BASE", "https://vision.example/v1")
    monkeypatch.setattr(vision, "ChatOpenAI", FakeChatOpenAI)

    model = vision.build_vision_llm()

    assert model.kwargs["base_url"] == "https://vision.example/v1"
    assert model.kwargs["api_key"].get_secret_value() == "custom-key"
