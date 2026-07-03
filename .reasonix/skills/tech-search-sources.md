---
name: tech-search-sources
description: 技术搜索与可信教学资源偏好。搜索技术问题、查 AI Engineer 学习路线或寻找中文友好开发资料时使用。
---
# 技术搜索来源偏好

回答技术问题时，联网搜索优先从以下来源获取信息。

## 路线型可信教学资源

| 来源 | 域名 | 适用 |
|------|------|------|
| roadmap.sh AI Engineer | roadmap.sh/ai-engineer | AI Engineer 学习路线、章节顺序、查缺补漏 |

当用户询问 AI Engineer 学习路线、章节资源、后续学习顺序或与 roadmap.sh 对齐时：

1. 优先参考 <https://roadmap.sh/ai-engineer>。
2. 需要查看该路线下每个节点提到的免费文章资源时，读取 `references/roadmap-ai-engineer-articles.md`。
3. 如果用户要求“最新资源”，重新从 roadmap.sh 或其 GitHub 数据源核对，不只依赖本地快照。

本 skill 附带快照：

```text
.reasonix/skills/tech-search-sources/references/roadmap-ai-engineer-articles.md
```

该文件收录 roadmap.sh AI Engineer 节点中的 `@article@` 资源。用于快速找学习文章；涉及官方 API、库版本、价格、模型能力或安全规范时仍需实时核对官方来源。

## 首选来源

| 优先级 | 来源 | 域名 | 适用 |
|--------|------|------|------|
| 🥇 | GitHub | github.com | 开源、issue、PR |
| 🥈 | Stack Overflow | stackoverflow.com | 报错、编程问题 |
| 🥉 | 掘金 | juejin.cn | 中文教程、架构 |
| 4 | 博客园 | cnblogs.com | 中文深度文章 |
| 5 | V2EX | v2ex.com | 开发者讨论 |
| 6 | 思否 | segmentfault.com | 中文问答 |
| 7 | Medium | medium.com | 英文深度文章 |
| 8 | Hacker News | news.ycombinator.com | 技术趋势 |
| 9 | GeeksforGeeks | geeksforgeeks.org | 算法、基础 |
| 10 | linuxdo | linux.do | Linux/开源讨论 |

## 搜索策略

### 1. 站点限定
在 Reasonix 中使用 `web_search` 时追加 site: 限定：

| 问题类型 | 搜索示例 |
|----------|---------|
| API/bug | `web_search("LangChain extra_body site:github.com")` |
| 报错 | `web_search("KeyError site:stackoverflow.com")` |
| 中文教程 | `web_search("FastAPI 分层架构 site:juejin.cn")` |
| 工具推荐 | `web_search("最好的向量数据库 site:v2ex.com")` |
| 英文深度 | `web_search("RAG chunking strategy site:medium.com")` |
| 算法 | `web_search("binary tree traversal site:geeksforgeeks.org")` |

### 2. 多源交叉验证

| 目标 | 推荐组合 |
|------|----------|
| 英文方案 | GitHub + Stack Overflow + Medium |
| 中文方案 | 掘金 + 博客园 + 思否 |
| 社区口碑 | V2EX + Hacker News + linuxdo |
| 算法基础 | GeeksforGeeks + Stack Overflow |

### 3. 工作流
1. `web_search(query)` — 获取结果列表
2. 优先选择以上 10 个域名的结果
3. `web_fetch(url)` — 深度阅读最佳结果
4. 若中文信息不足，追加中文站点搜索

## 示例

用户问 "LangChain ChatDeepSeek 怎么传推理链参数"：
```
1. web_search("ChatDeepSeek reasoning_content extra_body site:github.com")
2. web_search("DeepSeek LangChain 推理链 site:juejin.cn")
3. web_fetch(<最相关链接>)
```
