# 项目记忆 - PyCharmMiscProject

## 项目基本信息

- **项目名称**: PyCharmMiscProject (study_python)
- **项目类型**: Python + FastAPI ADHD友好学习项目
- **创建时间**: 2024年
- **主要用途**: 从 Python 基础到 AI 全栈开发的完整学习路径，包含 FastAPI 后端、RAG、LangChain、JWT、WebSocket 等

## 技术栈

- **语言**: Python 3.11+
- **Web框架**: FastAPI 0.128+
- **数据库**: SQLite (开发阶段) + ChromaDB (持久化向量存储)
- **ORM**: SQLAlchemy 2.0
- **向量数据库**: ChromaDB (本地持久化，chroma_db/ 目录)
- **Embedding**: 本地 bge-small-zh-v1.5 (sentence-transformers, MPS加速) + ModelScope API备选
- **LLM**: DeepSeek-V3.2 (via ModelScope/OpenAI兼容API)
- **AI框架**: LangChain (LCEL链式语法) + langchain-deepseek
- **认证**: JWT (pyjwt) + bcrypt密码哈希
- **数据库迁移**: Alembic
- **测试**: pytest 9.x + FastAPI TestClient
- **服务器**: Uvicorn (ASGI)
- **包管理**: Poetry + pip (requirements.txt备选)

## 项目结构

```
PyCharmMiscProject/
├── .trae/memory/              # 项目记忆与对话历史
│   ├── learning_plan.json     # 学习计划主数据
│   ├── learning_history_index.json
│   ├── roadmap查缺补漏计划.md
│   └── conversations/         # 日期对话归档
├── .reasonix/                 # Reasonix技能配置
├── .agents/skills/            # Agent技能
├── .codex/                    # Codex配置
├── alembic/                   # Alembic数据库迁移
│   ├── versions/              # 迁移脚本
│   └── env.py
├── chroma_db/                 # ChromaDB持久化数据
├── docs/                      # 文档与计划规格
├── md/                        # 学习文档(ADHD友好格式)
│   ├── README.md
│   ├── 00_~20_*.md            # 21个核心章节文档
│   ├── ai学习应用数学/        # 数学基础补充
│   ├── 试卷/                  # 章节测试卷（含补考卷）
│   ├── 答题/                  # 答题记录与错题
│   └── 错题本.md
├── routers/                   # FastAPI路由模块（分层架构）
│   ├── __init__.py
│   ├── ai_router.py           # AI流式对话 /ai/*
│   ├── auth_router.py         # JWT认证 /auth/*
│   ├── chat_memory.py         # 聊天记忆 /chat-memory/*
│   ├── todos_routers.py       # Todo CRUD /todos/*
│   ├── rag_router.py          # 手搓RAG /rag/*
│   ├── langchain_rag_router.py # LangChain RAG /langchain-rag/*
│   └── ws_router.py           # WebSocket实时通信 /ws/*
├── test/                      # pytest单元测试
│   ├── conftest.py            # pytest共享fixture
│   ├── test_auth.py
│   ├── test_fun.py
│   ├── test_rag.py
│   ├── test_router.py
│   ├── test_sse.py
│   └── test_ws.py
├── python第一月上半学习阶段/  # 早期Python练习代码
├── main.py                    # FastAPI应用入口
├── database.py                # 数据库配置(SQLite)
├── models.py                  # ORM模型(DBTodo, User, RevokedToken, Document, DocumentChunk)
├── ai_bot.py                  # AI聊天机器人(ModelScope API)
├── local_embedding.py         # 本地Embedding模型加载(bge-small-zh-v1.5)
├── rag_demo.py                # RAG入门演示
├── rag_test.py                # RAG测试
├── chroma_demo.py             # ChromaDB简化演示
├── chroma_real.py             # ChromaDB真实Embedding检索
├── dual_storage_demo.py       # 双存储架构演示
├── embedding_playground.py    # Embedding模型实验
├── pyproject.toml             # Poetry依赖管理
├── requirements.txt           # pip依赖
├── alembic.ini                # Alembic配置
└── README.md                  # 项目主说明
```

## 学习进度

### ✅ 已完成 (0-20章)
- [x] 00 - 环境配置与PyCharm使用
- [x] 01 - Python基础（变量、列表、字典、函数、类）
- [x] 02 - Python进阶（运算符、异常、文件、继承）
- [x] 03 - Python高级特性（列表推导式、生成器、装饰器）
- [x] 04 - FastAPI基础（JSON、路径参数、查询参数）
- [x] 05 - FastAPI CRUD（Pydantic、增删改查）
- [x] 06 - FastAPI ORM + SQLAlchemy（数据库、IoC/DI）
- [x] 07 - 代码分层与模块化架构（APIRouter）
- [x] 08 - 提示词工程与聊天记忆（System Prompt、多轮对话、SSE）
- [x] 09 - RAG向量数据库入门（Embedding、余弦相似度）
- [x] 10 - ChromaDB向量数据库实战
- [x] 11 - 双存储架构SQLite + ChromaDB
- [x] 12 - FastAPI + Chroma最小原型
- [x] 13 - 手搓最小RAG闭环（检索→拼Prompt→流式LLM）
- [x] 14 - 上下文窗口管理（Token截断、三层防御）
- [x] 15 - LangChain核心概念与集成（LCEL链式语法、ChatDeepSeek推理链）
- [x] 16 - 异步编程深入（async/await、三种协程对象、Semaphore、Event Loop）
- [x] 17 - JWT用户认证（bcrypt哈希、Token签发、Depends守卫、角色授权、黑名单、CORS、全局异常处理）
- [x] 18 - WebSocket实时通信（HTTP Upgrade、Query token认证、ConnectionManager、房间广播、AI流式打断）
- [x] 19 - Alembic数据库迁移（revision、upgrade/downgrade、autogenerate）
- [x] 20 - pytest单元测试（FastAPI TestClient、依赖覆盖、fixture、SSE测试、WebSocket测试）

### 🔥 当前进行中
- [ ] pytest进阶与测试完善
- [ ] 错题复习与薄弱点巩固

### 📋 待学习（后续阶段）
- [ ] Docker部署、CI/CD、日志与监控
- [ ] 前端框架基础（React/Vue）
- [ ] 前后端对接
- [ ] LangChain Memory & Agents（对话记忆、工具调用）
- [ ] RAG Chunking策略优化、混合检索、重排序
- [ ] RAG评估与指标（RAGAS）
- [ ] Prompt Engineering进阶（CoT、ReAct）
- [ ] AI Agents基础（ReAct模式、Function Calling）
- [ ] Multi-Agent与复杂工作流
- [ ] roadmap查缺补漏（详见roadmap查缺补漏计划.md）

## 核心概念掌握情况

### 已掌握
- ✅ Python基础语法和数据结构
- ✅ 函数和面向对象编程
- ✅ 列表推导式和生成器
- ✅ 装饰器原理
- ✅ FastAPI路由和参数
- ✅ Pydantic数据模型
- ✅ SQLAlchemy ORM操作
- ✅ 依赖注入(DI)和控制反转(IoC)
- ✅ yield在资源管理中的应用
- ✅ APIRouter模块化组织
- ✅ System Prompt和多轮对话
- ✅ SSE流式响应
- ✅ Embedding文本向量化（本地bge-small-zh-v1.5 + ModelScope API）
- ✅ 余弦相似度计算与数学原理
- ✅ ChromaDB向量数据库（Collection、add、query、持久化存储）
- ✅ 双存储架构（SQLite + ChromaDB，两条绳子连接）
- ✅ 手搓RAG闭环（检索→拼Prompt→LLM生成）
- ✅ 上下文窗口管理（Token估算、三层防御策略）
- ✅ LangChain LCEL链式语法（|管道符）
- ✅ LangChain核心组件（Document、Embedding、VectorStore、Retriever、LLM）
- ✅ LangChain ChatDeepSeek推理链集成（reasoning_content流式输出）
- ✅ 统一API响应格式（ApiResponse类，code/status/content）
- ✅ POJO/DTO概念及接口设计应用
- ✅ 对话历史索引管理（JSON格式索引）
- ✅ 异步编程深入（async/await、Coroutine/Task/Future三种对象、gather/create_task/as_completed、Semaphore限流、Event Loop）
- ✅ isinstance对比、Future唤醒回调机制
- ✅ JWT用户认证实战（bcrypt密码哈希、Token签发/验证、Depends守卫、角色守卫、登出黑名单、Swagger/CORS/全局异常处理）
- ✅ WebSocket实时通信（HTTP Upgrade、Query token认证、ConnectionManager、房间广播、SSE对比、可中断AI流式生成）
- ✅ Alembic数据库迁移（revision、upgrade/downgrade、autogenerate、target_metadata=Base.metadata、server_default、SQLite ALTER TABLE限制）
- ✅ pytest单元测试（FastAPI TestClient、依赖覆盖、fixture、conftest.py、测试数据库、SSE流式测试、WebSocket测试）
- ✅ 本地Embedding部署与MPS硬件加速
- ✅ 配置集中化（.env环境变量管理）
- ✅ 章节测试与补考系统（试卷/、答题/、错题本）

### 待深入学习
- ⬜ LangChain Memory对话记忆注入
- ⬜ LangChain Agents工具调用
- ⬜ Docker部署
- ⬜ CI/CD、日志与监控
- ⬜ 前端框架(React/Vue)
- ⬜ RAG Chunking策略优化
- ⬜ RAG评估指标(RAGAS)
- ⬜ roadmap.sh AI Engineer查缺补漏
