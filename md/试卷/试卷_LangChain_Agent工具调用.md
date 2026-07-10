# 试卷：LangChain Agent 工具调用

> 目标：确认你能把第 26 章手写 Function Calling Loop、第 27 章对话记忆、第 28 章 LangChain Agent 串起来。  
> 本卷重点不是死背 API，而是判断边界、修正代码、解释真实报错。

---

## 答题说明

- 总分：100 分
- 通过线：90 分以上继续下一章；70-89 分补漏；低于 70 分重学关键关卡。
- 允许大致描述命令，不要求完整背命令。
- 不需要运行真实模型 API。

---

## 一、核心概念判断题（20 分）

每题 4 分。判断对错，并用一句话说明理由。

### 1. `create_agent(...)` 会立刻向模型发送用户问题。

我的答案：不会，create_agent是创建agent实例


### 2. `agent.invoke(...)` 返回的一定是字符串，所以可以直接 `print(result)` 得到最终回答。

我的答案：错误的，agent.invoke 返回的是state实例，需要对里面的属性进行取值


### 3. 第 26 章的 `TOOLS` 可以直接等价替换第 28 章 `create_agent(..., tools=...)` 里的 `tools`。

我的答案：不行create_agent 里面的 tools 接收的是一个 用@tool装饰器包装的工具函数


### 4. `@tool` 函数里的 docstring 只是普通注释，模型看不到。

我的答案：不，@tool 装饰器会让函数定义的第一行的注释被模型给读取到


### 5. 只要创建了 Agent，不配置 `checkpointer` 也会自动记住上一轮对话。

我的答案：不，必须陪许


---

## 二、流程题：Agent 到底封装了什么（15 分）

请按顺序写出 LangChain Agent 一次工具调用的大致流程。

要求包含这些关键词：

```text
用户消息
模型
tool_call
后端工具函数
ToolMessage / tool output
最终回答
```

我的答案：


---

## 三、代码填空题：最小 Agent 骨架（15 分）

请补全空白处。

```python
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def search_project_knowledge(query: str, limit: int = 3) -> str:
    """______________________________"""
    docs = search_knowledge_base(query=query, limit=min(limit, 5))
    if not docs:
        return "没有检索到相关内容。"

    return "\n\n".join(
        f"[{index}] {doc.page_content[:800]}"
        for index, doc in enumerate(docs, start=1)
    )


agent = create_agent(
    model=______,
    tools=[______],
    system_prompt="你是一个严谨的知识库助手。",
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "退款需要几天内申请？",
            }
        ]
    }
)

answer = result["messages"][-1].______
```

我的答案：


---

## 四、代码纠错题：`TOOLS` 和 `tools`（10 分）

下面代码有什么问题？应该怎么改？

```python
from app.tools.registry import TOOLS

agent = create_agent(
    model=llm,
    tools=TOOLS,
)
```

我的答案：


---

## 五、代码解释题：格式化 Document（10 分）

解释下面代码最终输出的大致格式，以及三部分分别负责什么。

```python
"\n\n".join(
    f"[{index}] {doc.page_content[:800]}"
    for index, doc in enumerate(docs, start=1)
)
```

请分别解释：

```text
enumerate(docs, start=1)
f"[{index}] {doc.page_content[:800]}"
"\n\n".join(...)
```

我的答案：


---

## 六、报错诊断题：AIMessage 不能这样取值（10 分）

运行时报错：

```text
TypeError: 'AIMessage' object is not subscriptable
```

出错代码：

```python
answer = result["messages"][-1]["content"]
```

请解释为什么错，并写出正确写法。

我的答案：


---

## 七、报错诊断题：checkpointer 缺少 thread_id（10 分）

运行时报错：

```text
ValueError: Checkpointer requires one or more of the following 'configurable' keys:
thread_id, checkpoint_ns, checkpoint_id
```

相关代码：

```python
agent = create_agent(
    model=llm,
    tools=[search_project_knowledge],
    checkpointer=InMemorySaver(),
)

second_result = agent.invoke(
    {"messages": [{"role": "user", "content": "上面的对话说了什么？"}]}
)
```

请解释为什么错，并写出应该补什么。

我的答案：


---

## 八、边界题：state/messages 和传统 memory（10 分）

请回答：

1. `agent.invoke(...)` 返回的 `result` 可以近似理解成什么？
2. `result["messages"]` 是什么？
3. 它和上一章 `langchain_memory.py` 里的传统聊天历史有什么区别？

我的答案：


---

## 九、业务设计题：user_id、conversation_id、thread_id（10 分）

实际业务里，下面三个 ID 分别更适合表示什么？

```text
user_id
conversation_id / session_id
thread_id
```

如果前端传入：

```json
{
  "conversation_id": "conv_001",
  "message": "继续刚才的话题"
}
```

后端调用 Agent 时，`thread_id` 可以怎么设置？为什么？

我的答案：


---

## 自查清单

交卷前确认：

- [ ] 我能说清 `create_agent` 和 `agent.invoke` 的区别。
- [ ] 我没有把第 26 章的 `TOOLS` 当成第 28 章的 `tools=[...]`。
- [ ] 我知道 `@tool` docstring 会变成模型可见工具描述。
- [ ] 我知道 Tool output 最好返回字符串。
- [ ] 我知道最终回答通常用 `result["messages"][-1].content`。
- [ ] 我知道有 `checkpointer` 时每次 invoke 都要传 `thread_id`。
- [ ] 我知道 `state/messages` 是 Agent 的运行轨迹，不只是传统聊天历史。

---

## 批改区

> 等你答完后，把答案发给我。我会把评分、错题、补救建议追加到这里。
