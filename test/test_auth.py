from importlib import import_module
from database import get_db as shared_get_db

auth_router_module = import_module("routers.auth_router")

def test_auth_router_uses_shared_database_dependency():
    assert auth_router_module.get_db is shared_get_db
    #测试路由模块现在是否使用了共享的数据库依赖项get_db

def test_login_then_get_current_user(client):
    client.post("/auth/register",json={"username":"testuser","password":"testpassword"})
    login_response = client.post("/auth/login",json={"username":"testuser","password":"testpassword"})
    token = login_response.json()["access_token"]
    me_response = client.get("/auth/me",headers={"Authorization":f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "testuser"

