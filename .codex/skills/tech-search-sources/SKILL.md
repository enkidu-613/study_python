---
name: tech-search-sources
description: 技术搜索与可信教学资源偏好。搜索技术问题、查 AI Engineer 学习路线或寻找中文友好开发资料时使用。
---

# 技术搜索来源偏好

回答技术问题时，联网搜索优先从以下来源获取信息。

## 来源权威与版本冲突规则

权威等级与搜索入口分开处理：社区列表用于发现资料，不代表社区资料可以覆盖官方结论。

1. 先查目标技术的最新官方文档、官方 API 参考和官方版本说明，再查社区资料。
2. 社区文章与官方文档冲突时，以最新官方文档为准；社区文章只作为补充示例、经验和中文解释，不能覆盖官方 API 行为。
3. 如果项目锁定了旧版本，优先使用该旧版本对应的官方文档，并明确说明它与最新官方文档的差异；不要把最新 API 直接套到旧依赖上。
4. 如果官方文档与实际运行结果冲突，记录产品版本、依赖版本、文档更新时间和错误现象，再检查官方 changelog、release 或 issue；不要静默混合两套结论。
5. 教程和代码示例应标注版本敏感点；社区来源过时或无法确认版本时，明确标记为“仅供参考”。

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
.codex/skills/tech-search-sources/references/roadmap-ai-engineer-articles.md
```

该文件收录 roadmap.sh AI Engineer 节点中的 `@article@` 资源。用于快速找学习文章；涉及官方 API、库版本、价格、模型能力或安全规范时仍需实时核对官方来源。
