from gc import get_debug

from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy import create_engine,Column,Integer,String,Boolean
import uvicorn
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#链接数据库
DATABASE_URL = "sqlite:///.my_database.db"
engine = create_engine(DATABASE_URL, #你告诉这个方法sqllite地址他就会去在硬盘上寻找新建这个文件，把大门焊死，准备好传送带以后所有数据都从这里进出
                       connect_args={"check_same_thread":False})# 总的来说，创建了一个数据库引擎
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)# 使用会话工厂类创建一个会话工厂实例
Base = declarative_base()# 创建基类，记录继承他所有的ORM模型类，后续与数据库引擎关联，知道表要创建到哪里，给普通python类添加数据库操作能力
# 你不能随便往仓库乱扔东西，你要定做货架，class DBTodo就是图纸

class DBTodo(Base):# 定义一个orm模型，继承Base基类，作用是把面向对象和数据库的关系型表结构映射起来，约等于执行了SQL的DDL的创建表结构语句
    __tablename__ = "todos"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    is_done = Column(Boolean,default=False)
#在硬盘上真正建好这个表
Base.metadata.create_all(engine)
#数据库部分完成
#开始业务代码
app = FastAPI()

# 前端传过来快递单的格式
class TodoItem(BaseModel):
    title: str
    is_done: bool = False

# 获取数据库连接的函数
def get_db():
    # 当在Depends中调用这个函数的时候，而且被赋值给参数的时候，FastAPI执行依赖解析，调用该函数
    # 执行get_db到yield db
    # 拿到db实例，暂停get_db()
    # 将db注入给被赋值的参数
    # 执行该函数体，到该函数体执行完毕
    # FastAPI返回到get_db的暂停点，继续执行db.close()
    # 发送http相应
    db = SessionLocal() #使用会话工厂实例创建一个会话实例
    try:
        yield db# 这里使用yield将db返回出去的原因是return执行后该函数在Depends中不会在所调用的函数执行完成后继续执行db.close
    finally:
        db.close()
# 增
@app.post("/todos")
def create_todo(todo_item: TodoItem,db: Session = Depends(get_db)):
    # 控制反转 是使用Depends来实现的，传统写法是我来创建、控制、关闭db实例
    # 使用控制反转之后我只需要定义db的创建、控制、关闭逻辑，剩下的交给框架来自动执行
    # 把快递单的数据，转成数据库认识的样子
    db_item = DBTodo(title=todo_item.title,is_done=todo_item.is_done)
    #塞进数据库
    db.add(db_item)
    #保存到硬盘
    db.commit()
    #刷新一下，拿到数据库自动生成的id
    db.refresh(db_item)
    return {"message":"存到硬盘了！","data":db_item}
#查
@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(DBTodo).all()
    return {"data":todos}
#删
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int,db: Session = Depends(get_db)):
    #找到那个 id 的对应数据
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"message":"删除成功"}
    return {"message":"删除失败"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)


