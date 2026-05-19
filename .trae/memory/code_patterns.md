# 代码模式与模板

## FastAPI 分层架构模板

### 1. database.py (数据层)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./my_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### 2. models.py (模型层)
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()

class DBTodo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)
```

### 3. routers.py (业务层)
```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import DBTodo

router = APIRouter(prefix="/todos", tags=["Todos"])

class TodoItem(BaseModel):
    title: str
    is_done: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD 路由...
```

### 4. main.py (表现层)
```python
from fastapi import FastAPI
import uvicorn
from routers import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## 常用代码片段

### 依赖注入模板
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Model).all()
```

### CRUD 完整模板
```python
# Create
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    db_item = Model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Read All
@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Model).all()

# Read One
@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Model).filter(Model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item

# Update
@router.put("/{item_id}")
def update_item(item_id: int, item: ItemSchema, db: Session = Depends(get_db)):
    db_item = db.query(Model).filter(Model.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    return db_item

# Delete
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Model).filter(Model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted"}
```

### 多 Router 注册
```python
from fastapi import FastAPI
from routers import users, orders, products

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
```
