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

1. 是子agent对象，如果只是问对象的话那就是已编译的agent图
2. tool注解的langchain tool 对象，可以被主agent调用
3. 主agent
4. ask_research_agent
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
d,e,c,a,b
### 3. 三种模式的边界

为每个场景选择最合适的模式，并说明理由：

1. 只按用户问题是否包含“知识库”决定走检索分支还是普通回答分支。
2. 主 Agent 需要内部调用一个只做资料检索、不会直接对用户说话的专业助手。
3. 同一个对话助手需要根据当前处理角色改变 Prompt 和可用 Tools，且角色状态要保存在共享 State 中。

可选模式：`Router`、`Subagent`、`Handoff`。

我的答案：
1. Router
2. sub agent
3. handoff
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

不是，本质上是将当前agent切换了不同的prompt和tools子集，只是切换了当前agent的角色，需要langgraph的节点和边和多个create agent和不同的prompt和tools工具子集

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
1. command交给框架之后框架根据内容更新到State
2. 第二段可以修改State已经定义的active_agent
3. 第二段不是继承AgentState的HandoffState定义的么

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
1. 框架通过tool注解传递的
2. llm发起调用的时候生成，框架附上的
3. 他负责和带有tool call的AIMessage对应起来
4. 不是，因为业务字段是程序员自己定义，有业务逻辑使用的字段，这个是框架自带数据

### 8. `thread_id`、State 与 Checkpointer

解释以下三个东西的分工，且说明它们谁不能由 `Command(update=...)` 直接修改：

```text
State
thread_id
InMemorySaver checkpointer
```

再回答：为什么没有 checkpointer 时，连续两次独立 `supervisor.invoke(...)` 不会天然记住上一轮？

我的答案：

State：会话的状态快照
thread_id：绑定一个会话，当相同的id的会话请求来的时候，恢复绑定这个会话id的State快照
InMemorySaver：是状态检查点，当当前会话结束之后保存最终State到绑定id的会话

---
不会，因为模型没有记忆，需要State保存上下文对话

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
第一个是根据用户的对话中是否有知识库决定了是回答还是继续resarch的agent执行路径
第二个是根据用户回答分配用户应该使用哪一个角色配置prompt和tools，临时修改了State

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
a 和 b 因为command只是和修改State定义的框架自带属性和继承框架State类后自定义的属性

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
1. wrap_model_call把函数变为模型调用前的拦截器，再在模型创建时注册成为agent的中间件，当模型调用之前会首先触发改函数
2. 是apply_role_config拦截器函数调用的
3. 返回的是一个被修改的ModelResponse对象
4. 不调用就会卡住，永远请求不了模型
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
不对，继承记忆因为是每次在相同thread id 的会话使用的同一个State快照，在请求模型时框架注入进了runtime.state，state内有框架上次存到快照里的参数

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
middleware->select_prompt->request.override->handler->ToolRuntime->Command->State

### 14. `handler` 的本质

`handler: Callable[[ModelRequest], ModelResponse]` 中的 `handler` 是什么？

请用自己的话解释：它像 Express 的 `next` 的哪一部分，又与 Express 的 `next` 有什么不能直接画等号的地方？重点说明它接收什么、返回什么、在本例中为什么能让“改后的 Prompt 和 Tools”生效。

我的答案：
handler将修改好后的ModelRequest交给llm，至于next，我没有深入学习Express，这个我不想回答，他是一个可调用对象，接收一个ModelRequest参数，返回一个ModelResponse参数，因为request.override修改了给llm的State，handler接收update的时候收到的是修改过后的ModelResponse

### 15. 一个状态驱动 Handoff 的排错题

工具已经成功更新：

```python
{"active_agent": "support_agent"}
```

但下一次模型调用仍使用旧 Prompt 和旧 Tools。

请给出最可能的两个原因，并分别写出修复方向。

我的答案：
没有使用checkpoint，第二没有使用thread id绑定到会话中

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
1. supervisor只对用户负责，指挥subagent干活，subagent只对spuervisor负责，不直接对用户负责
2. 因为 supervisor 不能直接调用subagent，需要一个工具来进行
3. 输入一个str，返回一个str，经过tool message包装
4. 由checkpoint InMemorySaver 存储最后的快照State保留
5. 最终答案由主supervisor接收subagent的返回信息交给llm做最后输出
6. 当一个agent想要其subagent做不同的事情，有明确分工而且不需要直接与用户对话的时候
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
1. 不能，因为用户没有明确要求检索知识库
2. 首先这个模型没有提示词，第二检查tool注解函数的第一行注释
3. 不能，因为invoke没有设置config，agent也没有注册checkpoint
4. 注册checkpoint InMemorySaver 定义 config

---

## 交卷格式

答完后直接告诉我“答完了”。我会按 [第 31 章 Multi-Agent 与复杂工作流](</Users/enkidu/PyCharmMiscProject/md/31_Multi-Agent与复杂工作流.md>) 批改：先给总分与通过结论，再逐题解释真正需要补的知识点；不会因 Python 标点细节重复扣分。

---

## 批改结果（2026-07-31）

| 题号 | 得分 | 结论 |
| --- | ---: | --- |
| 1 | 5 / 5 | 对象关系准确。 |
| 2 | 4 / 5 | 顺序正确；漏写“supervisor 组织最终答复”。 |
| 3 | 4 / 5 | 三种模式选对；理由没有展开。 |
| 4 | 0 / 5 | 未作答。 |
| 5 | 5 / 5 | 清楚区分了角色状态值和真实 Agent 子图。 |
| 6 | 2 / 6 | 混淆普通字符串返回和 `Command(update=...)`；`ToolMessage` 的关联作用没有答到。 |
| 7 | 6 / 6 | `ToolRuntime`、`tool_call_id` 和 `AIMessage` 的关联答得准确。 |
| 8 | 5 / 6 | 基本正确；还应明确 `thread_id` 和 checkpointer 都不是 `Command(update=...)` 可直接修改的 State 字段。 |
| 9 | 5 / 6 | Handoff 部分正确；Router 更准确地说是选图中的后续路径，而不是直接选择另一个 Agent。 |
| 10 | 4 / 6 | 正确选出 A、B；漏写 C、D 不适合的原因。 |
| 11 | 4 / 5 | 调用关系正确；`override()` 返回的是修改后的 `ModelRequest`，不是 `ModelResponse`。 |
| 12 | 4 / 5 | 已知道记忆来自 State 快照；还需分清 middleware 只读取/改写本次请求，不保存记忆。 |
| 13 | 1 / 5 | 术语都出现了，但顺序倒置；这是本章当前最需要补的链路。 |
| 14 | 3 / 5 | 知道 handler 是可调用对象并会继续模型调用；仍混淆了 `ModelRequest` 与 `ModelResponse`。 |
| 15 | 0 / 5 | checkpointer/thread_id 影响跨轮恢复，不是同一次 Agent loop 内 Prompt/Tools 没切换的直接原因。 |
| 16 | 7 / 10 | Supervisor、最终答复和适用边界正确；用户上下文在本次调用内由 supervisor 的 State 保留，不必一定依赖 checkpointer。 |
| 17 | 9 / 10 | 已正确识别模型不保证调用 Tool、Prompt/Tool 描述的排查层面，以及跨轮记忆所需配置。 |

**总分：68 / 100**

**评定：需要重学关键关卡，但不需要重学整章。**

你已经掌握 Supervisor + Subagent、三种模式边界、`tool_call_id`、跨轮记忆的基本边界。当前卡点集中在“状态驱动 Handoff 的一次完整循环”，不是 Multi-Agent 概念整体没懂。

### 必补的三件事

1. **普通字符串与 `Command` 的差别**：普通字符串由 Agent / ToolNode 自动包装成 `ToolMessage` 并追加到 `messages`；`Command(update=...)` 除了写入消息，还能修改 `active_agent` 等 State 字段。
2. **Handoff 的正确时序**：模型先提出 tool call，框架再注入 `ToolRuntime` 执行工具，工具返回 `Command` 更新 State；之后 Agent loop 再次进入 middleware，`select_prompt` 才会读到新的 `active_agent`，`request.override(...)` 生成新的 `ModelRequest`，`handler(...)` 用它继续真实模型调用。
3. **本次切换与跨轮记忆分层**：同一次 `invoke()` 中切换 Prompt/Tools 靠 `Command -> State -> middleware -> override -> handler`；跨第二次 `invoke()` 恢复旧 State 才需要 `checkpointer + 相同 thread_id`。

### 最小补写检查

不用重答整卷。下次只需用自己的话写清下面两条：

1. 当 `transfer_to_support` 返回 `Command(update={"active_agent": "support_agent", ...})` 后，下一次模型调用前依次发生什么？
2. “State 已经变成 support_agent，但 Prompt 仍没变”时，优先检查哪两个地方？

这两条答清楚后，再做一份 20 分以内的补考。
