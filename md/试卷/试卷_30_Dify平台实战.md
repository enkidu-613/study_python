# 试卷：Dify 平台实战

> 目标：确认你能把 Dify 的 Workflow、知识检索、Workflow Tool、Agent 工具循环和 FastAPI 调用连接起来。

## 答题说明

- 总分：100 分
- 90 分以上：通过，标记 Dify 阶段完成
- 70-89 分：只补薄弱点，不重学整章
- 低于 70 分：回到关键关卡重新学习
- 可以用自己的话回答，不要求背完整菜单名称或 import 路径。
- 代码题只看核心结构和数据流，不因标点、缩进风格或 IDE 提示单独扣分。
- 请直接在每道题的“我的答案”后作答。

## 第一轮：核心概念（20 分）

每题 4 分。

### 1. Workflow 与 Chatflow

本章为什么使用 Workflow，而不是 Chatflow？两者分别适合什么场景？

我的答案：
workflow适合作为工具的一次对话场景，chatflow是有记忆的，适合做机器人聊天等

### 2. Dify 知识库的边界

Dify 的知识库和你项目中的 SQL/ORM 数据库、Chroma 向量库有什么区别？为什么 Dify Cloud 不会自动读取项目里的数据库？

我的答案：
不会，因为dify cloud根本就没有出现在我本地项目中

### 3. 变量和输出

请解释下面四个变量各自代表什么：

```text
question
query
result / results
answer
```

并说明它们分别出现在什么位置。

我的答案：
question 出现在用户输入 query出现在查询知识库环节中，result出现在知识库返回的切片中，answer是最终回答


### 4. 固定 RAG 与 Agentic RAG

请分别写出固定 RAG 和 Agentic RAG 的画布流程，并说明两者最重要的区别。

我的答案：
是dify的固定知识库查询节点，另一个是dify的agent以及工具？我没在文档里看到过

### 5. Output 节点

Output 节点的作用是什么？为什么把输出变量命名为 `answer` 后，FastAPI 可以从 `data.outputs.answer` 读取它？

我的答案：
输出最终回答，应该是他是什么名字fastapi就要用什么名字

## 第二轮：机制与边界（30 分）

每题 6 分。

### 6. Dify Agent 与 LangGraph 的对应关系

请把下面四组概念一一对应，并说明每一组在执行中负责什么：

```text
llm.bind_tools(tools)
ToolNode(tools)
tools_condition
model -> tools -> model
```

对应 Dify Agent 中的：模型和工具、工具执行、条件判断、迭代循环。

我的答案：
1. agent节点 读取了给模型看的工具说明书，可以使用tool_call让后端调用工具
2. 对应agent节点的工具列表，给后端使用的可以调用的工具列表
3. 对应agent策略？对model返回的逻辑进行判断，如果还是tool_call就继续迭代
4. 模型返回tool_call -> 工具返回结果 ->模型读取结果决定是继续调用还是进行最终回答


### 7. 为什么要把检索单独做成 Workflow Tool？

为什么主 Agent Workflow 不直接放 Knowledge Retrieval 节点，而要先创建：

```text
开始(query) -> 知识检索 -> 输出(results)
```

再把它发布为工具？

我的答案：
没有开始的 用户输入先放知识检索，没有问题就没有检索返回的结果

### 8. `result: []` 说明什么？

Dify 知识检索节点显示绿色成功，但输出是：

```json
{"result": []}
```

这能否说明检索节点报错？你应该优先检查哪些内容？

我的答案：
不能，可能是没有检索到相关内容，也可以看看是否是向量检索，dify的经济检索有时候会查不到


### 9. HTTP 成功不等于 Workflow 成功

为什么下面两种情况必须分别处理？

```text
HTTP 401 / 404 / 500
HTTP 200，但 data.status == "failed"
```

分别应该由什么检查发现？

我的答案：
第一种可能是鉴权和服务器内部错误，第二种可能是dify调用或者本身有问题

### 10. API Key、user 与 Maximum Iterations

请解释：

1. `DIFY_API_KEY` 应该放在哪里，为什么不能放前端？
2. `user` 参数负责什么，为什么它不是登录凭证？
3. `Maximum Iterations` 解决什么问题，为什么它不是权限控制？

我的答案：
1. env
2. user参数是dify 负责标记对话是属于谁的，不是登陆凭证
3. 这个我不知道，没在教学文档看到

## 第三轮：场景与排错（30 分）

每题 10 分。

### 11. Agent 没有调用检索工具

主 Agent 的运行追踪只有：

```text
question -> Agent -> final answer
```

没有出现 `tool call` 或工具结果。

请写出至少四项排查内容，并说明排查顺序。

我的答案：
检查工具是否存在，检查工具配置，后面忘了

### 12. `Collection not found` 与 Embedding 凭证错误

你遇到过下面两类错误：

```text
Collection not found
Model qwen3-embedding-0.6b credentials is not initialized
```

请说明它们分别更可能属于哪一层的问题，并写出你的修复顺序。不要把它们都归因于 Prompt。

我的答案：
我忘记了

### 13. API 返回 200，但没有 `answer`

FastAPI 调用 Dify 后得到 HTTP 200，但响应中没有：

```json
data.outputs.answer
```

请写出至少五步排查过程，要求包含：发布版本、`data.status`、`data.error`、Output 节点和 `inputs` 字段名。

我的答案：
我知道怎么找，但是我写不出来

## 第四轮：独立设计（20 分）

### 14. 独立搭建课程资料 Agentic RAG

请为“课程资料问答”设计一套 Dify 方案。要求：

1. 写出检索工具 Workflow 的画布结构。
2. 写出主 Agent Workflow 的画布结构。
3. 写出检索工具的输入变量和输出变量。
4. 写出 Agent 的核心指令，要求只依据工具返回的资料回答。
5. 写出一次成功运行时应看到的追踪顺序。
6. 写出一个知识库没有答案时的验证问题和预期行为。

我的答案：


## 第五轮：实践验收记录（不单独加分，作为通过条件）

请在完成答题后补充实际验证结果：

```text
[ ] 检索 Workflow 返回过非空 results
[ ] 主 Agent 追踪出现过 tool call 和 tool result
[ ] 主 Agent 根据检索结果生成最终回答
[ ] FastAPI POST /dify/rag 返回 HTTP 200
[ ] FastAPI 能取得 Dify Workflow 的最终输出
[ ] 知识库没有答案时，Agent 没有编造事实
```

我的实践记录：全都实践了

## 通过记录

- 结果：通过
- 方式：实践验收通过，书面画布结构题豁免
- 日期：2026-07-25
- 依据：已实际跑通知识检索、Agent 工具调用、Dify Workflow 发布，以及 FastAPI `POST /dify/rag` 调用。


## 交卷格式

答完后直接告诉我“答完了”。我会依据 [第 30 章 Dify 平台实战](</Users/enkidu/PyCharmMiscProject/md/30_Dify平台实战.md>) 批改：先给分，再逐题讲解错题，并把真正需要复习的内容写入错题本。
