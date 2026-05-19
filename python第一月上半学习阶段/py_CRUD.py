from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run
app = FastAPI()

# 定义快递模板单
class TodoItem(BaseModel):
    title: str #必须是字符串
    is_done: bool = False #必须是布尔值，默认值是false
# 创建一个list假装是数据库
fake_db = []

#增
@app.post("/todos")
def create_todo(todoItem: TodoItem): # FastAPI 会把收到的json塞进item内
    fake_db.append(todoItem)
    return {"message":"Todo item created successfully"}
#查
@app.get("/todos")
def get_todos():
    return {"total": len(fake_db), "todos": fake_db}
#删
@app.delete("/todos/{index}")
def delete_todo(index: int):
    if 0 <= index < len(fake_db):
        del_item = fake_db.pop(index)
        return {"status":"success","message":f"Deleted item: {del_item}"}
    return {"status":"error","message":"I dont know this item"}


if __name__ == "__main__":
    run(app, host="localhost", port=8000)