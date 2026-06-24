"""
项目启动入口
用法:
  python main.py          # 直接启动
  uvicorn main:app --reload
"""
import uvicorn

if __name__ == "__main__":   
    print("服务器已启动，监听地址：http://127.0.0.1:8000")
    print("文档地址：http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
