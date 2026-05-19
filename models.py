from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()

class DBTodo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_done = Column(Boolean, default=False)

# 建表动作只执行一次
Base.metadata.create_all(bind=engine)