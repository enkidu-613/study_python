from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
from routers import ai_router, todos_routers, chat_memory_router, rag_router, langchain_rag_router, auth_router, ws_router

# ====== 应用描述（显示在 Swagger 文档顶部）======
DESCRIPTION = """
## 🎯 Study Python — Python → AI 全栈学习项目

从 Python 基础到 FastAPI 后端，再到 AI 集成（RAG、LangChain）的学习服务器。

### 🔐 认证
所有 `/auth/*` 接口用于用户注册、登录、登出。
受保护接口需要在请求头中携带：`Authorization: Bearer <token>`

### 📚 模块
- **AI 对话** — 流式 LLM 对话（SSE）
- **Todo CRUD** — 增删改查示例
- **聊天记忆** — 多轮对话上下文
- **手搓 RAG** — 检索增强生成（SQLite + ChromaDB）
- **LangChain RAG** — LCEL 链式语法框架化 RAG
- **JWT 认证** — 用户注册/登录/登出
"""

TAGS_METADATA = [
    {"name": "认证", "description": "用户注册、登录、登出、身份查询。"},
    {"name": "AI", "description": "流式 LLM 对话接口（SSE）。"},
    {"name": "Todos", "description": "Todo 增删改查示例。"},
    {"name": "Chat Memory", "description": "多轮对话上下文记忆。"},
    {"name": "RAG 向量检索", "description": "手写 RAG 闭环：存入 → 检索 → 生成。"},
    {"name": "LangChain RAG", "description": "LCEL 链式语法框架化 RAG。"},
    {"name": "WebSocket", "description": "实时双向通信接口；Swagger 不直接展示 WebSocket 路由。"},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ====== 启动时预加载 ======
    print("[启动] 预加载本地 Embedding 模型...")
    from local_embedding import get_embedding_model
    get_embedding_model()
    print("[启动] Embedding 模型加载完成")
    yield
    # ====== 关闭时清理 ======
    print("[关闭] 应用已停止")


app = FastAPI(
    title="Study Python API",
    description=DESCRIPTION,
    version="0.1.0",
    lifespan=lifespan,
    openapi_tags=TAGS_METADATA,
    docs_url="/docs",       # Swagger UI: http://127.0.0.1:8000/docs
    redoc_url="/redoc",     # ReDoc:      http://127.0.0.1:8000/redoc
)

# ====== CORS 中间件（允许前端跨域访问）======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],               # 学习阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== 全局异常处理 ======
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """兜底异常处理：防止 500 裸奔返回给前端"""
    print(f"[异常] {request.method} {request.url.path} → {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器内部错误: {type(exc).__name__}"},
    )

# ====== 注册路由 ======
app.include_router(ai_router)                    # AI 流式对话 /ai/*
app.include_router(todos_routers)                # Todo CRUD /todos/*
app.include_router(chat_memory_router)           # 聊天记忆 /chat-memory/*
app.include_router(rag_router.router)            # 手搓 RAG /rag/*
app.include_router(langchain_rag_router.router)  # LangChain RAG /langchain-rag/*
app.include_router(auth_router.router)
app.include_router(ws_router.router)             # WebSocket 实时通信 /ws/*

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    print("服务器已启动，监听地址：http://127.0.0.1:8000")
    print("文档地址：http://127.0.0.1:8000/docs")
