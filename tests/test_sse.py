from importlib import import_module

ai_router_module = import_module("app.routers.ai")


def test_ai_router_format(client, monkeypatch):
    async def fake_generate_stream(message: str):
        yield ('data:{"type":"answer","content":"这是一个模拟回答"}\n\n')

    monkeypatch.setattr(ai_router_module, "generate_stream", fake_generate_stream)

    with client.stream("POST","/ai/chat",json={"message":"测试sse"})as response:
        body = response.read().decode('utf-8')
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        assert body == 'data:{"type":"answer","content":"这是一个模拟回答"}\n\n'
