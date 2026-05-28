# 项目记忆 - PyCharmMiscProject

## 项目基本信息

- **项目名称**: PyCharmMiscProject
- **项目类型**: Python + FastAPI 学习项目
- **创建时间**: 2024年
- **主要用途**: Python 后端开发学习，从基础到 FastAPI + SQLAlchemy ORM

## 技术栈

- **语言**: Python 3.11
- **Web框架**: FastAPI
- **数据库**: SQLite (开发阶段)
- **ORM**: SQLAlchemy
- **向量数据库**: ChromaDB (内存模式)
- **Embedding**: ModelScope API (Qwen/Qwen3-Embedding-8B)
- **LLM**: ModelScope API (流式聊天)
- **服务器**: Uvicorn
- **包管理**: Poetry

## 项目结构

```
study_python/
├── .trae/
│   └── memory/              # 记忆存储文件夹
├── md/                      # 学习文档 (11个Markdown文件)
│   ├── README.md
│   ├── 00_环境配置与PyCharm使用.md
│   ├── 01_Python基础.md
│   ├── 02_Python进阶.md
│   ├── 03_Python高级特性.md
│   ├── 04_FastAPI基础.md
│   ├── 05_FastAPI_CRUD.md
│   ├── 06_FastAPI_ORM_SQLAlchemy.md
│   ├── 07_代码分层与模块化架构.md
│   ├── 08_提示词工程与聊天记忆.md
│   ├── 09_RAG_向量数据库入门.md
│   ├── 10_RAG_ChromaDB向量数据库实战.md
│   └── 11_双存储架构SQLite_ChromaDB.md
│   └── ai学习应用数学/
│       └── 01_向量与余弦相似度.md
├── routers/                 # FastAPI 路由模块
│   ├── ai_router.py
│   ├── chat_memory.py
│   └── todos_routers.py
├── main.py                  # FastAPI 应用入口 (分层架构)
├── database.py              # 数据库配置
├── models.py                # ORM 模型 (Todo + Document + DocumentChunk)
├── ai_bot.py                # AI 聊天机器人
├── chroma_demo.py           # ChromaDB 简化向量演示
├── chroma_real.py           # ChromaDB 真实 Embedding 演示
├── embedding_playground.py  # Embedding 模型实验
├── dual_storage_demo.py     # 双存储架构演示
├── rag_test.py              # RAG 余弦相似度测试
├── rag_demo.py              # RAG 演示
├── pyproject.toml           # Poetry 包管理配置
└── requirements.txt         # pip 依赖

## 学习进度

- [x] Python 基础 (变量、列表、字典、函数、类)
- [x] Python 进阶 (运算符、异常处理、文件操作、继承)
- [x] Python 高级特性 (列表推导式、生成器、装饰器)
- [x] FastAPI 基础 (JSON、路径参数、查询参数)
- [x] FastAPI CRUD (Pydantic、增删改查)
- [x] FastAPI ORM (SQLAlchemy、依赖注入)
- [x] 代码分层 (APIRouter、模块化架构)
- [x] 提示词工程与聊天记忆 (System Prompt、多轮对话、SSE流式)
- [x] RAG 向量数据库入门 (Embedding、余弦相似度、向量概念)
- [x] ChromaDB 实战 (Collection、add、query、真实 Embedding)
- [x] Embedding 模型实验 (语义相近、多义词、跨语言)
- [x] 双存储架构 (SQLite + ChromaDB 协作、ChunkVector)
- [ ] FastAPI + Chroma 最小原型 (下一步)
- [ ] 手搓最小 RAG 闭环
- [ ] LangChain 集成
- [ ] 用户认证 (JWT)
- [ ] 项目部署 (Docker)
- [ ] 前端框架基础
- [ ] 前后端对接

## 核心概念掌握情况

### 已掌握
- Python 基础语法和数据结构
- 函数和面向对象编程
- 列表推导式和生成器
- 装饰器原理
- FastAPI 路由和参数
- Pydantic 数据模型
- SQLAlchemy ORM 操作
- 依赖注入 (DI) 和控制反转 (IoC)
- yield 在资源管理中的应用
- APIRouter 模块化组织
- System Prompt 与多轮对话记忆
- SSE 流式响应
- Embedding 向量化 (ModelScope API)
- 余弦相似度计算与数学原理
- ChromaDB 基本操作 (Collection、add、query)
- 双存储架构 (SQLite Document/DocumentChunk + ChromaDB 向量)

### 待深入学习
- FastAPI + Chroma 最小原型
- 手搓最小 RAG 闭环
- LangChain 框架集成
- 异步编程 (async/await)
- 用户认证 (JWT/OAuth2)
- 数据库迁移 (Alembic)
- 测试 (pytest)
- Docker 部署
- 前端框架对接 (React/Vue)
