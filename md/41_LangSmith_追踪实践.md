# 41. LangSmith：把 LangChain 调用变成可查看的 Trace

> 本章目标：在不改业务链路的前提下，为现有 LangChain / LangGraph 调用打开 LangSmith tracing，并知道哪些数据能上传、哪些不能上传。

## 一句话心智模型

LangSmith 是观测平台，不是模型、不是 Agent 框架，也不替你做 RAG。它接收运行事件，将一次链路组织成 trace，供你查看模型、链、工具和耗时。

```text
你的 LangChain Agent
  -> 运行事件
  -> LangSmith trace
  -> 调试、数据集、线上评估
```

第 40 章的本地日志是你自己定义的最小记录；LangSmith 是对 LangChain 生态更完整的可视化追踪。

## 官方配置：先直接声明依赖

虽然 `langsmith` 可能作为 LangChain 的间接依赖出现在当前虚拟环境，**当你的代码或教学明确使用它时，仍应直接声明它**：

```bash
poetry add langsmith
```

然后在 `.env` 写入，绝不提交真实密钥：

```dotenv
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_your_key_here
LANGSMITH_PROJECT=study-python-dev
```

[LangSmith Observability Quickstart](https://docs.langchain.com/langsmith/observability-quickstart) 说明这些环境变量会开启追踪；项目名用于把学习环境和以后生产环境分开。

## 为什么现有 Agent 可以被追踪

你的 `create_agent(...)`、chain 的 `.invoke()` / `.ainvoke()` 已经有清楚的调用层级。开启 tracing 后，LangSmith 会在这些层级周围自动产生记录：

```text
agent.invoke
  -> model
  -> tool call
  -> tool result
  -> model final answer
```

因此本章的第一步不是再包装一个 `Agent`，而是只开配置后运行已有示例。更细的自定义函数可用 `@traceable` 标记：

```python
from langsmith import traceable


@traceable(name="rag-format-context")
def format_context(documents: list[str]) -> str:
    return "\n\n".join(documents)
```

`@traceable` 是装饰器：调用 `format_context()` 时保留原有返回值，同时多写一条可关联的 trace 记录。它适合关键业务步骤，不适合给每个微小字符串操作都加。

## 本章的运行顺序

1. 注册 LangSmith，创建 API Key。
2. 只在本机 `.env` 配置上述三个变量。
3. 启动一个已经能工作的 LangChain / Agent 示例。
4. 在项目页检查是否出现一次 trace。
5. 确认 trace 中没有不应上传的密钥、完整敏感对话或原始文件内容。

官方的 [LangChain tracing 指南](https://docs.langchain.com/langsmith/trace-with-langchain) 覆盖了链和 Agent 的自动追踪方式；你遇到版本差异时以它为准。

## LangSmith 与 Langfuse 的边界

两者都能做 LLM observability：

| 选择 | 当前适合的原因 |
| --- | --- |
| LangSmith | 你项目已经学习 LangChain / LangGraph，自动 tracing 路径最短 |
| Langfuse | 是另一个可选平台；以后若要比较多框架接入或自托管部署，再按当时的官方文档核对支持情况 |

现在只选 LangSmith 做实践，避免为同一条调用同时接两套平台而看不清数据来源。

## 只需认识：OpenTelemetry 与 OpenInference

本章实际操作仍然只用 LangSmith。下面两个名字是为了让你以后看到它们时知道各自负责什么；**不需要安装、配置或背 API**。

| 名称 | 它是什么 | 它不是什么 |
| --- | --- | --- |
| OpenTelemetry（OTel） | 与具体厂商无关的一套观测工具与标准，用来生成、收集和导出 traces、metrics、logs 等遥测数据 | 不是观测平台本身，不负责存储数据或提供可视化页面 |
| OpenInference | 面向 AI 应用的语义约定与 instrumentation（埋点工具），约定如何描述模型调用、检索、工具调用等 AI 步骤；建立在 OpenTelemetry 之上 | 不是 OpenTelemetry 的替代品，也不是必须绑定 Arize/Phoenix 才能使用 |

可以用这条关系辨认它们的分工：

```text
应用产生 trace / span
  -> OpenTelemetry 负责通用的采集与导出机制
  -> OpenInference 可补充 AI 步骤的字段约定
  -> 观测后端负责接收、保存和展示
```

OpenTelemetry 也在维护自己的 GenAI 语义约定，因此 OpenInference 不是唯一的 AI 字段规范。当前只要记住：**OTel 是通用观测底座；OpenInference 是一种 AI 领域的约定与埋点工具；LangSmith 是本章选用的观测平台。**不同库和平台对标准的支持会变化，真正接入前应核对对应版本的官方文档。[OpenTelemetry 概览](https://opentelemetry.io/docs/what-is-opentelemetry/) · [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/) · [OpenTelemetry GenAI 约定](https://github.com/open-telemetry/semantic-conventions-genai) · [OpenInference 说明](https://arize.com/glossary/openinference/)

### FastAPI 版本边界

本项目当前固定使用 FastAPI `0.128.8`。FastAPI 从 `0.142.0` 开始提供原生 OpenTelemetry 支持；`0.143.0` 又把自动配置改为显式启用。**本章并不依赖 FastAPI 自动配置**：这里只实践 LangSmith tracing，并认识 OTel 的职责。将来升级到包含这项能力的版本时，再按当时的官方发布说明配置；不要把新版本的环境变量直接套到当前锁定版本上。[FastAPI 官方发布说明](https://fastapi.tiangolo.com/release-notes/)

## 数据边界和抽样

测试数据、密钥和真实用户内容都要先过边界判断。线上请求很多时，再参考官方的 [trace sampling](https://docs.langchain.com/langsmith/sample-traces) 设置抽样率；不要一开始就把所有生产内容无选择上传。

## 三遍练习

1. [追踪] `LANGSMITH_PROJECT` 是模型名、项目分组还是 API 地址？
2. [改] 把学习项目名设为 `study-python-dev`，运行现有 Agent，一次 trace 中找出模型调用和工具调用。
3. [独立做] 列出你不会发送到平台的三类字段，并说明原因。

## 常见坑

- 只装包，不配置 `LANGSMITH_TRACING=true` 和 API Key。
- 将生产和学习 trace 混到同一个项目中。
- 把观测平台当成评估平台的替代品；它们会配合，不会互相取代。
- 复制旧版社区 API；LangSmith SDK 和环境变量以当前官方文档为准。

## 课后压缩

```text
LangSmith = 把已有 LangChain 调用的运行过程组织成 trace。
先明确依赖与 .env，再运行已有链路；先处理数据边界，再考虑全量采集。
```
