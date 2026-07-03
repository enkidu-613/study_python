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

## 首选来源

| 优先级 | 来源 | 域名 | 适用 |
|--------|------|------|------|
| 🥇 | GitHub | github.com | 开源、issue、PR、官方文档 |
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

1. API、bug、框架源码优先 GitHub 和官方文档。
2. 报错优先 Stack Overflow，再看 GitHub issue。
3. 中文教程优先掘金、博客园、思否。
4. 技术选型和口碑优先 V2EX、Hacker News、linuxdo。
5. 同一技术结论尽量使用 2-3 个来源交叉验证。

## roadmap.sh AI Engineer 文章资源

本 skill 附带快照：

```text
.reasonix/skills/tech-search-sources/references/roadmap-ai-engineer-articles.md
```

该文件收录 roadmap.sh AI Engineer 节点中的 `@article@` 资源。用于快速找学习文章；涉及官方 API、库版本、价格、模型能力或安全规范时仍需实时核对官方来源。
