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
- [x] FastAPI + Chroma 最小原型 (API 封装)
- [x] 手搓最小 RAG 闭环 (检索 → 拼 Prompt → 流式 LLM 调用)
- [x] 跑通 RAG 闭环测试 (启动服务 + curl 验证流式返回)
- [x] 上下文窗口管理 (Token 截断策略、超长 Prompt 处理)
- [x] LangChain 集成 (LCEL 链式语法、框架化 RAG)
- [ ] 异步编程深入 (async/await 原理、asyncio)
- [ ] 用户认证 (JWT/OAuth2、密码哈希)
- [ ] 数据库迁移 (Alembic 表结构升级)
- [ ] 单元测试 (pytest 测试用例编写)
- [ ] 项目部署 (Docker 容器化部署)
- [ ] 前端框架基础 (React/Vue 基础)
- [ ] 前后端对接 (Fetch/Axios API 调用)
- [ ] LangChain 对话记忆 (ConversationBufferMemory)
- [ ] LangChain Agent 工具调用 (Tool 定义、AgentExecutor)
- [ ] Prompt Engineering 进阶 (CoT、ReAct、Zero-Shot、Few-Shot)
- [ ] RAG Chunking 策略 (分块策略、重叠窗口、语义分块)
- [ ] RAG 评估与指标 (RAGAS、Faithfulness)
- [ ] 多向量数据库对比 (Pinecone、Weaviate、Qdrant、FAISS)
- [ ] AI Agents 基础 (ReAct 模式、Function Calling)
- [ ] Multi-Agent 与复杂工作流 (多 Agent 协作)
- [ ] Dify 平台实战 (可视化 RAG 管道、Agent 工作流)
- [ ] AI 安全与伦理 (Prompt Injection、Bias、Content Moderation)
- [ ] LLM 可观测性 (LangSmith、Langfuse、Tracing)
- [ ] LLM 评估与回归测试 (DeepEval、Regression Testing)
- [ ] MCP (Model Context Protocol)
- [ ] 多模态 AI (Image Understanding、TTS、STT)
- [ ] Fine-tuning 基础 (LoRA、QLoRA)
- [ ] LlamaIndex
- [ ] Hugging Face 生态

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
- `yield` 在资源管理中的应用
- APIRouter 模块化组织
- System Prompt 与多轮对话记忆
- SSE 流式响应
- Embedding 向量化 (本地 HuggingFaceBgeEmbeddings)
- 余弦相似度计算与数学原理
- ChromaDB 基本操作 (Collection、add、query)
- 双存储架构 (SQLite Document/DocumentChunk + ChromaDB 向量)
- RAG 完整闭环 (切片→Embedding→存储→检索→拼Prompt→调LLM)
- 上下文窗口管理 (Token 截断策略)
- LangChain 集成 (LCEL 链式语法、Retriever、PromptTemplate)
- 本地 Embedding 部署与 MPS 硬件加速
- 配置集中化 (.env 环境变量管理)
- 深度思考/推理链 (reasoning_content)

### 待深入学习
- 异步编程 (async/await 原理、asyncio)
- 用户认证 (JWT/OAuth2、密码哈希)
- 数据库迁移 (Alembic)
- 单元测试 (pytest)
- Docker 部署
- LangChain Memory (对话记忆注入)
- LangChain Agents (工具调用)
- Prompt Engineering 进阶 (CoT、ReAct)
- RAG Chunking 策略
- RAG 评估与指标 (RAGAS)
- AI Agents 基础
- Dify 平台实战
