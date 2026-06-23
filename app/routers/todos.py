from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DBTodo

router = APIRouter(prefix="/todos", tags=["Todos"])


class TodoItem(BaseModel):
    title: str
    is_done: bool = False


@router.post("/")
def create_todo(item: TodoItem, db: Session = Depends(get_db)):
    db_item = DBTodo(title=item.title, is_done=item.is_done)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(DBTodo).all()


@router.put("/{todo_id}")
def update_todo(todo_id: int, item: TodoItem, db: Session = Depends(get_db)):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if not todo:
        return {"error": "找不到"}

    todo.title = item.title
    todo.is_done = item.is_done

    db.commit()
    return todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"message": "删除成功"}
    return {"error": "找不到"}
