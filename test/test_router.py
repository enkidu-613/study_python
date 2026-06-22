

from importlib import import_module

from database import get_db as shared_get_db #导入同样需要被替代的get_db函数，本地重命名


todo_router_module = import_module("routers.todos_routers") #导入路由模块，而不是路由实例


def test_todo_router_uses_shared_database_dependency():
    assert todo_router_module.get_db is shared_get_db #测试路由模块现在是否使用了共享的数据库依赖项get_db


def test_docs_page_available(client):
    response = client.get("/docs")
    assert response.status_code == 200
    
# 测试todo创建接口
def test_create_todo(client):
    res = client.post("/todos", json={"title": "测试任务"})
    assert res.status_code == 200
    data = res.json()
    title = data["title"]
    assert title == "测试任务"
