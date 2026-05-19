from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import DBTodo

# 实例化一个路由器，前缀统一为 /todos
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


# --- 增 ---
@router.post("/")
def create_todo(item: TodoItem, db: Session = Depends(get_db)):
    db_item = DBTodo(title=item.title, is_done=item.is_done)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# --- 查全部 ---
@router.get("/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(DBTodo).all()


# --- 更新 (PUT) ⭐新技能 ---
@router.put("/{todo_id}")
def update_todo(todo_id: int, item: TodoItem, db: Session = Depends(get_db)):
    # 1. 先查出这条数据
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if not todo:
        return {"error": "找不到"}

    # 2. 直接覆盖它的属性 (Python 对象属性赋值，ORM 会自动追踪变化)
    todo.title = item.title
    todo.is_done = item.is_done

    # 3. 提交事务，刷入磁盘
    db.commit()
    return todo


# --- 删 ---
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"message": "删除成功"}
    return {"error": "找不到"}