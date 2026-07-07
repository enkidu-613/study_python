# 试卷：LangChain 对话记忆

> 章节：`md/27_LangChain对话记忆.md`  
> 状态：已批改  
> 规则：本卷只考本章已经教过的内容，不考 LangGraph checkpointer、数据库长期记忆、复杂 Agent 记忆策略。

---

## 一、核心概念题

### 1. 四个词的区别（20 分）

请分别解释：

- `messages`
- `chat history`
- `memory`
- `state`

答题区：

```text
messages：本次请求真正发给模型的消息列表

chat history：应用保存下来的历史对话记录

memory：读取历史，注入历史，保存新消息的机制

state：应用运行中的完整状态，不只聊天

```

---

### 2. 模型为什么不会天然记住上一轮？（10 分）

请说明为什么用户上一轮说过的话，模型下一轮不一定知道。

答题区：

```text
模型本身本无状态
```

---

## 二、核心流程题

### 3. 画出带记忆调用流程（18 分）

请按顺序写出一次 `chain_with_history.invoke(...)` 背后发生的流程。

要求必须包含：

- `session_id`
- 找历史
- `MessagesPlaceholder`
- 当前 `question`
- 调模型
- 写回历史

答题区：

```text
拿到session_id，找到对应会话历史，放入MessagePlaceholder，放入当前question，调模型，写回历史
```

---

### 4. `InMemoryChatMessageHistory` 和 `RunnableWithMessageHistory` 的区别（12 分）

请说明它们分别负责什么，以及为什么不是同一个东西。

答题区：

```text
InMemoryChatMessageHistory 是标准历史对话容器
RunnableWithMessageHistory 调用前读历史，调用后写历史的封装
```

---

## 三、代码理解题

### 5. 四个变量怎么对上？（15 分）

请解释下面四行的对应关系：

```python
MessagesPlaceholder(variable_name="history")
("human", "{question}")

input_messages_key="question"
history_messages_key="history"
```

答题区：

```text
是相互对应的占位符，上面定义占位符之后下面的就需要将定义的占位符赋值给属性，分别是历史记录占位符和用户新对话占位符
```

---

### 6. `llm` 从哪里来？（8 分）

请解释为什么下面代码之前必须先定义 `llm`：

```python
chain = prompt | llm
```

在本项目里，`llm` 通常可以怎么创建？

答题区：

```text
ChatDeepSeek，ChatOpenAI 等
```

---

### 7. 判断：`HumanMessage(content="{question}")` 是否适合作为模板变量？（8 分）

请判断下面写法是否适合本章模板，并说明原因：

```python
HumanMessage(content="{question}")
```

答题区：

```text
不适合因为无法识别成占位符，传给模型的可能就是{question}
---
不过都是一个生态下的，真的没有别的办法传给这个类了？表示疑惑
```

---

## 四、会话边界题

### 8. `session_id` 是用户 ID 吗？（9 分）

请说明：

- `user_id` 表示什么？
- `session_id` 表示什么？
- 怎么判断新请求是继续旧对话，还是开始新对话？

答题区：

```text
不是
user_id 是用户id
session_id 是会话id
由前端发起请求，后端给前端一个新id，如果来的是新会话id，那就是新对话，如果是旧会话id，那就还是旧对话
```

---

## 自评区

写完后给自己标记：

```text
最稳的一题：

最不稳的一题：

我觉得自己本章掌握度：70 / 100
```

---

# 批改结果

> 批改时间：2026-07-08  
> 得分：86 / 100  
> 结论：通过但需要小补。你已经掌握本章主链路，可以继续学；补完两处订正后再标记本章完成。

---

## 逐题评分

| 题号 | 得分 | 说明 |
| --- | ---: | --- |
| 1 | 19 / 20 | 四个词基本准确。`state` 可以再补一句：它是多步 AI 流程里传递中间信息的状态包，`messages` 只是其中一部分。 |
| 2 | 6 / 10 | 方向正确：模型无状态。扣分点：回答太短，缺少“模型只看本次请求的 messages；历史必须由应用保存并重新注入”。 |
| 3 | 17 / 18 | 流程顺序正确，覆盖 `session_id`、找历史、`MessagesPlaceholder`、当前 `question`、调模型、写回历史。小扣分：`MessagesPlaceholder` 拼写少了 `s` 不影响概念。 |
| 4 | 10 / 12 | 大方向正确。可再补：`InMemoryChatMessageHistory` 只存，不会自动调用模型；`RunnableWithMessageHistory` 不负责长期存储，只负责包装 chain 的读写流程。 |
| 5 | 12 / 15 | 已知道两组占位符相互对应。还需要更明确：`question` 对当前输入，`history` 对历史消息；`input_messages_key` 对 `("human", "{question}")`，`history_messages_key` 对 `MessagesPlaceholder("history")`。 |
| 6 | 4 / 8 | 知道 `llm` 是 Chat 模型对象，但没有说明为什么要先定义，以及本项目具体用 `ChatDeepSeek(...)` 读取 `MODEL_NAME`、`MODEL_API_URL`、`MODELSCOPE_API_KEY`。 |
| 7 | 8 / 8 | 正确。`HumanMessage(content="{question}")` 不适合作为模板变量，可能把 `{question}` 原样传给模型。你提出的疑惑合理，但本章先记最稳写法。 |
| 8 | 10 / 9 | 答得很好，额外加 1 分。知道 `user_id` 和 `session_id` 的边界，也知道前端发起新旧会话、后端生成/管理/校验 ID。 |

---

## 当前掌握度

你的自评是 70 / 100，实际更接近：

```text
LangChain 对话记忆：85% 左右
```

已经掌握：

```text
messages / chat history / memory / state 的基本区别
chain_with_history.invoke 的调用流程
InMemoryChatMessageHistory 和 RunnableWithMessageHistory 的分工
question/history 变量对接
HumanMessage(content="{question}") 的坑
session_id 和 user_id 的边界
```

还要补牢：

```text
模型无状态这题要答完整：只看本次 messages，历史要外部保存并注入。
llm 来源要答完整：先创建 ChatDeepSeek，chain = prompt | llm 才能成立。
```

---

## 最小订正

请用自己的话补写两句：

```text
1. 为什么“模型本身无状态”不等于只写一句“模型无状态”就够了？完整机制是什么？

2. `chain = prompt | llm` 里的 `llm` 在本项目里应该怎么创建？至少说出 ChatDeepSeek 和三个环境变量。
```

补完这两句后，本章可以标记为完成。

---

## 订正完成

用户订正：

```text
1. 模型本身没有记忆功能，需要开发者创建 list 或者使用 LangChain 相关依赖，在模型下一次回答的时候把历史记录塞进去，这样模型才获得了记忆能力。

2. llm 需要请求地址、模型名称、api_key。
```

订正判断：

```text
通过。第 1 条已经说明外部保存历史并在下一次请求时重新注入；第 2 条已经说出模型地址、模型名称和 API Key 三个核心配置。更完整表述是：本项目里用 ChatDeepSeek(...) 创建 llm，读取 MODEL_API_URL、MODEL_NAME、MODELSCOPE_API_KEY。
```

最终结论：

```text
第 27 章 LangChain 对话记忆：通过。
最终成绩：86 / 100
```
