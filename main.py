from fastapi import FastAPI
import uvicorn
from routers import ai_router, todos_routers, chat_memory_router, rag_router, langchain_rag_router

app = FastAPI()

# 注册所有路由
app.include_router(ai_router)                    # AI 流式对话 /ai/*
app.include_router(todos_routers)                # Todo CRUD /todos/*
app.include_router(chat_memory_router)           # 聊天记忆 /chat-memory/*
app.include_router(rag_router.router)            # 手搓 RAG /rag/*
app.include_router(langchain_rag_router.router)  # LangChain RAG /langchain-rag/*

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
