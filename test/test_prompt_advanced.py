from importlib import import_module

prompt_router_module = import_module("routers.prompt_advanced_router")


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
