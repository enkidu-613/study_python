# 试卷：Function Calling 执行 Loop

> 章节：`md/26_Function_Calling执行Loop.md`  
> 状态：已批改  
> 规则：不用背完整 SDK 参数名，但必须说清楚执行链路、对象边界和安全边界。

---

## 一、核心流程题

### 1. 完整执行链路（20 分）

请按顺序写出一次 Function Calling 从用户提问到最终回答的完整流程。

要求必须包含：

- `TOOLS`
- `tool_call`
- `arguments`
- `TOOL_FUNCTIONS`
- `role="tool"`
- 最终回答

答题区：

```text
首先给模型配置tools，然后用户提问问题，模型生成tool_call交给后端，后端校验解包arg塞进对应函数执行，前提是TOOL_FUNCTIONS 里面有该函数，对此后端也需要进行校验，role=“tool”：模型需要知道这是自己调用的那个工具的结果
```

---

## 二、概念边界题

### 2. `TOOLS`、`tool_call`、`TOOL_FUNCTIONS` 分别是什么？（18 分）

请分别说明它们：

- 给谁用？
- 里面大概放什么？
- 是否会直接执行 Python 函数？

答题区：

```text
TOOLS：给模型用，模型需要知道可用的工具有哪些，还有工具的说明书

tool_call：给后端使用的，后端需要知道模型要调用的是什么工具，如果工具存在权限正确，则返回结果给模型

TOOL_FUNCTIONS：给后端使用的工具函数映射列表

```

---

### 3. Function Calling 是否等于模型直接执行函数？（10 分）

请判断下面说法是否正确，并解释原因：

```text
Function Calling 就是模型根据工具名直接运行后端 Python 函数。
```

答题区：

```text
并非，这是从模型到后端一整套循环
tools->model->tool_call->backend->result->modle->最终回答
```

---

## 三、代码理解题

### 4. 为什么是 `tool_call.function.name`？（12 分）

请解释为什么第五关中取工具名使用：

```python
tool_name = tool_call.function.name
```

而不是：

```python
tool_name = tool_call.name
tool_name = tool_call.get("name")
```

答题区：

```text
因为对象顶层只有id type function 而 name 参数在  function 属性内部
```

---

### 5. 为什么要 `json.loads(arguments)`？（12 分）

模型返回的 `tool_call.function.arguments` 通常是什么类型？  
为什么不能直接把它传给工具函数？

答题区：

```text
通常是json字符串，直接赋值会导致出现错误 json字符串也不能接包，所以需要反序列化为dict字典
```

---

### 6. 读代码说含义（12 分）

请逐行解释下面代码在做什么：

```python
tool_func = TOOL_FUNCTIONS[tool_name]
tool_result = tool_func(**tool_args)
```

答题区：

```text
将列表内的映射的函数赋值给变量，执行这个被赋值函数的变量，使用反序列后的dict然后解包的参数填充
```

---

## 四、安全与边界题

### 7. 为什么不能完全信任模型给的 arguments？（8 分）

请至少说出两个原因。

答题区：

```text
因为模型给的不一定是正确的json格式，在实战中还是需要使用后端约束，类似于使用shcema加上方法约束，给后端的时候也要再加上一层额外校验
```

---

### 8. 为什么需要 `MAX_STEPS`？（8 分）

如果没有循环上限，Agent Loop 可能出现什么问题？

答题区：

```text
ai不停调用工具，如果出现错误或者死循环，会把token耗尽
```

---

## 五、项目识别题

### 9. 当前项目里哪些文件对应本章概念？（10 分）

请根据你当前项目回答：

- 工具说明书在哪里？
- 工具函数映射在哪里？
- 知识库搜索工具在哪里？
- 普通模型调用代码在哪里？

答题区：

```text
1. TOOLS registry.py
2. TOOL_FUNCTIONS registry.py
3. knowleedge_base.py search_knowledge_base
4. ai.py
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

> 批改时间：2026-07-06  
> 得分：92 / 100  
> 结论：通过。本章主干已经掌握，可以进入收尾复盘；只需要补两处薄弱点。

---

## 逐题评分

| 题号 | 得分 | 说明 |
| --- | ---: | --- |
| 1 | 17 / 20 | 主流程正确，包含 `TOOLS`、`tool_call`、`arguments`、`TOOL_FUNCTIONS`、`role="tool"`。扣分点：没有明确写出“把 tool output 放回 messages 后，再次请求模型生成最终回答”。 |
| 2 | 14 / 18 | `TOOLS` 和 `TOOL_FUNCTIONS` 基本正确。`tool_call` 说成“给后端使用”是对的，但需要更精确：它是模型返回的调用申请单，本身不返回结果，也不直接执行函数。 |
| 3 | 9 / 10 | 判断正确，知道不是模型直接运行 Python，而是完整 loop。表达里 `modle` 拼写不影响概念。 |
| 4 | 10 / 12 | 知道顶层是 `id/type/function`，`name` 在 `function` 内部。可再补一句：这是 SDK 对象，所以不是 `.get()`。 |
| 5 | 11 / 12 | 正确：`arguments` 通常是 JSON 字符串，需要 `json.loads` 反序列化为 dict 后才能 `**` 解包。 |
| 6 | 9 / 12 | 主体正确。小扣分：`TOOL_FUNCTIONS` 不是列表，而是 dict 映射表；`TOOL_FUNCTIONS[tool_name]` 是用工具名字符串取到真实函数对象。 |
| 7 | 5 / 8 | 方向正确：模型参数不可靠，需要后端约束和校验。扣分点：题目要求至少两个原因，你只明确写了“JSON 格式可能不正确”。还应补：缺少必填字段、类型错误、limit 过大、工具名不存在、参数越权等。 |
| 8 | 8 / 8 | 正确：防止工具循环、错误循环、Token 被耗尽。 |
| 9 | 9 / 10 | 文件识别正确。`knowledge_base.py` 拼写有误但不影响判断；完整路径更好：`app/tools/registry.py`、`app/tools/knowledge_base.py`、`app/routers/ai.py`。 |

---

## 你的真实掌握度

你自评 70/100 偏低。按答卷看，你现在大概是：

```text
Function Calling 执行 Loop：90% 左右
```

已经掌握：

```text
TOOLS 给模型看
tool_call 是模型返回的调用申请单
arguments 要反序列化
TOOL_FUNCTIONS 是后端函数映射
后端执行工具
role="tool" 表示工具结果
MAX_STEPS 防止无限循环
```

还要补牢：

```text
tool output 放回 messages 后，需要再次请求模型生成最终回答
模型给的 arguments 可能有多种不可靠情况，不只是 JSON 格式错误
```

---

## 最小订正

请用自己的话补写两句：

```text
1. 为什么工具执行完之后，还要再次请求模型？

2. 为什么不能完全信任模型给的 arguments？请列出至少三个风险。
```

完成这两句后，本章可以标记为通过。

---

## 订正完成

用户订正：

```text
1. 工具调用后不是由用户再次提问，而是后端拿着追加了 role="tool" 的 messages 再请求模型，让模型基于工具结果生成最终回答。

2. 模型给的 arguments 可能 JSON 格式不对；即使格式对了，属性也可能不对；参数值也可能没轻没重，例如 limit=9999，所以后端必须限制和校验。
```

订正判断：

```text
通过。用户已理解“再次请求模型”是后端自动进行，不是用户重新提问；也能说出 arguments 的格式、字段和值范围三类风险。
```

最终结论：

```text
第 26 章 Function Calling 执行 Loop：通过。
最终成绩：92 / 100
```
