from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from routers import ai_router, todos_routers, chat_memory_router, rag_router, langchain_rag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ====== 启动时预加载 ======
    print("[启动] 预加载本地 Embedding 模型...")
    from local_embedding import get_embedding_model
    get_embedding_model()  # 首次加载模型，约 10-20 秒
    print("[启动] Embedding 模型加载完成")
    yield
    # ====== 关闭时清理 ======
    print("[关闭] 应用已停止")


app = FastAPI(lifespan=lifespan)

# 注册所有路由
app.include_router(ai_router)                    # AI 流式对话 /ai/*
app.include_router(todos_routers)                # Todo CRUD /todos/*
app.include_router(chat_memory_router)           # 聊天记忆 /chat-memory/*
app.include_router(rag_router.router)            # 手搓 RAG /rag/*
app.include_router(langchain_rag_router.router)  # LangChain RAG /langchain-rag/*

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
