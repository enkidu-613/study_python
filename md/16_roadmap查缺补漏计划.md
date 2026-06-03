# roadmap.sh AI Engineer 查缺补漏计划

> 基于 [roadmap.sh/ai/ai-engineer](https://roadmap.sh/ai/roadmap-chat/ai-engineer) 系统梳理，对照当前学习进度，制定完整查缺补漏方案。
> 生成时间：2026-06-03

---

## 一、当前学习进度概览

### 已完成阶段（16/38）

```
Python 基础 / 进阶 / 高级特性        ✅ ✅ ✅
FastAPI 基础 / CRUD / ORM           ✅ ✅ ✅
代码分层与模块化架构                 ✅
提示词工程与聊天记忆                 ✅
RAG 向量数据库入门                   ✅
ChromaDB 实战                      ✅
Embedding 模型实验                  ✅
双存储架构 (SQLite + Chroma)        ✅
FastAPI + Chroma 最小原型           ✅
手搓最小 RAG 闭环                   ✅
跑通 RAG 闭环测试                   ✅
上下文窗口管理                       ✅
```

### 进行中阶段

```
LangChain 集成 (LCEL 链式语法)      🟡  <- 当前位置
```

---

## 二、roadmap.sh 知识点覆盖对照表

### 2.1 LLM 基础模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Tokens / Tokenization | 已掌握 | 上下文窗口管理 | 无 |
| Context / Context Window | 已掌握 | 上下文窗口管理 | 无 |
| Inference vs Training | 未学习 | 无 | 部分缺失 |
| Claude / GPT / Llama / Mistral | 已了解 | Prompt 工程 | 概念 OK |
| Temperature / Top-K / Top-P | 未深入 | 无 | **需要补充** |
| Repetition Penalties | 未学习 | 无 | **需要补充** |

### 2.2 Prompt Engineering 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| System Prompting | 已掌握 | 提示词工程与聊天记忆 | 无 |
| Role & Behavior | 已掌握 | 提示词工程与聊天记忆 | 无 |
| Zero-Shot Prompting | 未系统学习 | 无 | **需要补充** |
| Few-Shot Prompting | 未系统学习 | 无 | **需要补充** |
| Chain-of-Thought (CoT) | 未学习 | 无 | **需要补充** |
| ReAct Prompting | 未学习 | 无 | **需要补充** |
| Function Calling | 未学习 | 无 | **需要补充** |
| Structured Output | 未学习 | 无 | **需要补充** |

### 2.3 Embeddings & 向量数据库模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Embedding 概念与原理 | 已掌握 | RAG 向量数据库入门 | 无 |
| Semantic Search | 已掌握 | RAG 闭环 | 无 |
| ChromaDB | 已掌握 | ChromaDB 实战 | 无 |
| Pinecone | 未学习 | 无 | **需要补充** |
| Weaviate | 未学习 | 无 | **需要补充** |
| FAISS | 未学习 | 无 | **需要补充** |
| Qdrant | 未学习 | 无 | **需要补充** |
| MongoDB Atlas | 未学习 | 无 | **需要补充** |
| Jina / Sentence Transformers | 未学习 | 无 | **需要补充** |

### 2.4 RAG 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Chunking | 未系统学习 | 无 | **需要补充** |
| Embedding | 已掌握 | RAG 向量数据库入门 | 无 |
| Vector Database | 已掌握 | ChromaDB 实战 | 无 |
| Retrieval Process | 已掌握 | RAG 闭环 | 无 |
| Generation | 已掌握 | RAG 闭环 | 无 |
| RAG vs Fine-tuning | 未学习 | 无 | **需要补充** |
| RAG 评估 (RAGAS) | 未学习 | 无 | **需要补充** |
| Context Engineering | 已掌握 | 上下文窗口管理 | 无 |
| Context Isolation | 未学习 | 无 | **需要补充** |

### 2.5 框架/工具模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| LangChain | 进行中 | LangChain 集成 | 进行中 |
| LangChain Memory | 未学习 | 无 | **需要补充** |
| LangChain Agents | 未学习 | 无 | **需要补充** |
| LlamaIndex | 未学习 | 无 | **需要补充** |
| Hugging Face Hub | 未学习 | 无 | **需要补充** |
| Transformers.js | 未学习 | 无 | **需要补充** |
| OpenAI Response API | 未学习 | 无 | **需要补充** |
| Google Gemini API | 未学习 | 无 | **需要补充** |

### 2.6 AI Agents 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| ReAct Prompting | 未学习 | 无 | **需要补充** |
| Tools & Function Calling | 未学习 | 无 | **需要补充** |
| Agent Usecases | 未学习 | 无 | **需要补充** |
| Manual Implementation | 未学习 | 无 | **需要补充** |
| OpenAI AgentKit | 未学习 | 无 | **需要补充** |
| Claude Agent SDK | 未学习 | 无 | **需要补充** |
| Multi-agents | 未学习 | 无 | **需要补充** |

### 2.7 MCP 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| MCP Host | 未学习 | 无 | **需要补充** |
| MCP Server | 未学习 | 无 | **需要补充** |
| MCP Client | 未学习 | 无 | **需要补充** |
| Data Layer / Transport Layer | 未学习 | 无 | **需要补充** |

### 2.8 Multimodal AI 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Image Understanding | 未学习 | 无 | **需要补充** |
| Image Generation (DALL-E) | 未学习 | 无 | **需要补充** |
| Video Understanding | 未学习 | 无 | **需要补充** |
| Text-to-Speech | 未学习 | 无 | **需要补充** |
| Speech-to-Text (Whisper) | 未学习 | 无 | **需要补充** |

### 2.9 Fine-tuning 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Fine-tuning 概念 | 未学习 | 无 | **需要补充** |
| LoRA / QLoRA | 未学习 | 无 | **需要补充** |
| RAG vs Fine-tuning 选择 | 未学习 | 无 | **需要补充** |

### 2.10 AI Safety 模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Prompt Injection Attacks | 未系统学习 | 无 | **需要补充** |
| Bias and Fairness | 未学习 | 无 | **需要补充** |
| Content Moderation | 未学习 | 无 | **需要补充** |
| Safety Best Practices | 未学习 | 无 | **需要补充** |

### 2.11 评估与可观测性模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Tracing & Logging | 未学习 | 无 | **需要补充** |
| Cost/Latency Monitoring | 未学习 | 无 | **需要补充** |
| LangSmith | 未学习 | 无 | **需要补充** |
| Langfuse | 未学习 | 无 | **需要补充** |
| DeepEval | 未学习 | 无 | **需要补充** |
| RAGAS | 未学习 | 无 | **需要补充** |
| Regression Testing | 未学习 | 无 | **需要补充** |

### 2.12 开发工具模块

| roadmap 知识点 | 当前状态 | 对应阶段 | 缺失程度 |
|---------------|---------|---------|---------|
| Cursor | 已了解 | 日常使用 | 无 |
| Claude Code | 已了解 | 日常使用 | 无 |
| Vibe Coding | 已了解 | 概念了解 | 无 |

---

## 三、查缺补漏学习子计划

### Phase 1: LangChain 深化（当前 LangChain 阶段之后）

#### 阶段 1.1: LangChain 对话记忆
- **学习目标**: 掌握 ConversationBufferMemory、ConversationSummaryMemory 等 Memory 类型，实现带历史对话的 RAG
- **预计时长**: 1 ~ 2 天
- **学习资源**:
  - LangChain 官方文档: Memory 模块
  - 实操: 在现有 RAG 中注入多轮对话上下文
- **产出物**: 代码实现 + 学习文档
- **roadmap 对应**: LangChain Memory

#### 阶段 1.2: LangChain Agent 工具调用
- **学习目标**: 理解 Tool 定义、AgentExecutor 工作机制，实现可调用外部工具的 Agent
- **预计时长**: 2 ~ 3 天
- **学习资源**:
  - LangChain 官方文档: Agents 模块
  - 实操: 实现天气查询、计算器、搜索引擎等 Tool
- **产出物**: 代码实现 + 学习文档
- **roadmap 对应**: LangChain Agents, Tools & Function Calling

---

### Phase 2: Prompt Engineering 进阶

#### 阶段 2.1: CoT / ReAct / Few-Shot
- **学习目标**: 掌握 CoT 思维链、ReAct 推理+行动模式、Few-Shot 示例工程
- **预计时长**: 2 天
- **学习资源**:
  - 论文: Chain-of-Thought Prompting Elicits Reasoning in LLMs
  - 论文: ReAct: Synergizing Reasoning and Acting in Language Models
  - 实操: 手写 ReAct Prompt，观察推理过程
- **产出物**: 学习文档 + 代码实验
- **roadmap 对应**: CoT, ReAct, Few-Shot, Zero-Shot

#### 阶段 2.2: 采样参数与输出控制
- **学习目标**: 理解 Temperature、Top-K、Top-P、Repetition Penalty 对生成结果的影响
- **预计时长**: 0.5 天
- **学习资源**:
  - 实验: 固定 Prompt，调整参数观察输出变化
- **产出物**: 参数实验记录
- **roadmap 对应**: Temperature, Top-K, Top-P, Repetition Penalties

---

### Phase 3: RAG 进阶

#### 阶段 3.1: Chunking 策略
- **学习目标**: 掌握固定长度分块、重叠窗口、递归字符拆分、语义分块等策略
- **预计时长**: 1 ~ 2 天
- **学习资源**:
  - LangChain Text Splitters 文档
  - 实操: 对比不同 Chunking 策略的检索效果
- **产出物**: 代码实现 + 效果对比文档
- **roadmap 对应**: Chunking

#### 阶段 3.2: RAG 评估与指标
- **学习目标**: 掌握 Faithfulness、Answer Relevance、Context Precision、Context Recall 等指标，使用 RAGAS 评估
- **预计时长**: 2 天
- **学习资源**:
  - RAGAS 官方文档
  - 实操: 对现有 RAG 系统进行评估打分
- **产出物**: 评估报告 + 学习文档
- **roadmap 对应**: RAG Evaluation, RAGAS

#### 阶段 3.3: 多向量数据库对比
- **学习目标**: 了解 Pinecone、Weaviate、Qdrant、FAISS 的特点与适用场景
- **预计时长**: 2 天
- **学习资源**:
  - 各数据库官方 Quickstart
  - 实操: 至少接入一个云端向量数据库（如 Qdrant Cloud）
- **产出物**: 对比文档 + 接入代码
- **roadmap 对应**: Pinecone, Weaviate, Qdrant, FAISS, MongoDB Atlas

---

### Phase 4: AI Agents

#### 阶段 4.1: AI Agents 基础
- **学习目标**: 理解 ReAct 模式，手动实现一个简单 Agent（推理 → 行动 → 观察）
- **预计时长**: 2 ~ 3 天
- **学习资源**:
  - ReAct 论文
  - LangChain Agent 文档
  - 实操: 不依赖框架，手写 ReAct Agent
- **产出物**: 手搓 Agent + 框架版 Agent
- **roadmap 对应**: AI Agents, ReAct, Function Calling

#### 阶段 4.2: Multi-Agent 与复杂工作流
- **学习目标**: 理解多 Agent 协作模式，尝试 OpenAI Agent SDK 或 CrewAI
- **预计时长**: 2 ~ 3 天
- **学习资源**:
  - OpenAI Agent SDK 文档
  - 实操: 实现「研究员 → 写手 → 审校」多 Agent 工作流
- **产出物**: Multi-Agent 系统代码
- **roadmap 对应**: Multi-agents, OpenAI AgentKit, Claude Agent SDK

---

### Phase 5: 生产级能力

#### 阶段 5.1: AI 安全与伦理
- **学习目标**: 了解 Prompt Injection、越狱攻击、Bias、Content Moderation 原理与防御
- **预计时长**: 1 ~ 2 天
- **学习资源**:
  - OWASP LLM Top 10
  - 实操: 对现有 RAG 系统进行对抗性测试
- **产出物**: 安全检查清单 + 防御代码
- **roadmap 对应**: AI Safety and Ethics, Prompt Injection

#### 阶段 5.2: LLM 可观测性
- **学习目标**: 接入 LangSmith 或 Langfuse，实现 Tracing、Cost 监控、Latency 监控
- **预计时长**: 2 天
- **学习资源**:
  - LangSmith 官方文档
  - 实操: 为现有 RAG 链路添加完整 Tracing
- **产出物**: 可观测性看板截图 + 接入代码
- **roadmap 对应**: LangSmith, Langfuse, Observability

#### 阶段 5.3: LLM 评估与回归测试
- **学习目标**: 建立 Deterministic Evals 和 Model-Based Evals，使用 DeepEval 进行自动化测试
- **预计时长**: 2 天
- **学习资源**:
  - DeepEval 官方文档
  - 实操: 为 RAG 编写测试用例集，实现 CI 集成
- **产出物**: 测试套件 + CI 配置
- **roadmap 对应**: DeepEval, Evaluation, Regression Testing

#### 阶段 5.4: MCP (Model Context Protocol)
- **学习目标**: 理解 MCP Host/Server/Client 架构，实现一个自定义 MCP Server
- **预计时长**: 2 ~ 3 天
- **学习资源**:
  - MCP 官方文档 (modelcontextprotocol.io)
  - 实操: 为现有 RAG 系统封装 MCP Server
- **产出物**: MCP Server 实现 + Client 调用代码
- **roadmap 对应**: MCP Host, MCP Server, MCP Client

---

### Phase 6: 扩展能力

#### 阶段 6.1: 多模态 AI
- **学习目标**: 使用 Vision API 理解图片，使用 Whisper 进行语音转文字
- **预计时长**: 2 ~ 3 天
- **学习资源**:
  - OpenAI Vision API 文档
  - Whisper API 文档
  - 实操: 上传图片问答、语音输入问答
- **产出物**: 多模态接口代码
- **roadmap 对应**: Multimodal AI, Vision, TTS, STT

#### 阶段 6.2: Fine-tuning 基础
- **学习目标**: 理解 Fine-tuning 概念、LoRA/QLoRA 原理、RAG vs Fine-tuning 选择策略
- **预计时长**: 2 天
- **学习资源**:
  - Hugging Face Fine-tuning 教程
  - 实操: 使用 unsloth 或 PEFT 进行一次小规模微调实验
- **产出物**: 微调实验记录 + 决策流程图
- **roadmap 对应**: Fine-tuning, LoRA, QLoRA

#### 阶段 6.3: LlamaIndex
- **学习目标**: 掌握 LlamaIndex 索引构建、查询引擎，与 LangChain 对比使用
- **预计时长**: 2 天
- **学习资源**:
  - LlamaIndex 官方文档
  - 实操: 用 LlamaIndex 重写现有 RAG 功能
- **产出物**: LlamaIndex 版 RAG 代码 + 对比文档
- **roadmap 对应**: LlamaIndex

#### 阶段 6.4: Hugging Face 生态
- **学习目标**: 了解 Hugging Face Hub、使用 Inference SDK、本地部署开源模型
- **预计时长**: 2 ~ 3 天
- **学习资源**:
  - Hugging Face 官方文档
  - 实操: 使用 Transformers 本地加载 Embedding 模型 / LLM
- **产出物**: 本地模型部署代码
- **roadmap 对应**: Hugging Face Hub, Transformers.js, Open Source Models

---

### Phase 7: 工程能力补全（原有计划）

#### 阶段 7.1: 异步编程深入
- **学习目标**: async/await 原理、asyncio 事件循环、并发控制
- **预计时长**: 2 天

#### 阶段 7.2: 用户认证
- **学习目标**: JWT/OAuth2、密码哈希 bcrypt、登录态管理
- **预计时长**: 2 天

#### 阶段 7.3: 数据库迁移
- **学习目标**: Alembic 迁移脚本编写、回滚操作
- **预计时长**: 1 天

#### 阶段 7.4: 单元测试
- **学习目标**: pytest 测试用例、Mock、Fixture、覆盖率
- **预计时长**: 2 天

#### 阶段 7.5: 项目部署
- **学习目标**: Docker 容器化、docker-compose、环境变量管理
- **预计时长**: 2 天

#### 阶段 7.6: 前端基础与对接
- **学习目标**: React 基础组件、Fetch/Axios 调用后端 API
- **预计时长**: 3 ~ 5 天

---

## 四、整合后的完整学习路线图

```
Phase 1: 基础构建（已完成）
├── Python 基础 / 进阶 / 高级特性        ✅
├── FastAPI 基础 / CRUD / ORM           ✅
├── 代码分层与模块化架构                 ✅
└── 提示词工程与聊天记忆                 ✅

Phase 2: RAG 核心（已完成）
├── RAG 向量数据库入门                   ✅
├── ChromaDB 实战                      ✅
├── 双存储架构                          ✅
├── 手搓最小 RAG 闭环                   ✅
├── 上下文窗口管理                       ✅
└── LangChain 集成                     🟡  <- 当前位置

Phase 3: LangChain 深化（查缺补漏新增）
├── LangChain 对话记忆
├── LangChain Agent 工具调用
└── Prompt Engineering 进阶 (CoT/ReAct)

Phase 4: RAG 进阶（查缺补漏新增）
├── RAG Chunking 策略
├── RAG 评估与指标 (RAGAS)
└── 多向量数据库对比

Phase 5: AI Agents（查缺补漏新增）
├── AI Agents 基础 (ReAct/手动实现)
└── Multi-Agent 与复杂工作流

Phase 6: 生产级（查缺补漏新增）
├── AI 安全与伦理
├── LLM 可观测性 (LangSmith/Langfuse)
├── LLM 评估与回归测试 (DeepEval)
└── MCP (Model Context Protocol)

Phase 7: 扩展能力（查缺补漏新增）
├── 多模态 AI
├── Fine-tuning 基础
├── LlamaIndex
└── Hugging Face 生态

Phase 8: 工程补全（原有计划）
├── 异步编程深入
├── 用户认证
├── 数据库迁移
├── 单元测试
├── 项目部署
└── 前后端对接
```

---

## 五、进度跟踪机制

### 5.1 数据结构（已集成到 learning_plan.json）

每个阶段新增 `roadmap_tags` 字段，标记该阶段覆盖的 roadmap 知识点：

```json
{
  "id": "langchain",
  "roadmap_tags": ["LangChain", "RAG"]
}
```

### 5.2 跟踪方式

| 跟踪项 | 频率 | 方式 |
|-------|------|------|
| 阶段完成状态 | 每阶段结束时 | 更新 `learning_plan.json` 中 `status` 字段 |
| 错题记录 | 每次测试后 | 追加到 `md/错题本.md` |
| 学习文档 | 每阶段产出 | 保存到 `md/XX_阶段名.md` |
| 对话归档 | 每天结束时 | 追加到 `.trae/memory/conversations/日期.md` |
| roadmap 覆盖度检查 | 每完成 5 个阶段 | 对照本文档 2.x 表格打勾确认 |

### 5.3 快速检查清单

每完成一个阶段，在该阶段前打勾，并记录完成日期：

- [ ] LangChain 对话记忆 (预计: ___)
- [ ] LangChain Agent 工具调用 (预计: ___)
- [ ] Prompt Engineering 进阶 (预计: ___)
- [ ] RAG Chunking 策略 (预计: ___)
- [ ] RAG 评估与指标 (预计: ___)
- [ ] 多向量数据库对比 (预计: ___)
- [ ] AI Agents 基础 (预计: ___)
- [ ] Multi-Agent 工作流 (预计: ___)
- [ ] AI 安全与伦理 (预计: ___)
- [ ] LLM 可观测性 (预计: ___)
- [ ] LLM 评估与回归测试 (预计: ___)
- [ ] MCP (预计: ___)
- [ ] 多模态 AI (预计: ___)
- [ ] Fine-tuning 基础 (预计: ___)
- [ ] LlamaIndex (预计: ___)
- [ ] Hugging Face 生态 (预计: ___)
- [ ] 异步编程深入 (预计: ___)
- [ ] 用户认证 (预计: ___)
- [ ] 数据库迁移 (预计: ___)
- [ ] 单元测试 (预计: ___)
- [ ] 项目部署 (预计: ___)
- [ ] 前后端对接 (预计: ___)

### 5.4 效果评估标准

| 评估维度 | 通过标准 |
|---------|---------|
| 代码可运行 | 每个阶段必须有可执行的代码，curl/API 调用成功 |
| 文档完整性 | 每个阶段必须有学习文档，包含概念 + 代码 + 常见错误 |
| 掌握度测试 | 每阶段结束后进行 5 道题测试，正确率 >= 80% |
| 错题复习 | 3 天后和 1 周后各复习一次错题本 |

---

## 六、预计总时长

| Phase | 阶段数 | 预计天数 |
|-------|--------|---------|
| Phase 3: LangChain 深化 | 3 | 3 ~ 5 天 |
| Phase 4: RAG 进阶 | 3 | 5 ~ 6 天 |
| Phase 5: AI Agents | 2 | 4 ~ 6 天 |
| Phase 6: 生产级 | 4 | 7 ~ 10 天 |
| Phase 7: 扩展能力 | 4 | 8 ~ 11 天 |
| Phase 8: 工程补全 | 6 | 12 ~ 15 天 |
| **合计** | **22** | **39 ~ 53 天** |

> 按每天有效学习 2 ~ 3 小时估算，约 1.5 ~ 2 个月完成全部查缺补漏。

---

## 七、文档索引

| 文档 | 对应阶段 |
|------|---------|
| `md/15_LangChain核心概念.md` | LangChain 集成 |
| `md/16_roadmap查缺补漏计划.md` | 本文件（总纲） |
| `md/错题本.md` | 全阶段错题记录 |
| `.trae/memory/learning_plan.json` | 阶段状态与依赖 |
| `.trae/memory/learning_history_index.json` | 历史文件索引 |

---

> 本计划会根据实际学习进度动态调整。每完成一个 Phase，建议回顾本文档对照表，确认 roadmap 覆盖度。
