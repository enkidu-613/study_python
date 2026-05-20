# 🎯 study_python - 从 Python 到 AI 全栈的 ADHD 友好学习项目

> **适合 ADHD 学习者的 Python 与 FastAPI 完整学习资料**  
> 从 Python 基础 → FastAPI 后端 → AI 接入 → RAG 向量数据库，一步一个脚印  
> 📅 创建时间：2024年 | 🐍 Python 3.11+ | ⚡ FastAPI | 🧠 AI 集成

---

## 📚 项目简介

这是一个**从零开始的 Python 后端学习项目**，专为 ADHD 学习者设计。通过丰富的类比、流程图、表格和实战代码，帮助理解从 Python 基础到 AI 应用开发的完整技术栈。

**当前阶段**：RAG 向量数据库入门（第9步）

---

## 🗂️ 项目结构

```
study_python/
├── 📁 md/                          # 学习文档（ADHD友好格式）
│   ├── README.md                   # 学习路线图总览
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
│   └── ai学习应用数学/
│       └── 01_向量与余弦相似度.md   # 数学基础复习
│
├── 📁 routers/                     # FastAPI 路由模块（分层架构）
│   ├── ai_router.py                # AI 流式对话 /ai/*
│   ├── chat_memory.py              # 聊天记忆 /chat-memory/*
│   └── todos_routers.py            # Todo CRUD /todos/*
│
├── 📁 python第一月上半学习阶段/     # 早期练习代码
│   ├── py学习.py                   # Python 基础
│   ├── py学习_进阶.py              # Python 进阶
│   ├── py学习_进阶2.py             # Python 高级特性
│   ├── python_接触fastapi之前的补充.py
│   ├── py_CRUD.py                  # FastAPI CRUD 练习
│   └── py_ORM.py                   # FastAPI + SQLAlchemy 练习
│
├── 📁 .trae/memory/                # 项目记忆与对话历史
│   ├── conversations.md            # 完整对话历史（13次）
│   ├── project_overview.md         # 项目概览
│   ├── learning_notes.md           # 学习笔记
│   └── learning_rag_week1.md       # RAG 第一周学习指南
│
├── main.py                         # FastAPI 应用入口
├── database.py                     # 数据库配置（SQLite）
├── models.py                       # ORM 模型（SQLAlchemy）
├── ai_bot.py                       # AI 聊天机器人（ModelScope API）
├── rag_demo.py                     # RAG 入门：Embedding 与相似度
├── rag_test.py                     # RAG 测试：ModelScope Embedding API
├── pyproject.toml                  # Poetry 依赖管理
├── poetry.lock                     # 依赖锁定文件
├── requirements.txt                # pip 依赖（备选）
└── .env                            # 环境变量（API Key）
```

---

## 🚀 学习路线图

### ✅ 已完成

| 步骤 | 主题 | 对应代码 | 掌握程度 |
|------|------|----------|----------|
| 0 | 环境配置与 PyCharm 使用 | `script.py` | ✅ |
| 1 | Python 基础（变量、列表、字典、函数、类） | `py学习.py` | ✅ |
| 2 | Python 进阶（运算符、异常、文件、继承） | `py学习_进阶.py` | ✅ |
| 3 | Python 高级特性（列表推导式、生成器、装饰器） | `py学习_进阶2.py` | ✅ |
| 4 | FastAPI 基础（JSON、路径参数、查询参数） | `python_接触fastapi之前的补充.py` | ✅ |
| 5 | FastAPI CRUD（Pydantic、增删改查） | `py_CRUD.py` | ✅ |
| 6 | FastAPI ORM + SQLAlchemy（数据库、IoC/DI） | `py_ORM.py` | ✅ |
| 7 | 代码分层与模块化架构（APIRouter） | `main.py` + `routers/` | ✅ |
| 8 | 提示词工程与聊天记忆（System Prompt、多轮对话） | `routers/chat_memory.py` | ✅ |

### 🔥 进行中

| 步骤 | 主题 | 对应代码 | 状态 |
|------|------|----------|------|
| 9 | **RAG 向量数据库入门** | `rag_test.py`, `rag_demo.py` | 🔥 当前 |
| | - Embedding 初体验（文本向量化） | `rag_test.py` | ✅ 完成 |
| | - 余弦相似度数学基础 | `md/ai学习应用数学/` | ✅ 完成 |
| | - ChromaDB 实战（待开始） | | ⬜ |
| | - 双存储架构设计（待开始） | | ⬜ |
| | - FastAPI + Chroma 最小原型（待开始） | | ⬜ |

### 📋 待学习

| 阶段 | 内容 | 说明 |
|------|------|------|
| **RAG 闭环** | 手搓最小 RAG | 手动实现切片→Embedding→存储→检索→Prompt→LLM |
| | LangChain 集成 | 自动化 RAG 流程 |
| **后端深耕** | 用户认证 (JWT) | Depends + OAuth2 的自然延伸 |
| | 项目部署 (Docker) | 能部署才有完整项目 |
| **前端** | React/Vue 基础 | 后端全通后再学 |
| | 前后端对接 | 有后端 API 才有对接意义 |

---

## 🛠️ 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **语言** | Python 3.11+ | 核心编程语言 |
| **Web 框架** | FastAPI | 高性能异步 Web 框架 |
| **数据库** | SQLite | 开发阶段轻量数据库 |
| **ORM** | SQLAlchemy | 数据库对象关系映射 |
| **AI API** | ModelScope (OpenAI 兼容) | 国内 AI 模型接入 |
| **向量模型** | Qwen/Qwen3-Embedding-8B | 文本向量化 |
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
- System Prompt 人设控制（傲娇猫娘）
- 内存存储（后续将持久化）

### 3. Todo CRUD (`/todos`)
- 完整的增删改查
- SQLAlchemy ORM 操作
- 依赖注入（DI）实践

### 4. RAG 向量检索（开发中）
- 文本 Embedding 向量化
- 余弦相似度计算
- ChromaDB 语义检索（待接入）

---

## 🧠 ADHD 学习特色

本项目专为 ADHD 学习者设计：

- **类比法**：用超市、快递、手电筒等生活场景解释技术概念
- **视觉化**：流程图、表格、ASCII 图示比纯文字更有效
- **循序渐进**：从基础到进阶，一步一个脚印
- **实践导向**：学完立即动手实现
- **数学基础**：为 AI 应用补充必要的数学概念（向量、余弦相似度）
- **对话历史**：完整记录每次学习对话，方便回顾

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 Poetry（推荐）
poetry install

# 或使用 pip
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
MODELSCOPE_API_KEY=你的_modelscope_api_key
```

### 3. 运行项目

```bash
# 启动 FastAPI 服务
poetry run python main.py

# 或测试 RAG
poetry run python rag_test.py
```

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
| [08_提示词工程](md/08_提示词工程与聊天记忆.md) | System Prompt、多轮对话 | ⭐⭐⭐ |
| [09_RAG入门](md/09_RAG_向量数据库入门.md) | Embedding、ChromaDB、语义检索 | ⭐⭐⭐⭐ |
| [向量与余弦相似度](md/ai学习应用数学/01_向量与余弦相似度.md) | 数学基础复习 | ⭐⭐ |

---

## 💡 核心概念掌握情况

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
- ✅ Embedding 文本向量化
- ✅ 余弦相似度计算

### 待深入学习
- ⬜ ChromaDB 向量数据库实战
- ⬜ 双存储架构（CQRS）
- ⬜ 手搓最小 RAG 闭环
- ⬜ LangChain 集成
- ⬜ 用户认证 (JWT/OAuth2)
- ⬜ 数据库迁移 (Alembic)
- ⬜ 测试 (pytest)
- ⬜ Docker 部署
- ⬜ 前端框架 (React/Vue)

---

## 🔗 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Chroma 官方文档](https://docs.trychroma.com/)
- [ModelScope 模型库](https://www.modelscope.cn/)
- [OpenAI Embedding 指南](https://platform.openai.com/docs/guides/embeddings)

---

## 📝 项目记忆

本项目使用 `.trae/memory/` 目录记录完整的学习历史：

- **conversations.md**：13次完整对话记录
- **project_overview.md**：项目概览与技术栈
- **learning_notes.md**：学习笔记与重点
- **learning_rag_week1.md**：RAG 第一周学习指南

---

> **祝你学习愉快！记住：理解 > 记忆，实践 > 阅读。**  
> 对于 ADHD 学习者：番茄工作法（25分钟学习 + 5分钟休息）+ 立即动手验证 = 最佳学习效果 🚀
