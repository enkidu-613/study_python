# 15_LangChain 核心概念与 LCEL 链式语法

> 阶段：`langchain` | 状态：🟡 进行中（第一课）
>
> 一句话总结：LangChain 不是魔法，它只是把你手搓的 RAG 流程，用 "|" 管道符串成了流水线。

---

## 一、为什么需要 LangChain

### 你现在的痛苦（手搓版）

打开 [`rag_router.py`](file:///Users/enkidu/PyCharmMiscProject/routers/rag_router.py)，你会发现一个 RAG 问答需要**手动拼接 6 个步骤**：

```python
# 步骤 1：调 Embedding 模型把问题变成向量
vec = get_embedding(query)

# 步骤 2：调 ChromaDB 搜相似片段
results = collection.query(query_embeddings=[vec], n_results=3)

# 步骤 3：自己拼 System Prompt（f-string）
system_prompt = f"根据以下资料回答：{chunks}"

# 步骤 4：调 LLM API
response = client.chat.completions.create(
    model="...", messages=[{"role": "system", ...}, {"role": "user", ...}]
)

# 步骤 5：处理流式输出
for chunk in response:
    yield chunk.choices[0].delta.content

# 步骤 6：自己算 Token、做截断、防幻觉...
```

**问题**：步骤越多，越容易漏、越容易错。比如忘了算 Token，直接报错；拼 Prompt 时漏了限制条件，AI 开始瞎编。

### LangChain 的解法（框架版）

```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
# 一行代码 = 上面 6 个步骤
result = rag_chain.invoke("问题")
```

**框架的价值**：把"拼水管"变成"拧水龙头"。你不需要记住每一步怎么调，只需要知道**水从哪进、从哪出**。

---

## 二、LCEL 链式语法：`|` 管道符

### 🎯 一句话理解
`|` 不是位运算，而是**数据接力棒**——左边步骤的输出，自动变成右边步骤的输入。

### 📖 生活类比

想象食堂打饭的流水线：

```
取餐盘 → 盛米饭 → 打菜 → 浇汤 → 端走
   |        |       |      |      |
   └────────┴───────┴──────┴──────┘
         每个师傅只做一件事
         做完传给下一个师傅
```

`|` 就是师傅之间的**递盘子动作**。

### 💻 代码对比

**没有管道符（手搓）：**
```python
step1_out = do_step1(input_data)
step2_out = do_step2(step1_out)
step3_out = do_step3(step2_out)
result = do_step4(step3_out)
```

**有管道符（LCEL）：**
```python
chain = do_step1 | do_step2 | do_step3 | do_step4
result = chain.invoke(input_data)
```

**区别**：手搓版是"**命令式**"（每一步都写清楚），LCEL 是"**声明式**"（只声明步骤和顺序，框架帮你跑）。

---

## 三、六大核心概念逐个拆解

### 1. Document（文档）

**🎯 一句话**：LangChain 里最小的知识单位，一张带标签的索引卡片。

**📖 类比**：图书馆的借书卡，正面写书名和内容摘要，背面写分类号和书架位置。

**💻 代码**：
```python
from langchain_core.documents import Document

doc = Document(
    page_content="苹果富含维生素C，每天吃一个有益健康。",  # 正面：内容
    metadata={"source": "营养百科", "page": 12}              # 背面：来源信息
)
```

**🔍 在咱们的代码里**：
```python
# retriever 返回的就是 List[Document]
docs = retriever.invoke("苹果怎么吃？")
for doc in docs:
    print(doc.page_content)  # 片段内容
    print(doc.metadata)      # {title: "...", source: "..."}
```

**⚠️ 常见错误**：
| 错误 | 原因 | 正确做法 |
|------|------|----------|
| 以为 Document 只能存字符串 | 被名字误导 | `page_content` 存文本，`metadata` 存字典，非常灵活 |
| 忽略 metadata | 以为只有内容重要 | metadata 里的 source 用于回答时标注出处 |

---

### 2. Embedding Model（嵌入模型）

**🎯 一句话**：把人类文字翻译成 AI 能懂的"语义坐标"的翻译官。

**📖 类比**：联合国同声传译。你说中文"苹果"，它翻译成向量 `[0.1, -0.3, 0.8, ...]`，这样无论原文是什么语言，AI 都能按"坐标距离"找相似内容。

**💻 代码**：
```python
from langchain_openai import OpenAIEmbeddings

# 创建翻译官
embeddings = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",           # 用什么词典
    openai_api_base="https://api-inference.modelscope.cn/v1",
    openai_api_key="你的密钥"
)

# 翻译一句话
vec = embeddings.embed_query("苹果怎么吃？")
print(len(vec))  # 4096（Qwen Embedding 输出 4096 维向量）
```

**🔍 和手搓版的区别**：
```python
# 手搓版：直接调 OpenAI 客户端
response = client.embeddings.create(model="Qwen/...", input=text)
vec = response.data[0].embedding

# LangChain 版：封装成对象，后面直接传给 VectorStore
embeddings = OpenAIEmbeddings(...)
# VectorStore 内部会自动调用 embeddings.embed_query()
```

---

### 3. VectorStore（向量数据库）

**🎯 一句话**：按"语义坐标"快速找亲戚的导航系统。

**📖 类比**：你把家里所有物品都按 GPS 坐标存在手机里。想找"冬天穿的"，不用翻箱倒柜，手机直接告诉你"羽绒服在衣柜第二层"。

**💻 代码**：
```python
from langchain_chroma import Chroma
import chromadb

# 连接到现有的 ChromaDB（和手搓版共用同一个数据库）
chroma_client = chromadb.PersistentClient(path="./chroma_db")

vectorstore = Chroma(
    client=chroma_client,              # 复用已有的客户端
    collection_name="documents",       # 集合名（手搓版也是这个）
    embedding_function=embeddings,     # 告诉它：查询时用哪个翻译官
)

# 统计有多少条文档
count = vectorstore._collection.count()
```

**🔍 关键理解**：
- `embedding_function` 只在**查询时**用到（把用户问题变成向量去搜）
- 存储时的向量是手搓版已经生成好的，LangChain 不会重新存一遍
- 所以能**直接读取**现有知识库，不需要重新导入

---

### 4. Retriever（检索器）

**🎯 一句话**：VectorStore 的"前台接待员"，你描述需求，它去后台找资料。

**📖 类比**：餐厅服务员。你说"想吃点辣的"，服务员去厨房找川菜菜单，而不是让你自己进厨房翻冰箱。

**💻 代码**：
```python
# 从 VectorStore 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",       # 检索方式：按相似度
    search_kwargs={"k": 3},         # 返回前 3 个最相关的结果
)

# 使用检索器
docs = retriever.invoke("苹果怎么吃？")
# 返回 List[Document]，已按相似度排好序
```

**🔍 和手搓版的对比**：
```python
# 手搓版：直接调 Chroma 的 query API
results = collection.query(
    query_embeddings=[vec],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)
# 返回的是原始字典，需要手动解析

# LangChain 版：retriever 帮你封装了上述所有步骤
# 输入字符串 → 自动调 Embedding → 自动查 VectorStore → 返回 Document 对象
# 你只需要关心：输入问题，拿到文档
```

---

### 5. LLM（大语言模型）

**🎯 一句话**：根据你给的资料和问题，写出回答的"作家"。

**📖 类比**：你给作家一叠参考资料和一道作文题，他根据资料写文章，不是凭空虚构。

**💻 代码**：
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3.2",
    openai_api_base="https://api-inference.modelscope.cn/v1",
    openai_api_key="你的密钥",
    temperature=0.7,        # 创造力：0=保守，1=放飞
    streaming=True,         # 开启流式输出（一个字一个字吐）
)

# 直接调用（非流式）
response = llm.invoke("你好")
print(response.content)   # "你好！有什么可以帮你的吗？"
```

**🔍 和手搓版的区别**：
```python
# 手搓版：直接构造 messages 列表调 API
messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
]
response = client.chat.completions.create(model="...", messages=messages, stream=True)

# LangChain 版：llm 对象封装了 API 调用
# 输入 LangChain 的 Message 对象，输出 AIMessage 对象
# 后面会配合 PromptTemplate 自动构造 messages
```

---

### 6. Chain / LCEL（链 / 表达式语言）

**🎯 一句话**：用 `|` 把 Document → Embedding → VectorStore → Retriever → LLM 串成流水线的**组装说明书**。

**📖 类比**：乐高说明书。你不用管每块积木内部怎么造的，只需要按顺序拼起来，最后就得到了飞船。

**💻 核心代码拆解**：

```python
# ========== 第 1 步：定义 Prompt 模板 ==========
# 手搓版用 f-string，LCEL 用 ChatPromptTemplate
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "根据以下资料回答：\n\n{context}"),   # {context} 是占位符
    ("human", "{question}"),                          # {question} 是占位符
])

# ========== 第 2 步：组装链 ==========
rag_chain = (
    {
        # 字典的每个 key 对应 Prompt 模板里的占位符
        "context": retriever | format_docs,   # 检索 → 格式化 → 填入 {context}
        "question": RunnablePassthrough(),     # 用户问题原样填入 {question}
    }
    | RAG_PROMPT    # 把字典里的值填进 Prompt 模板，生成完整 messages
    | llm           # 把 messages 送给 LLM，生成回答
    | StrOutputParser()  # 把 AIMessage 对象转成纯字符串
)
```

**🔍 数据流向图（关键！）**：

```
用户输入: "苹果怎么吃？"
    |
    v
+------------------+
| RunnablePassthrough |  ← 原样通过，不做任何处理
|   (question)       |
+------------------+
    |
    v
+------------------+
|    retriever     |  ← 用 Embedding 把问题变成向量
|                  |  ← 去 ChromaDB 搜相似文档
+------------------+
    |
    v
+------------------+
|   format_docs    |  ← 把 List[Document] 拼成字符串
|   (context)      |
+------------------+
    |
    v
+------------------+
|  RAG_PROMPT      |  ← 把 {context} 和 {question} 填入模板
|                  |  ← 生成标准 messages 列表
+------------------+
    |
    v
+------------------+
|      llm         |  ← 调 DeepSeek API 生成回答
+------------------+
    |
    v
+------------------+
| StrOutputParser  |  ← 把 AIMessage 转成纯字符串
+------------------+
    |
    v
最终输出: "根据资料，苹果可以生吃、榨汁..."
```

---

## 四、三个容易懵的概念详解

### 1. RunnablePassthrough 是什么？

**🎯 一句话**：**透明玻璃管**——数据从左边进，原样从右边出，不做任何修改。

**📖 类比**：快递分拣线上的"直通道"。包裹到这里不用拆、不用改，直接滑到下一站。

**💻 为什么需要它**：
```python
{
    "context": retriever | format_docs,    # 这条路需要处理（检索+格式化）
    "question": RunnablePassthrough(),      # 这条路不需要处理（原样通过）
}
```
用户的问题 `"苹果怎么吃？"` 既要传给 `retriever` 去检索（变成 context），又要原样保留作为 `question`。

`RunnablePassthrough()` 就是告诉框架：**"这个问题本身，不要动，直接传给下一站的 {question} 占位符。"**

**⚠️ 常见错误**：
| 错误 | 原因 | 正确做法 |
|------|------|----------|
| 省略 RunnablePassthrough | 以为 question 会自动传 | 必须显式声明，框架才知道要把原始输入映射到哪个占位符 |
| 把 RunnablePassthrough 放在 context 位置 | 混淆了"原样通过"和"需要处理" | context 需要 `retriever \| format_docs` 处理，question 才需要原样通过 |

---

### 2. StrOutputParser 是什么？

**🎯 一句话**：**拆信封的人**——LLM 返回的是封装好的 AIMessage 对象，它帮你把里面的纯文本抽出来。

**📖 类比**：你收到一个精美礼盒（AIMessage），里面除了礼物（回答内容）还有贺卡、填充纸。StrOutputParser 就是帮你扔掉包装，只留礼物。

**💻 对比**：
```python
# 没有 StrOutputParser
result = (prompt | llm).invoke("你好")
print(result)
# 输出: AIMessage(content='你好！', additional_kwargs={}, ...)

# 有 StrOutputParser
result = (prompt | llm | StrOutputParser()).invoke("你好")
print(result)
# 输出: "你好！"
```

**什么时候可以省略**：如果你需要 LLM 返回的额外信息（比如 token 用量、推理过程），就不要加它。

---

### 3. ChatPromptTemplate 是什么？

**🎯 一句话**：**带空格的作文模板**——你预先写好格式，运行时把数据填进空格。

**📖 类比**：请假条模板。
```
尊敬的{老师}：
    我是{班级}的{姓名}，因{原因}请假{天数}天。
                                        申请人：{姓名}
```
运行时填入：`{老师: "王老师", 班级: "三年二班", 姓名: "小明", 原因: "生病", 天数: 2}`

**💻 代码**：
```python
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "你是助手，根据资料回答。资料：\n{context}"),
    ("human", "{question}"),
])

# 运行时自动填入
messages = RAG_PROMPT.format_messages(
    context="苹果可以生吃...",
    question="苹果怎么吃？"
)
# 生成:
# [SystemMessage(content="你是助手..."), HumanMessage(content="苹果怎么吃？")]
```

**和手搓版的对比**：
```python
# 手搓版：手动拼字符串，容易漏、容易错
messages = [
    {"role": "system", "content": f"根据资料回答：{context}"},
    {"role": "user", "content": query}
]

# LangChain 版：模板化管理，可复用、可维护
messages = RAG_PROMPT.format_messages(context=context, question=query)
```

---

## 五、流式输出：astream() vs invoke()

### 对比

| 方法 | 用途 | 返回值 | 适合场景 |
|------|------|--------|----------|
| `invoke()` | 一次性返回完整结果 | 字符串 | 简短回答、调试 |
| `astream()` | 流式返回，逐字推送 | 异步迭代器 | 长回答、实时展示 |

### 代码

```python
# 同步一次性调用
result = rag_chain.invoke("苹果怎么吃？")
print(result)  # 等全部生成完才打印

# 异步流式调用（咱们代码里用的）
async for chunk in rag_chain.astream("苹果怎么吃？"):
    print(chunk, end="")  # 生成一个字打印一个字
```

### 为什么需要包装成 SSE

LangChain 的 `astream()` 返回的是纯文本 chunk。但前端要的是 SSE 格式：
```python
# LangChain 输出: "苹" → "果" → "可" → "以" → ...

# SSE 格式: data: {"content": "苹"}\n\n
data: {"content": "果"}\n\n
```

所以咱们的代码里加了一层包装：
```python
async for chunk in rag_chain.astream(req.query):
    data = {"type": "content", "content": chunk}
    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
```

---

## 六、手搓版 vs LangChain 版：完整对照表

| 环节 | 手搓版 (`rag_router.py`) | LangChain 版 (`langchain_rag_router.py`) |
|------|--------------------------|------------------------------------------|
| **初始化 Embedding** | `client.embeddings.create(...)` | `OpenAIEmbeddings(...)` |
| **连接 Chroma** | `chroma_client.get_or_create_collection(...)` | `Chroma(client=..., collection_name=...)` |
| **检索资料** | `collection.query(...)` + 手动解析 | `retriever.invoke(...)` → List[Document] |
| **拼 Prompt** | f-string | `ChatPromptTemplate.from_messages([...])` |
| **调 LLM** | `client.chat.completions.create(...)` | `llm.invoke(...)` 或 `chain.astream(...)` |
| **解析输出** | `chunk.choices[0].delta.content` | `StrOutputParser()` |
| **流式封装** | 手动写 SSE 格式 | 手动写 SSE 格式（LangChain 不封装传输层） |
| **Token 管理** | 手动用 tiktoken 计算 | 部分自动化（Prompt 长度检查） |

**LangChain 没有替你做的事**：
- ❌ HTTP 传输层（SSE 格式还是要自己写）
- ❌ Token 硬截断（框架有辅助，但精细控制仍需手动）
- ❌ 业务逻辑（相似度阈值、权限校验等）

---

## 七、常见错误与避坑指南

| 错误 | 现象 | 原因 | 修复 |
|------|------|------|------|
| `ModuleNotFoundError: langchain_openai` | 导入报错 | 没安装包 | `pip install langchain-openai` |
| `Chroma` 导入 DeprecationWarning | 提示即将移除 | 用了旧路径 | `from langchain_chroma import Chroma` |
| 链返回空字符串 | LLM 没回答 | Prompt 模板占位符名和字典 key 不匹配 | 检查 `{context}` / `{question}` 是否一致 |
| 检索结果为空 | retriever 没搜到 | collection 里没有数据，或 embedding 模型不一致 | 确认手搓版已存入数据，且用的是同一模型 |
| `astream()` 不输出 | 流式卡住 | 没有用 `async for` | 确保是异步迭代：`async for chunk in chain.astream(...)` |
| LLM 回答幻觉 | 没有基于资料 | Prompt 模板里没有 `{context}` 占位符，或 context 为空 | 检查 Prompt 模板和 retriever 是否正常工作 |

---

## 八、速查表

### LCEL 常用组件

```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 透明通过
RunnablePassthrough()           # 原样输出
RunnablePassthrough.assign(...) # 原样通过，同时附加新字段

# 自定义函数包装
RunnableLambda(lambda x: x.upper())  # 把普通函数变成链的一环

# 输出解析
StrOutputParser()               # 转字符串
JsonOutputParser()              # 转 JSON（需配合 Prompt 要求输出 JSON）
```

### 链的调用方式

```python
# 同步
result = chain.invoke("输入")

# 异步
result = await chain.ainvoke("输入")

# 批量
results = chain.batch(["输入1", "输入2", "输入3"])

# 流式（同步）
for chunk in chain.stream("输入"):
    print(chunk)

# 流式（异步）
async for chunk in chain.astream("输入"):
    print(chunk)
```

### Prompt 模板定义方式

```python
# 方式 1：from_messages（推荐，对应 Chat 模型）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，擅长{skill}"),
    ("human", "{question}"),
])

# 方式 2：from_template（简单场景）
prompt = ChatPromptTemplate.from_template("请回答：{question}")
```

---

## 九、检查清单

- [ ] 能用自己的话说出 LangChain 解决了什么问题（框架 vs 手搓）
- [ ] 理解 `|` 管道符的作用（数据接力棒）
- [ ] 能说出 Document、Embedding、VectorStore、Retriever、LLM、Chain 六个概念的关系
- [ ] 理解 RunnablePassthrough 是"透明玻璃管"
- [ ] 理解 StrOutputParser 是"拆信封的人"
- [ ] 能看懂 LCEL 链的数据流向图
- [ ] 知道 `invoke()` 和 `astream()` 的区别
- [ ] 知道 LangChain **没有**替你做哪些事（SSE 封装、Token 硬截断、业务逻辑）

---

## 十、下一步预告

第二课：**对话记忆（Memory）**
- 解决"那香蕉呢？"的问题
- 给 LangChain 链加上多轮对话能力
- 对比 `ConversationBufferMemory` 和 `ConversationSummaryMemory`

第三课：**Agent（工具调用）**
- 让 AI 能查天气、算数学
- 理解 `Tool` → `Agent` → `AgentExecutor` 的架构
