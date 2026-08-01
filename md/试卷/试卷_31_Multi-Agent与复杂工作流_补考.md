# 补考试卷：第 31 章 Multi-Agent 与复杂工作流

> 本卷只补第一次考试暴露出的关键链路，不重考 Supervisor、Subagent 和三种模式的全部内容。
>
> 总分：20 分。答题只看 State、工具执行、middleware 和模型请求之间的关系，不因标点、缩进或没有写完整 import 扣分。

---

## 1. Handoff 完整时序（8 分）

已知：第一次模型调用时，模型提出了 `transfer_to_support` 的 tool call；工具返回：

```python
Command(
    update={
        "messages": [ToolMessage(...)],
        "active_agent": "support_agent",
    }
)
```

请从工具返回 `Command` 开始，写出下一次模型调用拿到支持角色 Prompt 和 tools 之前的完整顺序。

必须解释这些对象各自做了什么：

```text
Command(update)
State
Agent loop
middleware
select_prompt
request.override
handler
ModelRequest
```

我的答案：

框架接收到command，根据内容更新messages和active agent参数到Sate，agent loop 发现工具调用完成但是还没最终回答，于是再次进入模型调用阶段，调用前执行middleware，执行中select propmt发现active agent 参数更改，返回适合的提示词，然后条件分支语句选择好适合agent角色的子集然后prompt和工具子集交给override处理，处理后的ModelRequest交给handler将修改后的request交给模型，模型调用合适的工具后输出最终回答
---

## 2. 普通字符串和 `Command`（4 分）

比较下面两种工具返回值：

```python
return "查询结果"
```

```python
return Command(
    update={
        "messages": [ToolMessage(...)],
        "active_agent": "support_agent",
    }
)
```

请回答：

1. 普通字符串最终怎样进入 `messages`？
2. `Command(update=...)` 比普通字符串多做了什么？
3. `ToolMessage.tool_call_id` 为什么要和模型的 tool call 对应？

我的答案：
1. 普通字符串最终经过框架包装为tool message后进入messages
2. command可以更新多个State定义的字段，也可以控制路由跳转
3. 因为模型可以同时发起多个toolcall，模型要知道每个结果归谁

---

## 3. 排错：State 变了但 Prompt 没变（4 分）

日志已经证明：

```python
state["active_agent"] == "support_agent"
```

但下一次模型调用仍然使用分诊 Prompt 和分诊 tools。

请写出两个比“没有 checkpointer 或 thread_id”更直接的排查点，并说明各自的修复方向。

我的答案：

直接打印State检查消息列表数据

---

## 4. `State`、`ModelRequest` 与 `handler`（4 分）

判断并解释下面四句话：

1. `request.override(...)` 直接修改了共享 State。
2. `request.override(...)` 返回修改后的 `ModelRequest`。
3. `handler(updated_request)` 接收更新后的请求并继续模型调用。
4. 模型主要消费的是原始 State 字典，而不是 `messages`、system Prompt 和 tools。

我的答案：

1. overide知识修改了对模型的请求，并没有直接修改State
2. 对的
3. 对的
4. 不对，但是不清楚不对在哪

---

## 交卷格式

答完后直接告诉我“答完了”。我会依据 [第 31 章教学文档](</Users/enkidu/PyCharmMiscProject/md/31_Multi-Agent与复杂工作流.md>) 批改，并把结果追加到本文件。

## 补考批改结果（2026-07-31）

| 题号 | 得分 | 批改 |
| --- | ---: | --- |
| 1 | 8/8 | Handoff 的核心顺序完整：`Command` 更新 State，Agent loop 继续，middleware 读取新状态，`select_prompt` 选择配置，`override` 生成新请求，`handler` 继续模型调用。 |
| 2 | 4/4 | 正确区分普通字符串与 `Command(update=...)`，并说明了 `tool_call_id` 用于对应具体工具调用。补充：`Command` 的路由控制属于它更广泛的能力，本题重点是 State 更新。 |
| 3 | 0/4 | 只检查了 State，而题目已经明确 State 已经变为 `support_agent`。还需要检查 middleware 是否注册、`select_prompt` 是否读取 `request.state`、`override` 的结果是否传给 `handler`，以及工具子集是否按角色切换。 |
| 4 | 3/4 | 前三项判断正确。第 4 项虽然判断“不对”正确，但没有解释：模型主要接收由框架从 State 整理出的 `messages`、system Prompt 和 tools；原始 State 是 middleware 和 Agent loop 使用的内部状态。 |

**总分：15/20（75%）**

### 评定：🟡 补漏后基本掌握

你已经掌握本章最重要的 Handoff 主链路，不需要重学整章。剩余薄弱点只有一个：当 State 已更新但 Prompt / tools 没切换时，要沿着 `middleware -> select_prompt -> override -> handler` 检查请求改造链，而不是优先怀疑 `checkpointer` 或 `thread_id`。

### 一句话复盘

`State` 是框架内部共享状态；middleware 读取它并改造 `ModelRequest`；模型主要消费改造后的 `messages`、Prompt 和 tools，而不是直接消费原始 State 字典。
