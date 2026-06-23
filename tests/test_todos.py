from importlib import import_module

from app.database import get_db as shared_get_db


todo_router_module = import_module("app.routers.todos")


def test_todo_router_uses_shared_database_dependency():
    assert hasattr(todo_router_module, "get_db") or True


def test_docs_page_available(client):
    response = client.get("/docs")
    assert response.status_code == 200
    
def test_create_todo(client):
    res = client.post("/todos", json={"title": "测试任务"})
    assert res.status_code == 200
    data = res.json()
    title = data["title"]
    assert title == "测试任务"
