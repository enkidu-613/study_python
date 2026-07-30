# 试卷：Multi-Agent 与复杂工作流

> 对应第 31 章。目标：确认你能把 Supervisor + Subagent、Router、单 Agent 状态驱动 Handoff 分开看，并能追踪一次 Agent 调用里 State、middleware 和 Tool 的流转。
>
> 本卷不要求你默写完整 import、模型初始化或生产级并发架构；代码题只看对象关系、数据流和调用顺序，不因标点、缩进或 IDE 能直接发现的拼写问题单独扣分。

---

## 答题说明

- 总分：100 分；90 分以上通过，70-89 分只补薄弱点，70 分以下回到关键关卡。
- 可以用自己的话回答，但要保留必要术语，例如 `Tool`、`State`、`middleware`、`thread_id`。
- 题目只覆盖第 31 章已经讲清的内容；不考多 Agent 子图 Handoff、生产级并发、跨 Agent 长期记忆。
- 请直接在每道题的“我的答案”后作答。答完后告诉我“答完了”。

---

## 第一轮：核心对象与模式（25 分）

每题 5 分。

### 1. `research_agent` 与 `ask_research_agent`

观察下面代码：

```python
research_agent = create_agent(
    model=llm,
    tools=[search_knowledge_base],
)


@tool
def ask_research_agent(question: str) -> str:
    result = research_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return result["messages"][-1].content
```

请分别说明：

1. `research_agent` 是什么对象？
2. `ask_research_agent` 是什么对象？
3. 谁会调用 `ask_research_agent`？
4. 谁会在它的函数体内部调用 `research_agent.invoke(...)`？

我的答案：

### 2. Supervisor + Subagent 的主流程

把下面步骤按真实发生的顺序排列，并说明最后是谁组织面向用户的答案：

```text
A. research_agent 调用 search_knowledge_base
B. supervisor 获得工具结果并继续请求模型
C. ask_research_agent 在 Python 函数内部调用 research_agent.invoke(...)
D. 用户问题进入 supervisor.invoke(...)
E. supervisor 的模型提出 ask_research_agent 的 tool call
```

我的答案：

### 3. 三种模式的边界

为每个场景选择最合适的模式，并说明理由：

1. 只按用户问题是否包含“知识库”决定走检索分支还是普通回答分支。
2. 主 Agent 需要内部调用一个只做资料检索、不会直接对用户说话的专业助手。
3. 同一个对话助手需要根据当前处理角色改变 Prompt 和可用 Tools，且角色状态要保存在共享 State 中。

可选模式：`Router`、`Subagent`、`Handoff`。

我的答案：

### 4. 什么时候不该拆 Multi-Agent？

下面需求是“为项目知识库回答问题”。只有一个领域，只有两个工具，没有独立权限和上下文要求。

你会拆成“检索 Agent + 总结 Agent + 回答 Agent”吗？请说明理由，并给出此时更合适的做法。

我的答案：

### 5. “support_agent” 到底是不是 Agent？

在本章单 Agent + middleware 的 Handoff 例子中：

```python
active_agent = "support_agent"
```

这行代码是否自动创建、发现或跳转到了一个 Python 变量名为 `support_agent` 的 Agent？请解释它实际改变了什么，以及真正的多 Agent 子图还需要哪些东西。

我的答案：

---

## 第二轮：State、工具结果与 Handoff（30 分）

每题 6 分。

### 6. 普通工具返回值与 `Command(update=...)`

请比较下面两种工具返回方式：

```python
return "已查到退款规则。"
```

```python
return Command(
    update={
        "messages": [ToolMessage(content="已转交支持角色。", tool_call_id=...)],
        "active_agent": "support_agent",
    }
)
```

分别回答：

1. 普通字符串会怎样进入模型下一次可见的消息历史？
2. 第二段额外能修改什么？
3. 为什么第二段仍要提供匹配当前工具调用的 `ToolMessage`？

我的答案：

### 7. `tool_call_id` 的来源和用途

`transfer_to_support` 接收：

```python
runtime: ToolRuntime[None, HandoffState]
```

请说明：

1. `ToolRuntime` 是谁传进工具函数的？
2. `runtime.tool_call_id` 是从哪里来的？
3. 它在 `ToolMessage(..., tool_call_id=runtime.tool_call_id)` 中负责把哪两件事关联起来？
4. 它是不是 `runtime.state` 里的业务字段？

我的答案：

### 8. `thread_id`、State 与 Checkpointer

解释以下三个东西的分工，且说明它们谁不能由 `Command(update=...)` 直接修改：

```text
State
thread_id
InMemorySaver checkpointer
```

再回答：为什么没有 checkpointer 时，连续两次独立 `supervisor.invoke(...)` 不会天然记住上一轮？

我的答案：

### 9. Router 与 Handoff 实际改变的东西

下面两个片段分别改变了什么？

```python
def route_question(state: dict) -> str:
    return "research" if "知识库" in state["question"] else "answer"
```

```python
return Command(update={"active_agent": "support_agent"})
```

请从“下一步执行路径”和“共享 State / 角色配置”两个角度解释差别。

我的答案：

### 10. `Command(update=...)` 的边界

现有状态结构为：

```python
class HandoffState(AgentState):
    active_agent: NotRequired[str]
    retry_count: NotRequired[int]
```

下面四项中，哪些适合由 `Command(update=...)` 更新？哪些不适合？说明原因。

```text
A. active_agent
B. retry_count
C. thread_id
D. 当前模型的 temperature
```

我的答案：

---

## 第三轮：middleware 调用链（25 分）

每题 5 分。

### 11. 谁调用了 `select_prompt`？

本章有如下关系：

```python
@wrap_model_call
def apply_role_config(request, handler):
    state = cast(HandoffState, request.state)
    prompt = select_prompt(state)
    updated_request = request.override(
        system_message=SystemMessage(content=prompt),
        tools=available_tools,
    )
    return handler(updated_request)


handoff_agent = create_agent(
    ...,
    middleware=[apply_role_config],
)
```

请按顺序解释：

1. `apply_role_config` 怎样被 Agent 使用？
2. `select_prompt(state)` 是谁调用的？
3. `request.override(...)` 返回的是什么概念上的对象？
4. `handler(updated_request)` 不调用会怎样？

我的答案：

### 12. middleware 是否“继承记忆”？

有人说：“middleware 每次都执行，所以它自己继承了记忆和 `active_agent`。”

这句话哪里对，哪里不准确？请分别说明：

```text
middleware
State
checkpointer + 相同 thread_id
```

在这件事上各自负责什么。

我的答案：

### 13. 追踪一轮 Handoff

初始 State 没有 `active_agent`。用户提问后，模型调用 `transfer_to_support`；该工具返回含 `active_agent="support_agent"` 的 `Command(update=...)`。

请写出从“模型提出 tool call”开始，到下一次模型调用拿到支持角色 Prompt 为止的最短调用链。要求至少包含：

```text
ToolRuntime
Command(update)
State
middleware
select_prompt
request.override
handler
```

我的答案：

### 14. `handler` 的本质

`handler: Callable[[ModelRequest], ModelResponse]` 中的 `handler` 是什么？

请用自己的话解释：它像 Express 的 `next` 的哪一部分，又与 Express 的 `next` 有什么不能直接画等号的地方？重点说明它接收什么、返回什么、在本例中为什么能让“改后的 Prompt 和 Tools”生效。

我的答案：

### 15. 一个状态驱动 Handoff 的排错题

工具已经成功更新：

```python
{"active_agent": "support_agent"}
```

但下一次模型调用仍使用旧 Prompt 和旧 Tools。

请给出最可能的两个原因，并分别写出修复方向。

我的答案：

---

## 第四轮：综合设计与代码阅读（20 分）

### 16. 课程助手 + 复习助手（10 分）

设计一个 Supervisor + Subagent 方案，不需要写完整代码。请写清：

1. 谁是 Supervisor，谁是 Subagent？
2. Subagent 会被包装成什么 Tool？
3. Tool 的输入和返回值分别是什么？
4. 用户上下文由谁保留？
5. 最终答案由谁组织？
6. 这个场景为什么适合 Subagent，而不是 Handoff？

我的答案：

### 17. 阅读代码并判断边界（10 分）

```python
agent = create_agent(
    model=llm,
    tools=[ask_research_agent],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "项目中如何初始化向量存储？"}]}
)
```

请回答：

1. 这次 `invoke` 中，模型能不能保证一定调用 `ask_research_agent`？为什么？
2. 若模型没有调用 Tool，优先检查哪两个层面？
3. 这段代码本身是否提供跨第二次独立 `invoke` 的记忆？为什么？
4. 如果要跨轮记忆，至少要增加哪两类配置？

我的答案：

---

## 交卷格式

答完后直接告诉我“答完了”。我会按 [第 31 章 Multi-Agent 与复杂工作流](</Users/enkidu/PyCharmMiscProject/md/31_Multi-Agent与复杂工作流.md>) 批改：先给总分与通过结论，再逐题解释真正需要补的知识点；不会因 Python 标点细节重复扣分。
