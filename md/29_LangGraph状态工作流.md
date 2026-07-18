# 29. LangGraph 状态工作流：把 Agent 的执行过程显式画出来

> 本章目标：你能把一个简单流程写成 `State -> Node -> Edge -> compile -> invoke`，并说清它和上一章 `create_agent(...)` 的关系。
>
> 本章不做生产级多智能体、复杂并行图、人工审批、数据库持久化或 LangSmith。先把最小状态图跑通。

---

## 权威来源速记

本章以 LangGraph 官方文档为准，并按当前项目的学习顺序改写：

| 来源 | 本章采用的结论 |
| --- | --- |
| [LangGraph Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) | 图由 State、Node、Edge 组成；先定义图，再 `compile()`，最后 `invoke()`。 |
| [Use the graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api) | State 可以用 `TypedDict`、Pydantic 或 dataclass 描述；入门阶段 `TypedDict` 最直观。 |
| [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | 配置 checkpointer 后，图会按线程保存执行过程中的 state 快照。 |

---

## 本章学到哪里，不学到哪里

本章学：

```text
StateGraph
State
Node
Edge
START / END
compile()
invoke()
checkpointer 与 thread_id 的连接点
```

本章暂不学：

```text
条件边的完整写法
复杂循环与并行图
Command / Send / reducer
人工介入审批
数据库 checkpointer
多 Agent Supervisor
```

这些不是不重要，而是先把“状态如何流过固定步骤”看清。下一阶段再让边根据 state 做选择。

---

## ADHD 四条铁律

| # | 本章规则 | 做法 |
| --- | --- | --- |
| 1 | 先看数据怎么流 | 先运行没有真实 LLM 的最小图。 |
| 2 | 一个新概念一次只做一件事 | State、Node、Edge 分开解释。 |
| 3 | 不把上一章推倒重来 | 复用 `state`、`checkpointer`、`thread_id` 的已有理解。 |
| 4 | 每一关都有可验证结果 | 运行最小代码，检查最终 state。 |

---

## 一句话理解

**LangGraph 是一个状态工作流框架：你自己声明状态长什么样、每一步做什么、下一步去哪里。**

上一章的 `create_agent(...)` 把很多流程藏在框架里：

```text
用户消息
-> 模型
-> 可能调用工具
-> 工具结果
-> 模型最终回答
```

LangGraph 让你显式写出这条流程：

```text
START
-> node A
-> node B
-> END
```

它不是另一种模型，也不是替模型调用工具。它负责的是：**编排哪些 Python 步骤按什么顺序运行，以及它们共用什么 state。**

---

## 准确术语

| 名称           | 准确含义                   | 在本章里的职责                  |
| ------------ | ---------------------- | ------------------------ |
| `State`      | 工作流当前共享数据的 schema      | 规定节点可以读写哪些字段。            |
| `StateGraph` | 构建状态图的 builder         | 注册节点和边。                  |
| Node         | 普通 Python 函数           | 读取当前 state，返回本节点要更新的字段。  |
| Edge         | 节点之间的连接规则              | 决定固定的下一步。                |
| `START`      | 框架提供的起点标记              | 指向第一个 node。              |
| `END`        | 框架提供的结束标记              | 表示流程完成。                  |
| `compile()`  | 把 builder 编译成可运行 graph | 检查基本图结构，并可接收 runtime 配置。 |
| `invoke()`   | 执行编译后的 graph           | 传入初始 state，返回最终 state。   |

### 先分清三个容易混的词

```text
state       = 当前整份工作数据
messages    = state 里可能存在的一个字段
checkpointer = 保存/恢复 state 快照的组件
```

例如后续聊天 Agent 的 state 可能是：

```python
{
    "messages": [...],
    "retrieved_docs": [...],
    "risk_level": "low",
}
```

`messages` 不是整个 state；它只是其中一部分。

---

## 第一关：最小状态图先跑起来

先不用真实 LLM。原因很简单：你现在要看的是图的执行顺序，不是 API、Prompt 或模型回答质量。

先在项目根目录安装并由 Poetry 记录依赖。这个命令只需要执行一次：

```bash
poetry add langgraph
```

马上验证当前 Poetry 环境能导入它：

```bashr
poetry run python -c "from langgraph.graph import StateGraph; print('LangGraph import ok')"
```

然后新建一个临时 Python 文件，或直接在项目根目录执行这段：

```python
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class LearningState(TypedDict):
    question: str
    normalized_question: str
    answer: str


def normalize_question(state: LearningState) -> dict[str, str]:
    return {"normalized_question": state["question"].strip().lower()}


def create_answer(state: LearningState) -> dict[str, str]:
    return {"answer": f"准备回答：{state['normalized_question']}"}


builder = StateGraph(LearningState)
builder.add_node("normalize_question", normalize_question)
builder.add_node("create_answer", create_answer)
builder.add_edge(START, "normalize_question")
builder.add_edge("normalize_question", "create_answer")
builder.add_edge("create_answer", END)

graph = builder.compile()

result = graph.invoke({"question": " Checkpointer 是什么？ "})
print(result)
```

预期核心结果：

```python
{
    "question": " Checkpointer 是什么？ ",
    "normalized_question": "checkpointer 是什么？",
    "answer": "准备回答：checkpointer 是什么？",
}
```

### 这段代码的执行顺序

```text
初始 state
{"question": " Checkpointer 是什么？ "}

START
  -> normalize_question
     返回 {"normalized_question": "checkpointer 是什么？"}
  -> create_answer
     返回 {"answer": "准备回答：checkpointer 是什么？"}
  -> END

最终 state
{
  "question": " Checkpointer 是什么？ ",
  "normalized_question": "checkpointer 是什么？",
  "answer": "准备回答：checkpointer 是什么？"
}
```

---

## 第二关：State 到底是什么

```python
class LearningState(TypedDict):
    question: str
    normalized_question: str
    answer: str
```

`TypedDict` 的作用是描述一个 dict 应该有哪些 key、每个 key 的值是什么类型。

它不是实例化一个复杂对象；运行时传进图的 state 仍然像普通 dict：

```python
{
    "question": "...",
    "normalized_question": "...",
    "answer": "...",
}
```

为什么不直接在函数里随便传变量？因为多个 node 需要共享同一份工作数据。State 就像它们共同遵守的数据合同。

### Node 不需要返回完整 state

看这个 node：

```python
def normalize_question(state: LearningState) -> dict[str, str]:
    return {"normalized_question": state["question"].strip().lower()}
```

它读取 `state["question"]`，但只返回自己更新的字段：

```python
{"normalized_question": "checkpointer 是什么？"}
```

LangGraph 会把这份更新合并回工作流 state。入门阶段先记住默认直觉：**同名字段的新值会覆盖旧值。**

以后你会学 reducer，才处理“列表要追加，不是覆盖”这类规则；本章先不展开。

---

## 第三关：Node 和 Edge 分工

### Node：做事

```python
builder.add_node("normalize_question", normalize_question)
```

左边字符串是 node 名称，右边是实际执行的 Python 函数。

Node 的职责是：

```text
读 state
-> 做一次工作
-> 返回 state 更新
```

它不会天然决定下一步去哪里。

### Edge：决定固定顺序

```python
builder.add_edge(START, "normalize_question")
builder.add_edge("normalize_question", "create_answer")
builder.add_edge("create_answer", END)
```

边把执行顺序写出来：

```text
START -> normalize_question -> create_answer -> END
```

这就是为什么说：

```text
node 负责做事
edge 负责安排下一步
state 负责传递工作数据
```

别把它理解成 node 返回下一个 node 名。这个例子的固定流向由 edge 定义；“根据 state 选不同边”是条件边，后面再学。

---

## 第四关：`compile()` 和 `invoke()` 为什么分开

```python
graph = builder.compile()
```

`builder` 只是你正在搭建的图纸。`compile()` 把图纸变成可运行的 graph(图表)，并做基本结构检查，例如节点有没有正确接入图。

```python
result = graph.invoke({"question": " Checkpointer 是什么？ "})
```

`invoke()` 才是真正执行：

```text
输入初始 state
-> 按 edge 运行 node
-> 合并每个 node 返回的更新
-> 返回最终 state
```

和上一章对照：

| 上一章 | 本章 |
| --- | --- |
| `agent = create_agent(...)` | `graph = builder.compile()` |
| `agent.invoke(...)` | `graph.invoke(...)` |
| 框架内置 Agent loop | 你显式声明 nodes 与 edges |

注意：两者都不是“创建时就请求模型”。真正执行仍发生在 `invoke()`。

---

## 第五关：把上一章的 checkpointer 接进来

上一章你已经学过：

```text
thread_id 决定恢复哪条线程
	checkpointer 负责保存和恢复 Agent state 快照
```

LangGraph 里这个组件放在 `compile()`：

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())

config = {
    "configurable": {
        "thread_id": "user-1-thread-1",
    }
}

result = graph.invoke(
    {"question": "Checkpointer 是什么？"},
    config=config,
)
```

边界要非常准确：

```text
没有 checkpointer：图照样能运行，但跨 invoke 不恢复旧 state。
有 checkpointer + 相同 thread_id：可以恢复同一条 state 快照链。
只有 thread_id：没有组件负责保存，不能产生记忆。
InMemorySaver：只在当前 Python 进程内；重启服务就会丢失。
```

本章只连接概念。下一章再决定什么状态该长期保存、什么状态只能临时保存。

---

## 第六关：先看你的 RAG Agent 里的对象长什么样

上一章的 `create_agent(...)` 已经能工作，但它把模型、工具和循环藏在框架内部。本节先不要求你手写完整 Agent；先认清真实代码形态：每个名字到底是函数、类还是对象。

### 先认四个已有或即将出现的对象

```python
from app.tools.knowledge_base import search_knowledge_base
from langgraph.prebuilt import ToolNode, tools_condition

tools = [search_knowledge_base]
model_with_tools = llm.bind_tools(tools)
```

| 代码 | 它是什么 | 谁创建它 | 用途 |
| --- | --- | --- | --- |
| `search_knowledge_base` | `@tool` 装饰后的 Tool 对象 | 你在 `knowledge_base.py` 里定义函数，再由 `@tool` 包装 | 描述工具名称、参数和说明，并能真正搜索知识库。 |
| `tools` | Tool 对象列表 | 你自己创建的 list | 告诉模型和工具节点：当前允许使用哪些工具。 |
| `llm` | `ChatDeepSeek(...)` 创建的模型对象 | 你在路由中创建 | 能调用大模型，但还不知道有哪些工具可用。 |
| `model_with_tools` | 绑定了工具说明的模型对象 | `llm.bind_tools(tools)` 返回 | 模型现在可以在回答中提出 `tool_call`。 |

`bind_tools(...)` 不是执行工具。它只是把工具的 schema 交给模型，作用和你第 26 章手写 Function Calling 时“把 tools 发给模型”相同。

### Model Node 是你写的普通 Python 函数

```python
from langgraph.graph import MessagesState


def call_model(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

`call_model` 不是 LangGraph 内置类。它就是一个普通 Python 函数，注册到图以后才成为一个 model node：

```python
builder.add_node("model", call_model)
```

它读取 `state["messages"]`，调用模型，然后把模型的新消息写回 State。模型的新消息可能是普通回答，也可能携带 `tool_call`。

### Tool Node 是 LangGraph 提供的预制对象

```python
tool_node = ToolNode(tools)

builder.add_node("tools", tool_node)
```

`ToolNode` 是一个类；`ToolNode(tools)` 创建的是能执行工具的对象。它读取模型消息里的 `tool_call`，找到对应的 `search_knowledge_base`，调用它，并把工具结果作为消息写回 State。

你当然也可以自己写一个普通函数来执行工具，但 `ToolNode` 已经处理了常见的工具调用、结果回写和错误处理。入门阶段先使用它，后面再拆开手写。

### 再把对象连成一张图

```python
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")

graph = builder.compile()
```

注意：`builder.add_edge("tools", "model")` 不是流程终止，而是把工具结果送回模型继续处理。这里先结束的是“图的节点和边定义”，下一步本来应当是 `compile()`，再下一步才是 `graph.invoke(...)`。本节为了先看懂对象形状，暂不要求你继续完成真实 Agent 的调用。

### `tools_condition`：决定模型下一步去哪

`tools_condition` 是 LangGraph 提供的路由函数。它只检查一件事：模型刚才的消息里有没有 `tool_call`。

```text
有 tool_call  -> 去 "tools"
没有 tool_call -> 去 END
```

因此本例不需要手写 `builder.add_edge("model", END)`：`tools_condition` 已经负责在“没有新工具调用”时结束流程。`END` 不是普通业务函数，而是 LangGraph 提供的结束标记。

这里的“没有 tool_call”不是说模型没有输出内容。模型可能已经生成了完整的普通回答：

```text
model 节点等待模型完成本次响应
  -> 得到 AIMessage(content="最终回答", tool_calls=[])
  -> tools_condition 发现没有 tool_call
  -> 走 END，但 AIMessage 的回答已经保留在 State/messages 中
```

`tools_condition` 只会在 `model` 节点完成一次响应后运行，不会在模型生成过程中打断模型。普通回答已经写入 `messages`，再走 `END`；`END` 只结束后续节点，不会删除回答。

因此真实执行路径是：

```text
用户消息
  -> call_model（普通函数，调用绑定工具后的模型）
  -> tools_condition（查看模型是否提出 tool_call）
     -> 有：ToolNode(tools) 执行 search_knowledge_base
           -> 工具结果写回 messages
           -> call_model 再次调用模型，生成最终回答
     -> 无：END
```

这正是你已学过的 Function Calling loop。区别只是：第 26 章你手写“判断、找函数、执行、回传”；这里 LangGraph 用 Node 和 Edge 把同一流程显式画出来。

### 多次调用工具时如何循环

一次工具调用不是整个流程的终点。模型拿到工具结果后，可能继续提出另一个 `tool_call`；只要还有 `tool_call`，就会再次经过 `tools` 节点，再回到 `model`：

```text
model：调用 search_weather
  -> tools：执行并返回天气
  -> model：根据天气，继续调用 search_calendar
  -> tools：执行并返回日历
  -> model：根据两个结果生成普通回答
  -> tools_condition：发现没有 tool_call
  -> END
```

所以 `builder.add_edge("tools", "model")` 形成的是循环回边，不是“工具只执行一次”。真正结束的条件是：某次 `model` 响应中没有新的 `tool_call`。如果图一直产生工具调用而始终不结束，LangGraph 会在达到递归限制后报错；生产代码还应限制工具次数、校验参数并处理异常。

### 和你当前 `create_agent(...)` 的关系

| 你当前代码 | 显式 LangGraph 图里的对应部分 |
| --- | --- |
| `ChatDeepSeek(...)` | `llm` |
| `tools=[search_knowledge_base]` | `tools`，再通过 `llm.bind_tools(tools)` 交给模型 |
| `create_agent(...)` | 替你封装 `call_model`、`ToolNode`、条件边和循环 |
| `checkpointer=InMemorySaver()` | 编译图时传给 `graph.compile(checkpointer=...)` |

### 本节边界

这节的目标是认得真实代码形态和调用链，不要求你现在复制运行完整图。`MessagesState`、`tools_condition` 和完整 Agent 实战会在下一章逐个写出来；现在只需能指出：哪个是普通函数、哪个是框架类、哪个对象真正执行工具。

安全边界没有变：模型 node 只能提出 `tool_call`；`ToolNode` 才执行 Python 工具。LangGraph 不能替你跳过参数校验、权限校验或高风险确认。

---

## 三遍主动练习

### 1. 读懂

不看代码，先口头说出：

```text
初始 state 里有什么？
第一个 node 新增或更新了什么？
第二个 node 读取了什么、又更新了什么？
最终 result 是什么？
```

### 2. 跟写

先确认下面三条 edge 组成的是一条直线：

```python
builder.add_edge(START, "normalize_question")
builder.add_edge("normalize_question", "create_answer")
builder.add_edge("create_answer", END)
```

然后只做一个“读图实验”：删除这条结束边：

```python
builder.add_edge("create_answer", END)
```

再改为：

```python
builder.add_edge("create_answer", "normalize_question")
```

这时图才会变成：

```text
normalize_question -> create_answer -> normalize_question
```

先不要运行它。没有结束边的循环图会在达到框架的递归限制后报 `GraphRecursionError`；这个练习只用于确认：**改 edge 改的是流程，不是 node 内的业务逻辑。**

### 3. 独立重写

把最小图换成“学习计划”版本：

```text
输入 topic
-> make_outline node 生成提纲
-> write_preview node 生成一段预览
-> END
```

要求：

1. State 至少有 `topic`、`outline`、`preview`。
2. 两个 node 都只返回自己更新的字段。
3. 运行后 `result["preview"]` 能读到 `result["outline"]` 的内容。

---

## 常见坑

### 坑 1：以为 `compile()` 会执行图

```python
graph = builder.compile()
```

这一步只是得到可运行对象。只有 `graph.invoke(...)` 才会执行 node。

### 坑 2：以为 node 要返回整个 state

```python
# 不必重复返回所有字段
return {"answer": "..."}
```

Node 返回它负责更新的字段即可。

### 坑 3：把 `state` 当成 `messages`

聊天工作流里 `messages` 很常见，但它只是一个字段。普通工作流可以完全没有 messages，例如本章的 `question`、`normalized_question`、`answer`。

### 坑 4：没有 checkpointer 就以为图不能运行

最小图不需要 checkpointer。它负责跨步骤/跨调用保存恢复 state，不负责让 node 本身“能运行”。

### 坑 5：以为 LangGraph 自动保证安全

图能规定流程，不能自动判断你是否该执行删除、付款、发送邮件等动作。工具参数、权限和人工确认仍由你的业务代码负责。

---

## 本章和后续章节的关系

```text
第 26 章：手写 Function Calling loop，理解工具调用实际如何执行
第 27 章：消息历史怎样保存和注入
第 28 章：create_agent 把常见 Agent loop 封装起来
第 29 章：LangGraph 把 state、node、edge 显式写成工作流
后续：条件边、工具循环、人工介入、可恢复工作流、多 Agent
```

---

## 四条理解标准检查点

### 1. 核心思想是什么？

LangGraph 用共享 state、执行 node、连接 edge 来显式定义工作流，而不是把执行顺序藏在框架内部。

### 2. 它解决什么问题？

当 Agent 不再是一条固定直线，而需要明确分支、循环、状态恢复或人工介入时，你可以看见并控制每一步。

### 3. 为什么不一直用 `create_agent` 或手写 loop？

简单标准 Agent 用 `create_agent` 更省事；为了学习底层或完全自定义，用手写 loop 最直观；当流程变成多个明确步骤和状态转移时，LangGraph 更容易组织、观察和扩展。

### 4. 在本项目里怎么识别？

看到 `StateGraph(...)`、`add_node(...)`、`add_edge(...)`、`compile()`、`invoke(...)` 时，就知道它在显式构建状态工作流；看到 `InMemorySaver()` 和 `thread_id` 时，就知道它在给 state 增加保存和恢复能力。

---

## 本章最小通关标准

你能做到下面四条，就可以进入跟写：

1. 说出 State、Node、Edge 各自负责什么。
2. 写出 `START -> node A -> node B -> END` 的最小图。
3. 说出 `compile()` 和 `invoke()` 的区别。
4. 说出为什么 `messages` 只是 state 的一个字段，以及为什么 checkpointer 不是运行图的必需品。
