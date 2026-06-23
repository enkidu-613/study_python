# 🎯 study_python - 从 Python 到 AI 全栈的 ADHD 友好学习项目

> **适合 ADHD 学习者的 Python 与 FastAPI 完整学习资料**
> 从 Python 基础 → FastAPI 后端 → AI 接入 → RAG 向量数据库 → LangChain 框架，一步一个脚印
> 📅 创建时间：2026年3月 | 🐍 Python 3.11+ | ⚡ FastAPI | 🧠 AI 集成 | 🔗 LangChain

---

## 📚 项目简介

这是一个**从零开始的 Python 后端学习项目**，专为 ADHD 学习者设计。通过丰富的类比、流程图、表格和实战代码，帮助理解从 Python 基础到 AI 应用开发的完整技术栈。

**当前阶段**：pytest 单元测试（已完成 ✅），下一阶段：高级提示词工程（prompt-advanced）

---

## 🗂️ 项目结构

```
PyCharmMiscProject/
│
├── 🚀 app/                          # 【核心代码区】每天写的代码都在这里
│   ├── main.py                      # FastAPI 入口（启动+路由注册+CORS/中间件）
│   ├── database.py                  # 数据库配置（SQLite/SQLAlchemy）
│   ├── models.py                    # ORM 模型（DBTodo/User/RevokedToken/Document/DocumentChunk）
│   ├── embedding.py                 # 本地Embedding模型（bge-small-zh-v1.5，原local_embedding.py）
│   │
│   └── routers/                     # API路由（文件名统一，无冗余后缀）
│       ├── ai.py                    # AI 流式对话 /ai/*
│       ├── auth.py                  # JWT 认证 /auth/*
│       ├── todos.py                 # Todo CRUD /todos/*
│       ├── chat_memory.py           # 聊天记忆 /chat-memory/*
│       ├── rag.py                   # 手搓 RAG /rag/*
│       ├── langchain_rag.py         # LangChain RAG /langchain-rag/*
│       ├── websocket.py             # WebSocket 实时通信 /ws/*
│       └── prompt.py                # Prompt Engineering 高级 /prompt-advanced/*
│
├── 📦 archive/                      # 【归档区】历史学习代码（留作回顾，不干扰主线）
│   └── month1-python-basics/        # 第1个月Python基础练习（按编号00-06顺序学习）
│
├── 🧪 playground/                   # 【实验区】Demo/试错代码（随便改，不影响主项目）
│   ├── ai_bot.py                    # AI 聊天机器人（ModelScope API）
│   ├── embedding_playground.py      # Embedding模型实验
│   ├── rag_demo.py / rag_test.py    # RAG 入门与测试
│   ├── chroma_demo.py / chroma_real.py  # ChromaDB 演示
│   └── dual_storage_demo.py         # 双存储架构完整演示
│
├── ✅ tests/                        # 【测试区】pytest 单元测试（标准Python tests/命名）
│   ├── conftest.py                  # pytest 共享 fixture
│   ├── test_auth.py                 # JWT 认证测试
│   ├── test_fun.py                  # 函数式测试
│   ├── test_prompt.py               # Prompt 高级测试
│   ├── test_rag.py                  # RAG 测试
│   ├── test_sse.py                  # SSE 流式测试
│   ├── test_todos.py                # Todo CRUD 测试
│   └── test_websocket.py            # WebSocket 测试
│
├── 📖 md/                           # 【学习文档区】ADHD友好格式的学习笔记
│   ├── 00_环境配置与PyCharm使用.md
│   ├── 01_Python基础.md ~ 21_Prompt_Engineering进阶.md
│   ├── README.md                    # 本文档索引
│   ├── ai学习应用数学/
│   ├── 试卷/                        # 章节测试卷（含补考卷）
│   ├── 答题/                        # 答题记录与错题
│   └── 错题本.md
│
├── 🗄️ alembic/                      # Alembic 数据库迁移
├── 💾 chroma_db/                    # ChromaDB 持久化数据
│
├── main.py                          # 项目启动入口（python main.py 直接启动）
├── pyproject.toml                   # Poetry 依赖管理
├── alembic.ini                      # Alembic配置
└── requirements.txt                 # pip 依赖（备选）
```

---

## 🚀 学习路线图

### ✅ 已完成

| 步骤 | 主题 | 对应代码 | 掌握程度 |
|------|------|----------|----------|
| 0 | 环境配置与 PyCharm 使用 | - | ✅ |
| 1 | Python 基础（变量、列表、字典、函数、类） | `py学习.py` | ✅ |
| 2 | Python 进阶（运算符、异常、文件、继承） | `py学习_进阶.py` | ✅ |
| 3 | Python 高级特性（列表推导式、生成器、装饰器） | `py学习_进阶2.py` | ✅ |
| 4 | FastAPI 基础（JSON、路径参数、查询参数） | `python_接触fastapi之前的补充.py` | ✅ |
| 5 | FastAPI CRUD（Pydantic、增删改查） | `py_CRUD.py` | ✅ |
| 6 | FastAPI ORM + SQLAlchemy（数据库、IoC/DI） | `py_ORM.py` | ✅ |
| 7 | 代码分层与模块化架构（APIRouter） | `app/main.py` + `app/routers/` | ✅ |
| 8 | 提示词工程与聊天记忆（System Prompt、多轮对话） | `app/routers/chat_memory.py` | ✅ |
| 9 | RAG 向量数据库入门（Embedding、余弦相似度） | `playground/rag_test.py`, `playground/rag_demo.py` | ✅ |
| 10 | ChromaDB 向量数据库实战 | `playground/chroma_demo.py`, `playground/chroma_real.py` | ✅ |
| 11 | 双存储架构 SQLite + ChromaDB | `playground/dual_storage_demo.py`, `app/models.py` | ✅ |
| 12 | FastAPI + Chroma 最小原型 | `app/routers/rag.py` | ✅ |
| 13 | 手搓最小 RAG 闭环 | `app/routers/rag.py` | ✅ |
| 14 | 上下文窗口管理（Token 截断、防幻觉） | `app/routers/rag.py` | ✅ |
| 15 | **LangChain 集成（LCEL 链式语法、DeepSeek 推理链）** | `app/routers/langchain_rag.py` | ✅ |
| 16 | **异步编程深入（async/await 原理、三种协程对象、Semaphore）** | - | ✅ |
| 17 | **学习计划审计与 AI 应用路线精简** | - | ✅ |
| 18 | **JWT 用户认证（密码哈希、Token 签发、Depends 守卫、角色授权）** | `app/routers/auth.py` | ✅ |
| 19 | **WebSocket 实时通信（协议升级、房间广播、AI 流式打断）** | `app/routers/websocket.py` | ✅ |
| 20 | **Alembic 数据库迁移（revision、upgrade、downgrade、autogenerate）** | `alembic/` | ✅ |

### ✅ 已完成（续）

| 步骤 | 主题 | 对应代码 | 掌握程度 |
|------|------|----------|----------|
| 21 | **pytest 单元测试（FastAPI TestClient、依赖覆盖、断言）** | `tests/` | ✅ |
| 22 | **pytest 进阶（conftest fixture、SSE 流式测试、WebSocket 测试）** | `tests/test_sse.py`, `tests/test_websocket.py` | ✅ |
| 23 | **Prompt Engineering 进阶（Few-shot、结构化输出、角色隔离）** | `app/routers/prompt.py` | 🔥 进行中 |

### 🔥 下一步

| 阶段 | 内容 | 说明 |
|------|------|------|
| **AI 核心深入** | 高级提示词工程（结构化输出、采样参数、Prompt Injection防御） | prompt-advanced |
| **AI 核心深入** | RAG Chunking策略、混合检索、重排序、RAGAS评估 | rag-chunking/evaluation |
| **AI 核心深入** | AI Agents基础（ReAct模式、Function Calling，手动实现优先） | ai-agents |
| **AI 核心深入** | LangChain Memory/Agents、LangGraph | langchain-* |
| **AI 核心深入** | LLM评估与可观测性（LangSmith/Langfuse） | llm-eval |
| **全栈补全（暂缓）** | Docker部署、CI/CD、日志监控 | 工程能力补全 |
| **全栈补全（暂缓）** | React/Vue基础、前后端对接 | 全栈能力 |
| **详见** | roadmap.sh AI Engineer 查缺补漏计划 | `.trae/memory/roadmap查缺补漏计划.md` |

---

## 🛠️ 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **语言** | Python 3.11+ | 核心编程语言 |
| **Web 框架** | FastAPI | 高性能异步 Web 框架 |
| **数据库** | SQLite + ChromaDB | 关系型 + 向量数据库双存储 |
| **ORM** | SQLAlchemy | 数据库对象关系映射 |
| **AI 框架** | LangChain (LCEL) | RAG 链式编排 |
| **AI API** | ModelScope (OpenAI 兼容) | 国内 AI 模型接入 |
| **向量模型** | bge-small-zh-v1.5 (本地) | 文本向量化（512维，本地部署 MPS 加速，sentence-transformers） |
| **LLM 模型** | DeepSeek-V3.2 | 大语言模型问答 |
| **包管理** | Poetry | 依赖管理与虚拟环境 |
| **部署** | Uvicorn | ASGI 服务器 |

---

## 🎯 核心功能模块

### 1. AI 流式对话 (`/ai`)
- 接入 DeepSeek-V3.2 模型（通过 ModelScope）
- 支持思维链（CoT）显示
- 流式响应（SSE）

### 2. 聊天记忆 (`/chat-memory`)
- 多轮对话上下文记忆
- System Prompt 人设控制
- 内存存储（后续将持久化）

### 3. Todo CRUD (`/todos`)
- 完整的增删改查
- SQLAlchemy ORM 操作
- 依赖注入（DI）实践

### 4. 手搓 RAG (`/rag/*`)
- **存储**: 双存储架构（SQLite 存全文 + ChromaDB 存向量）
- **检索**: 语义检索 + 上下文窗口管理
- **生成**: 流式 LLM 调用，带资料来源引用
- **代码**: [`app/routers/rag.py`](app/routers/rag.py)

### 5. LangChain RAG (`/langchain-rag/*`)
- **框架化**: 使用 LangChain LCEL 链式语法重构 RAG
- **复用数据**: 与手搓版共用同一个 ChromaDB collection
- **流式输出**: `chain.astream()` 一步搞定检索 → 拼 Prompt → LLM 生成
- **推理链**: 集成 ChatDeepSeek，支持深度思考（reasoning_content）流式输出
- **统一响应**: 标准 API 响应格式（`{"code": 200, "status": "success", "content": ...}`）
- **文档管理**: 支持文档删除（同步清理 ChromaDB + SQLite）
- **代码**: [`app/routers/langchain_rag.py`](app/routers/langchain_rag.py)

### 6. Prompt Engineering 高级 (`/prompt-advanced/*`)
- **任务提取器**: 从自然语言文本中结构化提取任务（标题、优先级、标签）
- **Few-shot 提示**: 通过示例输入输出引导模型行为
- **结构化输出**: Pydantic 模型约束 LLM 输出格式（`TaskExtractionResult`）
- **角色隔离**: System Prompt 明确限定模型为"信息提取器"，拒绝执行指令
- **代码**: [`app/routers/prompt.py`](app/routers/prompt.py)

---

## 📖 学习文档速查

| 文档 | 内容 | 难度 |
|------|------|------|
| [00_环境配置](md/00_环境配置与PyCharm使用.md) | PyCharm、虚拟环境、调试 | ⭐ |
| [01_Python基础](md/01_Python基础.md) | 变量、列表、字典、函数、类 | ⭐ |
| [02_Python进阶](md/02_Python进阶.md) | 运算符、异常、文件、继承 | ⭐⭐ |
| [03_Python高级特性](md/03_Python高级特性.md) | 列表推导式、生成器、装饰器 | ⭐⭐⭐ |
| [04_FastAPI基础](md/04_FastAPI基础.md) | JSON、路径参数、查询参数 | ⭐⭐ |
| [05_FastAPI_CRUD](md/05_FastAPI_CRUD.md) | Pydantic、增删改查 | ⭐⭐⭐ |
| [06_FastAPI_ORM](md/06_FastAPI_ORM_SQLAlchemy.md) | 数据库、ORM、IoC/DI | ⭐⭐⭐⭐ |
| [07_代码分层](md/07_代码分层与模块化架构.md) | APIRouter、分层架构 | ⭐⭐⭐⭐ |
| [08_提示词工程](md/08_提示词工程与聊天记忆.md) | System Prompt、多轮对话、SSE | ⭐⭐⭐ |
| [09_RAG入门](md/09_RAG_向量数据库入门.md) | Embedding、余弦相似度、向量数据库概念 | ⭐⭐⭐⭐ |
| [10_ChromaDB实战](md/10_RAG_ChromaDB向量数据库实战.md) | Collection、add/query、简化vs真实向量 | ⭐⭐⭐ |
| [11_双存储架构](md/11_双存储架构SQLite_ChromaDB.md) | SQLite+ChromaDB、两条绳子连接 | ⭐⭐⭐⭐ |
| [12_最小原型](md/12_FastAPI_Chroma_最小原型.md) | API 封装、持久化存储、依赖注入 | ⭐⭐⭐⭐ |
| [13_RAG闭环](md/13_RAG_闭环_检索到回答.md) | 检索 → 拼 Prompt → 流式 LLM 调用 | ⭐⭐⭐⭐ |
| [14_上下文窗口](md/14_上下文窗口管理.md) | Token 截断策略、超长 Prompt 处理、防幻觉 | ⭐⭐⭐⭐ |
| [15_LangChain](md/15_LangChain核心概念.md) | LCEL 链式语法、六大核心概念 | ⭐⭐⭐⭐ |
| [16_异步编程深入](md/16_异步编程深入.md) | async/await 原理、三种协程对象、并发模式、Semaphore 限流 | ⭐⭐⭐⭐ |
| [17_JWT用户认证](md/17_JWT用户认证.md) | JWT 令牌、bcrypt 密码哈希、Depends 验票、角色守卫、黑名单、Swagger/CORS/异常处理 | ⭐⭐⭐⭐ |
| [18_WebSocket实时通信](md/18_WebSocket实时通信.md) | WebSocket 协议升级、Query token 认证、房间广播、AI 流式打断 | ⭐⭐⭐⭐ |
| [19_Alembic数据库迁移](md/19_Alembic数据库迁移.md) | 迁移心智模型、revision、upgrade/downgrade、autogenerate、target_metadata | ⭐⭐⭐⭐ |
| [20_pytest单元测试](md/20_pytest单元测试.md) | FastAPI TestClient、依赖覆盖、断言、fixture、测试数据库 | ⭐⭐⭐⭐ |
| [21_Prompt Engineering 进阶](md/21_Prompt_Engineering进阶.md) | Few-shot、结构化输出、角色隔离、Pydantic 约束 | ⭐⭐⭐⭐ |
| [向量与余弦相似度](md/ai学习应用数学/01_向量与余弦相似度.md) | 数学基础复习 | ⭐⭐ |

---

## 🧠 核心概念掌握情况

### 已掌握
- ✅ Python 基础语法和数据结构
- ✅ 函数和面向对象编程
- ✅ 列表推导式和生成器
- ✅ 装饰器原理
- ✅ FastAPI 路由和参数
- ✅ Pydantic 数据模型
- ✅ SQLAlchemy ORM 操作
- ✅ 依赖注入 (DI) 和控制反转 (IoC)
- ✅ `yield` 在资源管理中的应用
- ✅ APIRouter 模块化组织
- ✅ System Prompt 和多轮对话
- ✅ Embedding 文本向量化（ModelScope API）
- ✅ 余弦相似度计算与数学原理
- ✅ ChromaDB 向量数据库（Collection、add、query）
- ✅ 双存储架构（SQLite + ChromaDB，两条绳子连接）
- ✅ 手搓 RAG 闭环（检索 → 拼 Prompt → LLM 生成）
- ✅ 上下文窗口管理（Token 估算、三层防御策略）
- ✅ LangChain LCEL 链式语法（`|` 管道符）
- ✅ LangChain 核心组件（Document、Embedding、VectorStore、Retriever、LLM）
- ✅ LangChain ChatDeepSeek 推理链集成（reasoning_content）
- ✅ 统一 API 响应格式（`ApiResponse` 类，code/status/content）
- ✅ POJO/DTO 概念及在接口设计中的应用
- ✅ 对话历史索引管理（JSON 格式索引）
- ✅ 异步编程深入（async/await、Coroutine/Task/Future 三种对象、并发模式 gather/create_task/as_completed、Semaphore 限流、Event Loop 调度原理）
- ✅ isinstance 与 instanceof 对比、Future 唤醒回调机制
- ✅ JWT 用户认证实战（bcrypt 密码哈希、Token 签发/验证、Depends 守卫、角色守卫、登出黑名单、Swagger/CORS/全局异常处理）
- ✅ WebSocket 实时通信（HTTP Upgrade、Query token 认证、ConnectionManager、房间广播、SSE 对比、可中断 AI 流式生成）
- ✅ Alembic 数据库迁移（revision、upgrade、downgrade、autogenerate、target_metadata = Base.metadata、server_default、SQLite ALTER TABLE 限制）
- ✅ pytest 单元测试（FastAPI TestClient、依赖覆盖、fixture、conftest、测试数据库、SSE流式测试、WebSocket测试、Arrange/Act/Assert三段式、假阳性空测试诊断）
- ✅ 章节测试与补考系统（试卷/、答题/、错题本）

### 待深入学习
- ⬜ Prompt Engineering 进阶（结构化输出、采样参数、Prompt Injection边界）
- ⬜ RAG Chunking策略、混合检索、重排序、RAGAS评估
- ⬜ AI Agents基础（ReAct模式、Function Calling，手动实现优先）
- ⬜ LangChain Memory & Agents、LangGraph
- ⬜ LLM评估与可观测性（LangSmith、Langfuse）
- ⬜ Docker 部署
- ⬜ CI/CD、日志与监控
- ⬜ 前端框架 (React/Vue)
- ⬜ roadmap 查缺补漏（详见 `.trae/memory/roadmap查缺补漏计划.md`）

---

## 🔗 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Chroma 官方文档](https://docs.trychroma.com/)
- [LangChain 官方文档](https://python.langchain.com/)
- [ModelScope 模型库](https://www.modelscope.cn/)
- [OpenAI Embedding 指南](https://platform.openai.com/docs/guides/embeddings)
- [roadmap.sh AI Engineer](https://roadmap.sh/ai/roadmap-chat/ai-engineer)

---

## 📝 项目记忆

本项目使用 `.trae/memory/` 目录记录完整的学习历史：

- **learning_plan.json**：学习计划主数据（42 个阶段）
- **learning_history_index.json**：历史文件索引（含对话记录索引，JSON 格式）
- **roadmap查缺补漏计划.md**：roadmap.sh AI Engineer 查缺补漏完整计划
- **conversations/**：日期对话文件

---

## 🤖 AI 辅助技能

本项目配备了 9 个定制 AI 技能，在对话中随时可用：

| 技能 | 触发场景 | 功能 |
|------|----------|------|
| **python-adhd-tutor** | 询问 Python 基础、编程概念或代码机制 | 以 ADHD 友好且专业的方式讲解 Python |
| **comfortable-fast-learning-coach** | ADHD学习指导、薄弱点诊断、学习规划 | 舒心快速学习流程教练 |
| **programming-language-mastery** | 学习新语言、对比语言特性、通用编程概念 | 跨语言的计算思维心法 |
| **chapter-review-quizzer** | 要求检测、复习错题、检查章节掌握程度 | 生成试卷 → 用户答题 → AI批改并记录错题 |
| **learning-plan-manager** | 更新进度、追踪阶段、添加计划、查询状态 | 管理学习计划进度和历史文件索引 |
| **history-archiver** | 归档对话历史 | 按实际日期归档到正确的 `YYYY-MM-DD.md` 文件 |
| **firecrawl-karpathy-research** | 网页研究、技术调研 | Firecrawl网页研究 + Karpathy风格AI工程准则 |
| **tech-search-sources** | 搜索技术问题 | 优先从 GitHub、Stack Overflow、掘金、V2EX 等来源获取 |
| **ui-ux-pro-max-3** | UI/UX设计、前端界面 | 设计智能、组件库、样式方案 |

> 💡 在对话中直接说出需求即可触发对应技能，例如：「帮我检测一下第 20 章的掌握程度」

---

> **祝你学习愉快！记住：理解 > 记忆，实践 > 阅读。**
> 对于 ADHD 学习者：番茄工作法（25分钟学习 + 5分钟休息）+ 立即动手验证 = 最佳学习效果 🚀
