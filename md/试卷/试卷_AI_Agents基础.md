# 试卷：AI Agents 基础

> 答题规则：
>
> - 不需要背完整代码，重点写出调用链和边界。
> - 可以用你自己的话回答，但术语要尽量准确。
> - 本章不要求你真的写完整 Agent 接口；只要求你能读懂和画出最小 Agent Loop。
> - 满分 100 分，90 分以上通过，70-89 分补漏，低于 70 分回到关键关卡重学。

---

## 一、核心概念题

### 1. 一句话解释 Agent（10 分）

请用一句话说明 AI Agent 是什么。必须包含下面四个词里的至少三个：

```text
LLM / Tools / Loop / Safety
```

答题区：

```text
agent 是一个会在思考、调用工具、观察结果、继续决策之间循环的 ai 程序
```

---

### 2. 普通聊天、RAG、Agent 的区别（12 分）

分别说明下面三者最核心的区别：

```text
普通聊天：

RAG：

Agent：
```

答题区：

```text
1. 只适合问答和对文本的处理
2. 适合知识库搜索问答
3. 可以自主决定要不要调用搜索知识库还是查看天气的工具
```

---

## 二、Tool 与 Function Calling

### 3. 区分 Tool、Tool Schema、Tool Call、Tool Output（16 分）

请用自己的话解释：

```text
Tool：

Tool Schema：

Tool Call：

Tool Output：
```

答题区：

```text
1. tool 就是开放给模型使用的后端函数，模型并不能亲自调用只是说：“我想要执行后端函数，参数{query:"我想要查找xxxx"}”
2. tool schema 就是给模型看的约定好的 tool 说明书， 说明了模型名称用途，以及参数和参数类型必填参数是什么
3. tool call 是模型吐出的，交给后端去寻找函数执行的一个数据结构
4. tool output 工具执行结果，也就是后端执行tool function 后返回给模型的结果
```

---

### 4. Function Calling 是否等于模型直接执行函数？（10 分）

判断并解释：

```text
Function Calling 就是模型直接调用 Python 函数。
```

这个说法对不对？为什么？

答题区：

```text
不对， function calling 时描述 模型调用tool 时的流程，而模型调用tool的时候并不是直接调用，是吐出tool call 交给后端去执行
```

---

## 三、Tool Schema 与 Registry

### 5. required 应该放在哪个层级？（10 分）

下面这段 schema 还缺一行。请补出 `required`，并说明它和 `properties` 是什么关系。

```python
TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "在知识库中搜索相关文档切片，并返回结果列表。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要搜索的查询字符串。"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回的结果数量限制。"
                }
            }
            # 这里补 required
        }
    }
]
```

答题区：

```python
TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "在知识库中搜索相关文档切片，并返回结果列表。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要搜索的查询字符串。"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回的结果数量限制。"
                }
            },
            # 这里补 required
            "required":["query"]
        }
    }
]
# 都是工具传参结构底下的，parameters是描述参数类型介绍做什么，require是描述某个参数是不是必填
```

---

### 6. `TOOLS` 和 `TOOL_FUNCTIONS` 分别给谁用？（12 分）

解释下面两个变量的职责：

```python
TOOLS = [...]

TOOL_FUNCTIONS = {
    "search_knowledge_base": search_knowledge_base,
}
```

答题区：

```text
TOOLS：是把所有的工具说明书集合成一个列表，发给大模型看

TOOL_FUNCTIONS：给后端调用的函数映射列表，是说明书介绍的函数本身的映射列表

为什么要分成两份：分类更加清晰，调用的时候不会混
```

---

## 四、最小 Agent Loop

### 7. 画出最小 Agent Loop（15 分）

请用文字画出一个最小 Agent Loop。必须包含：

```text
用户输入
模型判断
tool call
后端执行工具
tool output
模型生成最终回答
```

答题区：

```text
用户输入-> 模型判断 -> tool call -> 后端执行工具 -> tool output -> 模型生成最终回答
```

---

### 8. 什么时候不应该调用 `search_knowledge_base`？（8 分）

当前工具是只读知识库搜索工具：

```python
def search_knowledge_base(query: str, limit: int = 3):
    ...
```

请举出两个不应该调用它的场景。

答题区：

```text
场景 1：用户只是闲聊： 你好、谢谢、讲个笑话

场景 2：用户只是让模型改写文本，翻译文本总结用户刚刚发来的内容

这里的核心是 search_knowledge_base 只适合需要查找本项目知识库的问题
```

---

## 五、安全边界

### 9. 为什么高风险工具不能只靠 Prompt 控制？（12 分）

例如：

```text
删除数据
发邮件
扣费
修改用户权限

这里可以补上 ：审计日志 audit log 这里的审计日志就是audit，放在后端或者agent 安全里就是：记录谁，在什么时候，对什么东西，做了什么操作，结果如何
```

为什么不能只在 prompt 里写“不要乱调用”？后端还应该做什么？

答题区：

```text
因为propmt很容易被绕过， 后端应该进行检查用户是否登陆，权限校验，提示用户对是否使用工具进行确认
```

---

## 六、项目代码判断题

### 10. 读代码判断职责（5 分）

你当前项目中：

```text
app/tools/knowledge_base.py
app/tools/registry.py
```

分别更适合放什么？

答题区：

```text
knowledge_base.py：放工具代码

registry.py：放工具说明书列表 和允许使用的被说明书描述的工具函数列表
```

---

## 自评分

写完后先自己标一下：

```text
我最确定的 2 题：

我最不确定的 2 题：

我觉得自己有没有掌握本章最小 Agent Loop：我个人拿不准，请您确定我是不是掌握了
```

---

## 批改结果

批改时间：2026-07-04

总分：96 / 100，通过。

### 分题得分

```text
1. 一句话解释 Agent：10 / 10
2. 普通聊天、RAG、Agent 区别：10 / 12
3. Tool / Tool Schema / Tool Call / Tool Output：16 / 16
4. Function Calling 边界：9 / 10
5. required 层级：7 / 10
6. TOOLS 与 TOOL_FUNCTIONS：8 / 12
7. 最小 Agent Loop：15 / 15
8. 不该调用 search_knowledge_base 的场景：6 / 8
9. 高风险工具安全边界：10 / 12
10. 项目代码职责：5 / 5
```

### 已掌握

你已经掌握本章最小 Agent Loop。你的第 7 题能把“用户输入 -> 模型判断 -> tool call -> 后端执行工具 -> tool output -> 最终回答”完整串起来，这就是本章核心。

Tool / Tool Schema / Tool Call / Tool Output 的边界答得很好，尤其是你写出“模型并不能亲自调用，只是吐出调用请求交给后端执行”，说明 Function Calling 的关键边界已经接上。

### 批改修正

第 1 题原本因为没有明确写出 `Safety` 扣 2 分，但第 25 章开头“一句话理解”也没有把 Safety 写进句子里，只在后面的结论和检查点中出现。这个扣分不公平，已改为满分。

### 需要补的两个小点

1. `required` 的准确写法是：

```python
"required": ["query"]
```

它和 `"properties"` 同级，都在 `"parameters"` 里面。你概念位置对了，但 Python 字典写法少了引号和冒号前的字符串 key。

2. `TOOL_FUNCTIONS` 不是给模型看的工具列表，而是后端用来按名字找到真实 Python 函数的映射：

```python
TOOL_FUNCTIONS = {
    "search_knowledge_base": search_knowledge_base,
}
```

一句话：`TOOLS` 给模型看，`TOOL_FUNCTIONS` 给后端执行用。

### 最小复习计划

明天只复习两点：

```text
1. required 和 properties 的层级关系是什么？
2. TOOLS 和 TOOL_FUNCTIONS 为什么要分开？
```

本章可以标记为完成。下一阶段开始前，先用一个桥接小节把 Function Calling 的执行 loop 写清楚，再进入更高层的 LangChain Agent。
