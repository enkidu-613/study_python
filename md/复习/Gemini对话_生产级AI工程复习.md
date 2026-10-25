# Gemini 对话复习：从 RAG 基础到生产级 AI 工程

整理日期：2026-09-17。

这是一份**复习讲义**，不是试卷，也不代表其中所有主题都已经学完。它把 Gemini 分享对话里出现过的知识重新编排，方便你恢复主线、定位薄弱点，并区分“已经实践过”“只完成概念预览”和“以后再深入”。

## 来源与阅读边界

本讲义依据 Gemini 分享页中当前可显示的用户与助手文字对话整理：[原始分享对话](https://share.gemini.google/U5IY26FqidYN)。

我能读取分享页中渲染出来的完整文字问答和最后的复习总结；分享页里的以下附件被标记为不可查看或下载，因此没有把它们的内容当作已读取事实：

- `00-33章_已学重点总复习`
- `00-33章_教学文档校验记录`
- `33_多模态AI_学习复习`
- `README`

本项目本地教学文档是术语和代码边界的校正依据。对话中的示例、经验和推测，如果没有当前项目代码或官方资料支持，会在本文中标为“概念说明”或“需要验证”，不当作框架的绝对行为。

## 一句话主线

**AI 应用不是“把模型接上就结束”，而是把数据契约、检索证据、工具权限、状态流转、输出校验和网络交付拼成一条可观测的调用链。**

```text
用户输入
  -> 输入校验
  -> 检索资料或调用工具
  -> 组织模型请求
  -> 模型生成
  -> 输出校验与安全检查
  -> 普通响应或流式响应
  -> 日志、评估和故障定位
```

这条链上每一层职责不同。Prompt 负责引导，Pydantic 负责结构校验，后端权限负责限制能力，RAG 负责提供证据，LangGraph State 负责在流程中传递数据，SSE 负责把已经生成的结果交给前端。

## 建议复习顺序

时间少时不要从名词表开始，按下面的顺序追踪一条请求：

1. 先回忆 Pydantic、SQLAlchemy、Alembic 的边界。
2. 再回忆 RAG 的四段：索引、检索、上下文、生成。
3. 然后追踪 Agent 的 `bind_tools`、`ToolNode`、State 和 Handoff。
4. 再复习结构化输出、提示词注入和人工确认。
5. 最后看语义缓存和 SSE，它们是性能与交互层的扩展。

每个主题都先回答四个问题：

- 它解决什么问题？
- 它在调用链的哪一层？
- 它接收什么，返回或更新什么？
- 它不能替代什么？

---

## 一、后端基础：三个“模型”不要混淆

### 1. Pydantic、SQLAlchemy 和 Alembic

| 工具 | 它管理什么 | 典型形态 | 不负责什么 |
| --- | --- | --- | --- |
| Pydantic | 外部数据的结构与字段约束 | `class UserIn(BaseModel)` | 不负责把数据持久化到数据库 |
| SQLAlchemy ORM | Python 对象与数据库表之间的映射和数据库操作 | `class User(Base)`、`Session` | 不自动替你设计完整的接口契约 |
| Alembic | 数据库结构的版本迁移 | `revision`、`upgrade`、`downgrade` | 不负责普通业务数据的增删改查 |

最小关系可以记成：

```text
HTTP 请求 JSON
  -> Pydantic 校验并创建输入对象
  -> Service 使用 SQLAlchemy Session 操作数据库
  -> 数据库结构变化由 Alembic 记录并应用
```

`Base.metadata.create_all()` 只适合初始化时创建不存在的表；它不会像迁移工具一样可靠地记录和应用已有表的字段变更。正式的结构变化应由 Alembic 管理，不能把 `create_all()` 理解成“自动同步所有模型改动”。

### 2. 类比 Prisma 时要保留边界

可以把 SQLAlchemy ORM 理解为和 Prisma Client 类似的数据库访问层，但不是一一对应：

- SQLAlchemy 的 ORM 模型和 `Session` 负责映射、查询、事务等运行时工作。
- Alembic 更接近 Prisma 的迁移流程。
- `create_all()` 更像一次“如果没有就创建”的初始化动作，不能等同于正式迁移。

类比只帮助建立入口，最终仍要看当前库的真实 API 和项目版本。

### 3. Pydantic 是关于 `dict` 还是 `object`

两者都可以参与，但角色不同：

```python
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


payload = {"username": "enkidu", "password": "secret"}
request = LoginRequest.model_validate(payload)
```

- `payload` 是普通 Python `dict`。
- `LoginRequest` 是你定义的 Pydantic 类。
- `request` 是经过校验后的 Pydantic 实例，也就是对象。
- `request.model_dump()` 可以再次得到字典。

Pydantic 校验的是你声明的结构、类型和约束；字段“看起来合法”不代表内容一定真实、用户一定有权限，或业务动作一定安全。

---

## 二、向量、Base64 和 RAG：先分清数据是什么

### 1. Base64 不是 Embedding

这是对话里需要牢牢记住的边界：

| 名词 | 本质 | 能否还原原数据 | 用途 |
| --- | --- | --- | --- |
| Base64 | 字节到文本的编码 | 可以 | 把本地图片字节放进 Data URL 或传输字段 |
| Embedding | 模型计算出的数值向量 | 通常不能还原原文 | 比较语义相似度、做向量检索 |

```text
本地图片文件
  -> 读取 bytes
  -> Base64 编码
  -> data:image/...;base64,...
  -> 作为视觉模型的图片输入
```

```text
文本
  -> Tokenizer
  -> 模型隐藏向量
  -> 池化或模型指定的聚合
  -> Embedding 向量
  -> 向量数据库检索
```

Base64 不是加密，也不是向量；Embedding 也不是把文件“编码成可以解码回原文的字符串”。

### 2. RAG 的四段定位法

RAG（检索增强生成）不是一个单独的模型，而是一条组合流程：

```text
资料准备与索引
  -> 查询改写与检索
  -> 上下文组装
  -> 模型依据上下文回答
```

#### A. 资料准备与索引

原始文档需要经过加载、切分、Embedding 和入库。此时重点检查：

- 文档是否真的被读到；
- 切片是否包含完整语义；
- 每个切片的来源、ID 和元数据是否保留；
- 入库时使用的 Embedding 模型是否与查询侧处在兼容的向量空间。

如果更换了 Embedding 模型，通常需要重新生成已有资料的向量。只看“维度相同”不能证明两个模型的向量空间兼容。

#### B. 检索与重排

查询也要经过与文档一致的向量化流程，然后搜索近邻切片。关键词检索、向量检索、混合检索和重排是不同层次的能力：

- BM25 等关键词方法擅长实体名、专有名词和精确词面。
- 向量检索擅长语义相近，但可能漏掉精确实体或混入相似主题。
- 混合检索把词面匹配和语义匹配结合起来。
- Rerank（重排）使用更精细的模型对候选结果再次排序，不是重新生成答案。
- `top_k` 表示送入后续环节的候选切片数量，不等于“最终答案质量”，也不保证前 `k` 条都相关。

#### C. 上下文组装

检索结果必须真正放进模型请求。例如：

```text
用户问题
  + 检索到的资料片段
  + 来源和边界说明
  + “只能依据资料回答”的系统指令
  -> 模型请求
```

只在日志里打印检索结果，或者只把节点连起来而没有把结果接到 Prompt 中，都不算完成 RAG 闭环。

#### D. 模型生成

模型能看到上下文，也不等于它一定正确使用上下文。系统提示应说明证据边界，后端还应检查：

- 资料不足时是否明确拒答或说明没有依据；
- 回答是否引用了上下文之外的事实；
- 用户是否有权读取这些资料；
- 输出是否满足接口结构。

### 3. RAG 出错时的固定排查顺序

用四个问题快速定位，不要一上来就怀疑模型：

```text
1. 库里有吗？       文档是否入库，切片和索引是否存在？
2. 查出来了吗？     查询方式、Embedding、top_k、过滤器是否合理？
3. 送进去了吗？     检索结果是否真的进入模型请求？
4. 卡死了吗？       Prompt 或模型是否错误地拒绝、忽略或扩写？
```

如果是 `Collection not found`，优先检查数据集 ID、向量集合生命周期、索引存储和服务端配置；它不是单纯“模型回答不好”。如果是 Embedding 凭据没有初始化，则先修复模型供应商配置，检索工具还没进入正常语义检索阶段。

### 4. RAG 评估指标的含义

| 指标 | 主要问什么 |
| --- | --- |
| Context Recall | 需要的证据有没有被检索回来 |
| Context Precision | 检索结果里有多少真正相关 |
| Faithfulness | 答案是否忠实于给出的上下文 |
| Answer Relevance | 答案是否真正回应用户问题 |

记忆方法：前两个主要看“找资料”，后两个主要看“用资料回答”。指标名称本身不能指出唯一原因，必须结合具体样本和日志。RAGAS 等 LLM-as-a-Judge 工具可以辅助评估，但不是不加审查就绝对可靠的裁判；本项目当前应先用确定性测试集和人工核对建立基线。

---

## 三、Agent、工具和 LangGraph State

### 1. `bind_tools` 和 `ToolNode` 是两件事

```text
bind_tools(tools)
  -> 把工具的名称、参数 Schema 和描述交给模型
  -> 模型可以返回 tool call

ToolNode(tools)
  -> 读取模型返回的 tool call
  -> 找到对应 Python 工具并执行
  -> 把执行结果组织成 ToolMessage 或状态更新
```

所以：

- `bind_tools` 是模型侧的“可调用工具声明/绑定”。
- `ToolNode` 是图或 Agent 流程中的“工具执行节点”。
- 模型可以提出调用请求，但通常不应该被理解为它自己执行了 Python 函数。

### 2. State 和模型请求不是同一个东西

这是理解 LangGraph 和 Agent 的关键：

```text
State：框架内部在节点之间流转的共享数据
       例如 messages、question、active_agent

Request：某一轮真正发给模型的请求对象
         例如 system message、messages、tools、模型参数
```

模型不会直接读取 Python 的 `state` 字典。框架或 Agent 运行时会从 State 取出需要的字段，再构造模型请求。中间件也可以在模型调用前，根据 State 改写本次 Request。

### 3. Handoff 的完整调用链

Handoff 的重点不是“换了一个字符串”，而是让控制权或角色配置发生变化。当前项目中的状态驱动实现可以按下面追踪：

```text
① 用户问题进入 Agent
   State = messages + 其他状态字段

② Agent 调用模型
   模型收到当前 system message、messages 和 tools

③ 模型决定调用 transfer_to_support
   这只是模型产生的工具调用请求

④ 框架实际执行 transfer_to_support
   工具返回 Command(update={...})

⑤ 框架把 update 合并回共享 State
   例如写入 ToolMessage 和 active_agent="support_agent"

⑥ 下一次模型调用前触发 middleware
   middleware 读取 active_agent

⑦ select_prompt 选择角色配置
   得到 support 的 system prompt 和工具集合

⑧ request.override(...)
   生成本次临时修改后的模型 Request

⑨ handler(update_request)
   继续调用后续 handler，最终把修改后的请求交给模型
```

一个缩小后的代码形状是：

```python
def transfer_to_support(runtime: ToolRuntime[None, HandoffState]) -> Command:
    tool_call_id = runtime.tool_call_id
    return Command(
        update={
            "active_agent": "support_agent",
            "messages": [
                ToolMessage(
                    content="已转交支持角色",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
```

这里的 `Command(update=...)` 是 LangGraph 的状态控制对象：工具不直接拿着全局 State 改值，而是把“希望框架合并的更新”返回给框架。`ToolRuntime` 是框架注入给工具的运行时对象，`tool_call_id` 用来把工具结果和当前那次模型工具调用对应起来。

`ToolMessage` 是消息历史中的一条工具结果消息；它和普通字符串的区别在于，它保留了消息角色以及对应的工具调用关系。

### 4. middleware、handler 和 `override`

可以把一次模型调用理解为：

```text
Agent 准备调用模型
  -> middleware(request, handler)
  -> middleware 根据 State 选择配置
  -> request.override(...) 生成临时 Request
  -> handler(临时 Request)
  -> 下一个处理层或模型客户端
  -> 返回模型响应
```

`handler` 是框架提供给中间件的“继续执行入口”，不是 Express 专属概念。中间件可以在调用前修改 Request，也可以在调用后检查或包装 Response。`request.override(...)` 不会永久修改 Agent 配置，只为当前这次请求创建一份覆盖后的请求。

需要注意：不同 LangChain 版本的 `ModelRequest` 字段和 `override()` 参数可能不同。若编辑器提示没有 `system_prompt` 参数，应查看当前安装版本的类型定义，使用该版本实际支持的 `system_message` 等字段；不要只照抄另一版本的示例。

### 5. Supervisor、Subagent、Router 和 Handoff

| 模式 | 核心行为 | 适用场景 |
| --- | --- | --- |
| Subagent | 主 Agent 把一个专门 Agent 当作工具调用 | 主 Agent 统一编排，子 Agent 完成局部任务 |
| Router | 根据条件把请求送到一条或多条专门路径 | 分类明确、路径相对稳定 |
| Handoff | 当前角色通过工具或状态把后续控制权交给另一角色 | 不同角色需要轮流直接处理对话 |
| Supervisor | 一个上层角色协调多个专门角色 | 需要统一分派、汇总和决策 |

“Handoff 是不是只换 Prompt 和 tools？”要分两种实现回答：

- 单 Agent + middleware 的实现，确实主要是在下一轮模型请求前切换 system message 和可用工具，同时把角色名写入 State。
- 多个 Agent 子图的实现，还可能通过 `Command(goto=...)` 跳转到另一个图节点。

当前项目第 31 章重点是读懂第一种状态驱动实现，并知道第二种存在；不能把两种实现混成同一条框架路径。

### 6. Checkpointer、`thread_id` 和 `interrupt`

- Checkpointer 保存某个线程的 State 快照。
- `thread_id` 是查找这条会话快照的标识；同一个 ID 才能让后续调用尝试恢复同一线程。
- 换一个 `thread_id` 通常表示开始另一条线程。
- `InMemorySaver` 适合学习和单进程演示；进程重启后是否保留数据取决于具体实现，不能把它当作生产级持久化数据库。
- `interrupt()` 用于暂停图的执行，把控制权交给外部人工或上层系统；恢复时使用当前版本要求的 resume 机制。它和普通的 Handoff 不同：Handoff 是角色/路径转交，interrupt 是执行暂停与恢复。

复习边界：不要把“有 checkpointer”理解成 Agent 自动拥有永久记忆，也不要把清空一个字段理解成所有检查点都被可靠删除。生产环境的删除、恢复、并发和持久化语义要看具体 checkpointer 后端与官方版本文档。

---

## 四、结构化输出与 AI 安全

### 1. Prompt、Pydantic 和权限各管什么

```text
Prompt：引导模型怎么理解和表达
Pydantic：确定性校验字段、类型和结构
服务端权限：决定用户和工具到底能做什么
人工确认：高风险动作执行前增加批准步骤
日志：记录发生过什么，方便追踪和评估
```

Prompt 写得再严格，也不能代替权限系统。Pydantic 发现不了一个结构合法但业务危险的请求，例如：

```json
{
  "priority": "high",
  "summary": "删除所有用户数据"
}
```

字段和类型都可能合法，但真正执行删除前仍必须经过后端授权、工具白名单和必要的人工确认。

### 2. 结构化输出的处理链

```text
Prompt 引导格式
  -> 模型返回候选 JSON
  -> 解析器转换为 Python 数据
  -> Pydantic Schema 校验
  -> 成功返回，或进入错误处理/重试
```

`PydanticOutputParser` 负责把模型输出解析并校验为指定结构；`OutputFixingParser` 可以在解析失败时尝试让模型修正格式。后者是补救机制，不是安全验证，也不是所有 Agent 或结构化输出调用都会自动使用。

`@classmethod` 是 Python 的类方法装饰器，让方法通过类或实例调用，并把类对象作为第一个参数。看到解析器的 `from_*` 工厂方法时，先看它是不是类方法，再确认它创建的对象是什么；不要因为名字像函数就忽略对象生命周期。

### 3. 间接提示词注入

直接注入是用户在输入里要求模型违背规则；间接注入则可能藏在网页、文档、知识库切片或工具返回内容里。RAG 把外部资料送进上下文后，资料本身也要视为不可信输入。

防御应分层：

1. 把系统指令、用户问题和不可信资料分区，例如 `<system_instructions>`、`<untrusted_context>`、`<user_query>`。
2. 明确告诉模型：资料只作为证据，不是新的系统指令。
3. 对资料做内容风险检查或 Guardrails 分类。
4. 工具使用最小权限，按用户身份在服务端再次校验。
5. 高风险动作通过 `interrupt()` 或其他人工确认流程暂停。
6. 输出返回前做敏感信息、凭据、内部提示词和越权资料检查。

标签有助于模型区分区域，但不是安全边界，也不是沙箱。真正的安全边界仍然是后端权限、工具能力和数据访问控制。

---

## 五、语义缓存：减少重复模型调用

### 1. 心智模型

语义缓存不是“把所有回答永久记住”，而是尝试判断新问题是否足够接近以前的问题；如果命中且满足安全条件，才复用旧结果。

```text
新问题
  -> 生成查询向量
  -> 搜索缓存中的相似查询
  -> 通过相似度和元数据校验
       -> 命中：返回缓存答案
       -> 未命中：调用模型，再写入缓存
```

### 2. Redis 和向量数据库的边界

- Redis 是通用的内存数据存储；Redis Stack/RediSearch 等组件可以提供向量搜索能力。
- Milvus、Qdrant、Chroma 等更偏向向量数据库或向量检索组件。
- “缓存”描述的是使用方式和生命周期，不等于某个数据库天然就是缓存。

### 3. 不能只看相似度

两个问题在向量上很接近，不代表它们可以共享答案。缓存键或元数据至少要考虑：

- 用户身份和权限范围；
- 租户或项目空间；
- 模型名称和版本；
- Prompt 版本；
- 语言、产品、时间范围等实体条件；
- 答案是否允许过期。

例如“这个模型的上下文长度是多少”和“另一个模型的上下文长度是多少”可能语义很像，但不能仅凭相似度复用答案。

缓存命中也不一定总是直接返回。对时效性高、权限敏感或需要当前上下文的回答，应缩短 TTL、加入硬过滤，或只复用中间检索结果而不是最终答案。

### 4. 关于代码补全缓存的谨慎理解

对话中提到 AST、Tree-sitter、FIM、前缀缓存和 KV Cache 等概念。这些是代码补全系统可能采用的技术方向，不应据此断言某个具体产品一定采用了某种完整架构。复习时只需要记住：代码补全通常会利用结构化上下文、前缀和缓存来减少重复计算；具体产品实现要以其官方资料或实测为准。

---

## 六、SSE、LangGraph 和前端流式交互

### 1. SSE 和 WebSocket 的选择

| 方式 | 方向 | 典型用途 |
| --- | --- | --- |
| SSE | 服务端到客户端为主，基于 HTTP 长响应 | 模型逐段输出、进度事件、日志推送 |
| WebSocket | 双向长连接 | 实时协作、双向控制、多人状态同步 |

如果只是把模型生成的文字从服务端持续推给浏览器，SSE 通常更直接；如果前后端需要持续双向发送复杂事件，WebSocket 更合适。选择取决于交互方向、连接生命周期、代理环境和取消需求，不是“流式就必须 WebSocket”。

### 2. LangGraph 事件流的调用链

概念上可以这样追踪：

```text
LangGraph 执行节点
  -> 产生模型、工具或节点事件
  -> FastAPI 异步生成器读取事件
  -> 组装成 SSE data: ...\n\n
  -> 浏览器逐事件解析并更新界面
```

项目中使用 `astream_events(version="v2")` 时，应以当前 LangChain/LangGraph 版本的事件名称和字段为准。常见事件名可能包括模型流、工具开始和工具结束事件，但不能把不同版本的事件表硬套在一起。

前端使用 `fetch` 读取响应体时，要注意：一次 `reader.read()` 不一定正好对应一条完整 SSE 事件。应使用 `TextDecoder` 和 `buffer`，等到空行分隔符出现后再解析完整事件。

### 3. SSE 的生产边界

至少考虑：

- 客户端断开后是否取消上游模型调用；
- 鉴权、CORS 和连接超时；
- 心跳与代理缓冲；
- 上游错误如何转换成事件；
- 用户点击停止后，服务端是否真的停止；
- 日志中不要输出 API Key、完整敏感上下文或模型内部思考内容。

“前端显示停止”不等于“服务端已经停止生成”。要做到真正取消，需要让取消信号沿前端、FastAPI、上游 HTTP 客户端和模型调用链传播。

---

## 七、对话中最值得再次巩固的几个点

### 已经形成较好理解的部分

- 能区分 Pydantic 校验、SQLAlchemy ORM 和 Alembic 迁移。
- 能区分 Base64 文件编码和 Embedding 向量。
- 能说出 `bind_tools` 是给模型工具 Schema，工具节点才负责执行。
- 能理解 State 是流程内部共享数据，模型实际接收的是组织后的 Request。
- 已经实践过 Dify 自带知识检索和 Agent 通过工具访问知识库。
- 已经接触过多模态消息、图像 URL、本地图片 Data URL 和视觉模型调用。

### 需要保持在复习队列里的部分

1. Handoff 中 `Command(update=...)` 如何把 `ToolMessage` 和 `active_agent` 合并进 State。
2. middleware 如何读取 State，再用 `select_prompt` 和 `request.override(...)` 改造本次 Request。
3. `thread_id`、checkpointer、interrupt 的边界：恢复线程、暂停执行和永久记忆不是同一个概念。
4. RAG 的四段排查顺序，以及 `top_k`、rerank、Context Recall、Context Precision 的职责区别。
5. Prompt 标签、Guardrails、工具白名单和后端权限分别能防什么，不能防什么。
6. 语义缓存不能只看向量相似度，必须加入权限、实体和版本条件。
7. SSE 的网络分块、断连取消和版本相关事件字段。

---

## 八、复述检查：先遮住答案再说

### 基础边界

- Pydantic 和 SQLAlchemy 分别站在请求边界和数据库访问的哪一侧？
- 为什么 `create_all()` 不能替代 Alembic？
- Base64 为什么不能用于语义检索？

### RAG

- 一个检索结果为什么可能“查到了但没有帮助模型回答”？
- `top_k` 和 rerank 分别改变哪一步？
- Context Recall 和 Faithfulness 分别检查什么？

### Agent 与 State

- 模型提出 tool call 后，谁真正执行 Python 工具？
- Handoff 发生后，`active_agent` 如何影响下一轮请求？
- State 和 Request 各自包含什么？
- 为什么同一个 `thread_id` 只说明可能恢复同一线程，不代表拥有永久记忆？

### 安全、缓存和交互

- 为什么 `<untrusted_context>` 标签不能替代服务端权限？
- 语义缓存命中前还需要检查哪些硬条件？
- 为什么 SSE 的一次读取不一定是一条完整事件？

### 自检标准

复述时不要求一字不差，但每个主题都应能说清：

```text
是什么 -> 解决什么问题 -> 进入哪一步 -> 输入输出是什么 -> 不能替代什么
```

如果只能说出比喻，说明还没有回到准确术语；如果能说出术语但不知道谁调用谁，说明需要重新追踪最小代码；如果能追踪代码但不知道失败时查哪里，说明需要补一次调试练习。

---

## 九、下一次实践建议

按最小闭环安排，不需要一次做完整生产系统：

1. **Handoff 小实验**：让两个角色共享 `messages`，工具只更新 `active_agent`，观察下一轮 Prompt 和 tools 是否变化。
2. **RAG 排错实验**：故意让检索结果不进入 Prompt，对比“检索日志有结果”和“模型实际看到了结果”的区别。
3. **安全实验**：把一段伪装成指令的文本放进不可信上下文，验证结构化分隔不会代替后端权限。
4. **缓存实验**：给两个不同模型名的相似问题加元数据过滤，观察不满足条件时不能命中。
5. **SSE 实验**：把一条事件拆成多个网络片段，验证 `buffer` 能否等到完整事件后再解析。

这些实验的验收证据应是：日志、State 快照、请求内容、响应事件或测试断言，而不是“运行后看起来没报错”。

## 十、不要从这份复习文档推出的结论

- 读过一段 Handoff 代码，不等于已经能独立设计多 Agent 系统。
- Dify 能配置一个知识检索节点，不等于已经掌握所有 RAG 召回、重排和评估问题。
- 使用一个结构化输出解析器，不等于输出事实、权限和安全都正确。
- 有语义缓存，不等于可以忽略数据新鲜度和权限隔离。
- SSE 能逐段显示，不等于断连、取消、鉴权和上游资源已经处理好。
- Gemini 对话中出现过某个名词，不等于该名词已经在本项目教学文档中完整教过；仍按“有定义、看过代码、追踪调用、完成验证”判断是否掌握。

## 参考入口

- [LangChain Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangChain Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Alembic 文档](https://alembic.sqlalchemy.org/en/latest/)
- [Python Base64 标准库](https://docs.python.org/3/library/base64.html)
- [Ragas 文档](https://docs.ragas.io/)

