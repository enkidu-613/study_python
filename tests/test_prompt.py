from importlib import import_module

prompt_router_module = import_module("app.routers.prompt")


def test_extract_task_returns_structured_result(client, monkeypatch):
    async def fake_extract_task_from_text(text: str):
        assert text == "明天下午提交项目报告，这是高优先级工作"
        return prompt_router_module.TaskExtractionResult(
            title="提交项目报告",
            priority="high",
            tags=["工作", "报告"],
        )

    monkeypatch.setattr(
        prompt_router_module,
        "extract_task_from_text",
        fake_extract_task_from_text,
    )

    response = client.post(
        "/prompt-advanced/extract-task",
        json={"text": "明天下午提交项目报告，这是高优先级工作"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "提交项目报告",
        "priority": "high",
        "tags": ["工作", "报告"],
    }


def test_extract_task_hides_model_failure(client, monkeypatch):
    async def fake_extract_task_from_text(text: str):
        raise RuntimeError("provider leaked internal details")

    monkeypatch.setattr(
        prompt_router_module,
        "extract_task_from_text",
        fake_extract_task_from_text,
    )

    response = client.post(
        "/prompt-advanced/extract-task",
        json={"text": "整理会议纪要"},
    )

    assert response.status_code == 502
    assert response.json() == {"detail": "结构化输出生成失败"}
    assert "provider leaked" not in response.text


def test_prompt_advanced_route_appears_in_openapi(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/prompt-advanced/extract-task" in response.json()["paths"]


def test_build_task_extractor_requires_api_key(monkeypatch):
    import pytest

    monkeypatch.delenv("MODELSCOPE_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="MODELSCOPE_API_KEY 未配置"):
        prompt_router_module.build_task_extractor()
