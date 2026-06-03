# 🎯 study_python - 从 Python 到 AI 全栈的 ADHD 友好学习项目

> **适合 ADHD 学习者的 Python 与 FastAPI 完整学习资料**
> 从 Python 基础 → FastAPI 后端 → AI 接入 → RAG 向量数据库 → LangChain 框架，一步一个脚印
> 📅 创建时间：2024年 | 🐍 Python 3.11+ | ⚡ FastAPI | 🧠 AI 集成 | 🔗 LangChain

---

## 📚 项目简介

这是一个**从零开始的 Python 后端学习项目**，专为 ADHD 学习者设计。通过丰富的类比、流程图、表格和实战代码，帮助理解从 Python 基础到 AI 应用开发的完整技术栈。

**当前阶段**：LangChain 集成（已完成 ✅）→ RAG 深化 & 工程化

---

## 🗂️ 项目结构

```
study_python/
├── 📁 md/                          # 学习文档（ADHD友好格式）
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
│   ├── 11_双存储架构SQLite_ChromaDB.md
│   ├── 12_FastAPI_Chroma_最小原型.md
│   ├── 13_RAG_闭环_检索到回答.md
│   ├── 14_上下文窗口管理.md
│   ├── 15_LangChain核心概念.md
│   ├── ai学习应用数学/
│   │   └── 01_向量与余弦相似度.md
│   └── 错题本.md
│
├── 📁 routers/                     # FastAPI 路由模块（分层架构）
│   ├── ai_router.py                # AI 流式对话 /ai/*
│   ├── chat_memory.py              # 聊天记忆 /chat-memory/*
│   ├── todos_routers.py            # Todo CRUD /todos/*
│   ├── rag_router.py               # 手搓 RAG /rag/*
│   └── langchain_rag_router.py     # LangChain RAG /langchain-rag/*
│
├── 📁 .trae/memory/                # 项目记忆与对话历史
│   ├── learning_plan.json          # 学习计划主数据
│   ├── learning_history_index.json # 学习历史索引（含对话记录索引）
│   ├── roadmap查缺补漏计划.md       # roadmap.sh AI Engineer 查缺补漏
│   └── conversations/              # 日期对话文件
│
├── main.py                         # FastAPI 应用入口
├── database.py                     # 数据库配置（SQLite）
├── models.py                       # ORM 模型（含 Document、DocumentChunk）
├── ai_bot.py                       # AI 聊天机器人（ModelScope API）
├── rag_demo.py                     # RAG 入门：Embedding 与相似度
├── rag_test.py                     # RAG 测试：ModelScope Embedding API
├── chroma_demo.py                  # ChromaDB 简化版演示
├── chroma_real.py                  # ChromaDB 真实 Embedding 检索
├── dual_storage_demo.py            # 双存储架构完整演示
├── pyproject.toml                  # Poetry 依赖管理
└── requirements.txt                # pip 依赖（备选）
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
| 7 | 代码分层与模块化架构（APIRouter） | `main.py` + `routers/` | ✅ |
| 8 | 提示词工程与聊天记忆（System Prompt、多轮对话） | `routers/chat_memory.py` | ✅ |
| 9 | RAG 向量数据库入门（Embedding、余弦相似度） | `rag_test.py`, `rag_demo.py` | ✅ |
| 10 | ChromaDB 向量数据库实战 | `chroma_demo.py`, `chroma_real.py` | ✅ |
| 11 | 双存储架构 SQLite + ChromaDB | `dual_storage_demo.py`, `models.py` | ✅ |
| 12 | FastAPI + Chroma 最小原型 | `routers/rag_router.py` | ✅ |
| 13 | 手搓最小 RAG 闭环 | `routers/rag_router.py` | ✅ |
| 14 | 上下文窗口管理（Token 截断、防幻觉） | `routers/rag_router.py` | ✅ |
| 15 | **LangChain 集成（LCEL 链式语法、DeepSeek 推理链）** | `routers/langchain_rag_router.py` | ✅ |

### 🔥 进行中

| 步骤 | 主题 | 对应代码 | 状态 |
|------|------|----------|------|
| 16 | **RAG 深化 & 工程化（记忆注入、Agents、测试）** | - | 🔥 当前 |

### 📋 待学习

| 阶段 | 内容 | 说明 |
|------|------|------|
| **LangChain 深化** | Memory、Agents、Prompt 进阶 | LangChain 框架深入 |
| **后端深耕** | 异步编程、用户认证 (JWT)、数据库迁移 (Alembic)、单元测试 (pytest)、Docker 部署 | 工程能力补全 |
| **前端** | React/Vue 基础、前后端对接 | 全栈能力 |
| **roadmap 查缺补漏** | RAG 进阶、AI Agents、MCP、多模态、Fine-tuning 等 | 详见 `.trae/memory/roadmap查缺补漏计划.md` |

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
| **向量模型** | Qwen/Qwen3-Embedding-8B | 文本向量化（4096维） |
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
- **代码**: [`routers/rag_router.py`](routers/rag_router.py)

### 5. LangChain RAG (`/langchain-rag/*`)
- **框架化**: 使用 LangChain LCEL 链式语法重构 RAG
- **复用数据**: 与手搓版共用同一个 ChromaDB collection
- **流式输出**: `chain.astream()` 一步搞定检索 → 拼 Prompt → LLM 生成
- **推理链**: 集成 ChatDeepSeek，支持深度思考（reasoning_content）流式输出
- **统一响应**: 标准 API 响应格式（`{"code": 200, "status": "success", "content": ...}`）
- **文档管理**: 支持文档删除（同步清理 ChromaDB + SQLite）
- **代码**: [`routers/langchain_rag_router.py`](routers/langchain_rag_router.py)

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

### 待深入学习
- ⬜ LangChain Memory（对话记忆注入）
- ⬜ LangChain Agents（工具调用）
- ⬜ 异步编程深入（async/await 原理）
- ⬜ 用户认证 (JWT/OAuth2)
- ⬜ 数据库迁移 (Alembic)
- ⬜ 单元测试 (pytest)
- ⬜ Docker 部署
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

- **learning_plan.json**：学习计划主数据（38 个阶段）
- **learning_history_index.json**：历史文件索引（含对话记录索引，JSON 格式）
- **roadmap查缺补漏计划.md**：roadmap.sh AI Engineer 查缺补漏完整计划
- **conversations/**：日期对话文件

---

> **祝你学习愉快！记住：理解 > 记忆，实践 > 阅读。**
> 对于 ADHD 学习者：番茄工作法（25分钟学习 + 5分钟休息）+ 立即动手验证 = 最佳学习效果 🚀
