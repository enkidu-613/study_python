import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db
from models import Base

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture() # 这是一个装饰器，他告诉pytest：这不是一个client不是普通的测试函数，而是给测试准备资源的函数，需要这个函数的测试开始之前，请先执行这个函数
def client():
    Base.metadata.create_all(bind=test_engine) # 创建测试数据库表
    app.dependency_overrides[get_db] = override_get_db # dependency_overrides 本质是上是一个字典，这个告诉FastAPI：在测试中，get_db依赖项应该使用override_get_db函数代替
    with TestClient(app) as test_client: # with 打开资源用完后关闭 TestClient(app) 创建一个能直接请求FastAPI应用的客户端
        yield test_client # 返回客户端实例交给测试函数，然后暂停执行，等待测试函数执行完毕
    app.dependency_overrides.clear() # 清除依赖项覆盖，恢复默认行为
    Base.metadata.drop_all(bind=test_engine) #删除测试数据库表
