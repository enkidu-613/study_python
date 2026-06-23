import json

#将字典转换为json字符串
person = {"name":"Alice","age":18}
print(person, type(person))
json_str = json.dumps(person)
print(json_str, type(json_str))

from fastapi import FastAPI
import uvicorn
# 创建一个fastapi实例
app = FastAPI()
@app.get("/")
def home():
    return {"message":"Hello World"}
#API
@app.get("/hello/{name}") #路径参数
def say_hello(name: str): #把路径里的东西抓出来，存到name变量里
    return {"message":f"Hello {name},欢迎来到我的网站！"}
@app.get("/search")
def search(keyword: str, limit: int = 10): #查询参数 是地址问号后面的信息
    #FastAPI 会把 ?keyword=xxx 抓过来
    #limit = 10 意思是如果用户没有写limit 默认就是10
    return  {
        "你在找":keyword,
        "要几条":limit
    }
#启动服务器
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



