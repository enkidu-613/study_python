# 30. Dify 平台实战：把你写过的 RAG 画成可运行工作流

> 本章目标：你能在 Dify 里搭出一条“用户问题 -> 知识检索 -> LLM 回答 -> 输出”的 RAG 工作流，并能通过 API 从 FastAPI 调用它。
>
> 本章不学习 Dify 插件开发、复杂循环、Agent 策略或生产部署。先把你已经写过的 RAG 闭环在可视化画布上走一遍。

## 权威来源

| 来源 | 本章采用的结论 |
| --- | --- |
| [Dify 30-Minute Quick Start](https://docs.dify.ai/en/quick-start) | 先配置模型提供商，再从 Studio 创建 Workflow，并从 `User Input` 节点开始搭建。 |
| [Test Knowledge Retrieval](https://docs.dify.ai/en/cloud/use-dify/knowledge/test-retrieval) | 文档处理完成后，可先用真实问题检查召回的片段是否含有预期证据。 |
| [Run Workflow API](https://docs.dify.ai/en/api-reference/workflow-runs/run-workflow) | 已发布工作流可通过 `POST /workflows/run` 调用；阻塞响应的输出位于 `data.outputs`。 |

## 一句话理解

Dify 是把模型、知识库、Prompt 和流程节点配置在画布上的平台；它不替代你理解 RAG，而是把你已经写过的 RAG 流程变成可观察、可配置的应用。

## 先看真实对象长什么样

本章主要操作的是 Dify 的**工作流画布**里的对象，而不是 Python 类：

| Dify 画布对象 | 它是什么 | 对应你项目里的什么 |
| --- | --- | --- |
| User Input | 工作流输入变量的声明节点 | FastAPI 请求体里的 `question` |
| Knowledge Retrieval | 查询知识库并输出切片的节点 | `similarity_search(query, k=...)` |
| LLM | 调用模型并组合 Prompt 的节点 | `ChatDeepSeek(...).invoke(...)` |
| Output | 声明工作流的返回变量 | FastAPI `return {...}` |
| Variable | 节点输出在画布中的名字 | Python 变量或 State 字段 |

先在 Dify Studio 创建 `Workflow`，不是 Chatflow 或 Chatbot。Workflow 使用 `Output` 节点把结果返回给 API 调用者；Chatflow 对应的是 `Answer` 节点。工作流可以明确地把输入、节点输出和最终输出连成一条线。

```text
User Input(question)
  -> Knowledge Retrieval(query=question)
  -> LLM(context=检索结果, question=question)
  -> Output(answer=LLM 输出)
```

这条线和你第 13、23、24 章的 RAG 闭环是同一件事：检索不是回答，LLM 必须读取检索结果后才生成答案。

## 开始前：让三个真实对象先可用

先不要连画布。准备好下面三个对象后，再搭最小流程：

1. 打开 `Integrations > Model Provider`，安装并配置一个可用的聊天模型（使用 Dify 提供的额度或填入你自己的 Provider API Key）。**成功标准：**在模型提供商页面能看到该模型可选；打开 LLM 节点时能在模型下拉列表中选中它。
2. 打开 `Knowledge`，新建知识库并上传一份明确写有退款规则的文档，例如包含“退款须在购买后 7 天内申请”。等待文档处理完成。**成功标准：**文档状态显示为 `Completed`，而不是处理中或失败。
3. 在该知识库的 `Test Retrieval` 中输入“退款需要几天内申请？”。**成功标准：**返回的前几个片段能直接看到“7 天内申请”或你的文档中的等价退款规则；拿不到这条证据就先修文档或检索设置，不要连画布、更不要调 Prompt。

## 第一关：搭出最小 RAG 工作流

### 1. User Input 节点：先声明输入

在 `User Input` 节点新增一个字段：

```text
变量名：question
类型：Short Text
必填：是
```

`question` 是运行时数据。后面的 Knowledge Retrieval 和 LLM 都引用同一个 `User Input/question`，而不是把问题硬编码在 Prompt 里。

### 2. Knowledge Retrieval 节点：真正取回证据

添加 Knowledge Retrieval 节点，选择你已经测试过的知识库。将它的 query 绑定到 `User Input/question`。

它的输出是“若干相关文档片段”，不是最终回答。这里对应你项目里的：

```python
docs = get_vector_store().similarity_search(query, k=3)
```

立即测试一次，例如输入：

```text
退款需要几天内申请？
```

检查检索节点日志：返回的片段里是否真的出现退款规则。没有证据时，不要急着调 Prompt，先检查知识库是否上传、分块和索引是否正确。

### 3. LLM 节点：把问题和证据同时交给模型

添加 LLM 节点。它至少需要两个动态变量：用户问题和检索结果。Prompt 的核心不是花哨措辞，而是证据边界：

```text
你是知识库问答助手。
仅根据下面的检索结果回答；检索结果没有答案时，明确说“知识库中没有找到依据”。

问题：{{question}}

检索结果：{{Knowledge Retrieval 的输出}}
```

变量名以你画布显示的节点和字段为准，Dify 会在编辑器中提供变量选择器；不要手打猜变量路径。

### 4. Output 节点：声明 API 真正返回什么

在 `Output` 节点选择 LLM 节点的文本输出，命名为：

```text
answer
```

`Output` 不是“再调用一次模型”，它只是把某个节点的结果暴露为工作流输出。它是 Workflow 的节点；Chatflow 要把内容回复到对话中时使用 `Answer` 节点。

## 第二关：在画布上追一次数据流

输入：

```text
退款需要几天内申请？
```

按顺序查看每个节点的输入和输出：

```text
User Input 输出 question
-> Knowledge Retrieval 输入 question，输出 chunks
-> LLM 输入 question + chunks，输出 answer
-> Output 输出 answer
```

这就是你当前项目中 `page_content`、Prompt 和模型回答的可视化版本。Dify 的节点日志是调试证据，不能只看最后回答“像不像对”。

## 第三关：从 FastAPI 调用已发布工作流

发布 Workflow 后，Dify 给出 API Base URL 和应用 API Key。Key 只能放服务端环境变量，不能放前端或提交到 Git。

```python
import os

import httpx


async def run_dify_workflow(question: str, user_id: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{os.environ['DIFY_API_BASE']}/workflows/run",
                headers={
                    "Authorization": f"Bearer {os.environ['DIFY_API_KEY']}",
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": {"question": question},
                    "response_mode": "blocking",
                    "user": user_id,
                },
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError("Dify workflow request failed") from exc

    return str(response.json()["data"]["outputs"]["answer"])
```

这里每个对象的职责：

| 代码 | 含义 |
| --- | --- |
| `DIFY_API_BASE` | 你的 Dify 服务 API 地址，不是工作流名称。 |
| `DIFY_API_KEY` | 调用该应用的服务端密钥。 |
| `inputs` | 必须和 `User Input` 节点声明的变量名匹配。 |
| `user` | 后端从已认证用户稳定派生的标识；用于关联该用户的运行记录和选定资源。 |
| `response_mode="blocking"` | 等工作流完成再返回 JSON。 |

`user` 不是登录凭证：Dify 不会认证它，绝不能直接相信前端传来的任意字符串。先由你的后端完成会话或 Token 验证，再从已认证用户派生稳定值，例如 `user:{account_id}`。它用于让 Dify 关联同一用户的运行与已选资源，不是知识库的授权机制；知识库访问控制仍应由你的后端、Dify 工作区权限和应用配置分别负责。

想得到 SSE 时把 `response_mode` 改为 `streaming`，并用流式 HTTP 客户端消费 `text/event-stream`。这和你第 18 章的 WebSocket 不同：Dify 这里是服务器向客户端推送事件。

## 常见坑

1. 只给 LLM 传问题，没有传检索结果：这不是 RAG，模型会凭已有知识回答。
2. 把检索节点输出当作最终答案：它只是证据片段，仍需 LLM 组织回答。
3. 修改画布后没有 Publish：测试画布能运行，不代表 API 使用的是最新版。
4. 把 API Key 放前端：任何拿到浏览器代码的人都可能调用你的 Dify 应用。

## 三遍主动练习

### 1. 读懂

不看文档，说出 User Input、Knowledge Retrieval、LLM、Output 分别输入和输出什么。

### 2. 跟写

创建一个“项目知识问答”工作流，只接四个节点。用一个知识库确实没有的提问测试，确认 LLM 会说明没有依据。

### 3. 独立重写

把场景换成“课程资料问答”：输入 `question`，检索课程资料，输出 `answer` 和 `sources`。先在 Output 节点暴露两个输出，再决定 FastAPI 如何返回它们。

## 本章边界与检查点

本章学习 Dify 如何复现你已掌握的 RAG；不学习插件开发、复杂 Agent 路由或 Dify 的生产部署。

你能回答下面五条，就可以进入下一章：

1. Dify 的 Knowledge Retrieval 节点和 `similarity_search()` 对应什么关系？
2. 为什么 LLM 节点必须同时收到问题和检索结果？
3. Output 节点与 LLM 节点的职责有什么区别？为什么 Chatflow 不用 Output？
4. 为什么要在连画布前先完成 Test Retrieval？
5. `POST /workflows/run` 的 `inputs`、`user`、`response_mode` 分别负责什么？为什么不能把前端原样传来的 `user` 当作可信身份？

> 教学方式：具体锚点优先。先在画布中创建真实节点并测试一次，再为它们命名和解释架构。
