from importlib import import_module
from database import get_db as shared_get_db

rag_router_module = import_module("routers.langchain_rag_router")

def test_rag_router_uses_shared_database_dependency():
    assert rag_router_module.get_db is shared_get_db
    #测试路由模块现在是否使用了共享的数据库依赖项get_db

# 测试流程 从存入 到 语义检索 到流式问答
