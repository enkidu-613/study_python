---
name: "tech-search-sources"
description: "技术搜索来源偏好设定。当用户需要互联网搜索技术问题时，优先从 GitHub、Stack Overflow、博客园(cnblogs)、掘金(juejin)、V2EX、思否、Medium、Hacker News、GeeksforGeeks、linuxdo 获取参考信息。Invoke when user asks for web search on technical topics or wants Chinese-friendly dev community sources."
---

# 技术搜索来源偏好

在回答技术问题时，如果需要联网搜索，应优先从以下来源获取参考信息。

## 首选来源（按优先级排序）

| 优先级 | 来源 | 域名 | 适用场景 |
|--------|------|------|----------|
| 🥇 | **GitHub** | `github.com` | 开源项目、issue 讨论、PR 解决方案、官方文档 |
| 🥈 | **Stack Overflow** | `stackoverflow.com` | 具体报错、编程问题、最佳实践 |
| 🥉 | **掘金** | `juejin.cn` | 中文技术教程、最佳实践、架构设计 |
| 4 | **博客园** | `cnblogs.com` | 中文深度技术文章、踩坑记录 |
| 5 | **V2EX** | `v2ex.com` | 开发者社区讨论、工具推荐、技术选型 |
| 6 | **思否** | `segmentfault.com` | 中文问答、前端/后端问题、技术面试 |
| 7 | **Medium** | `medium.com` | 英文深度技术文章、架构设计、趋势分析 |
| 8 | **Hacker News** | `news.ycombinator.com` | 技术新闻、创业讨论、前沿技术趋势 |
| 9 | **GeeksforGeeks** | `geeksforgeeks.org` | 算法、数据结构、计算机基础、面试题 |
| 10 | **linuxdo** | `linux.do` | Linux/开源社区讨论、技术分享、工具推荐 |

## 搜索策略

### 1. 搜索时追加站点限定
在进行 WebSearch 时，若问题属于特定领域，应在查询中追加站点限定词：

| 问题类型 | 追加站点限定 |
|----------|-------------|
| 开源项目 / bug / API 用法 | `site:github.com` |
| 报错排查 / 编程语法 | `site:stackoverflow.com` |
| 中文教程 / 架构方案 | `site:juejin.cn` 或 `site:cnblogs.com` |
| 工具推荐 / 开发者讨论 | `site:v2ex.com` 或 `site:linux.do` |
| 中文问答 / 面试相关 | `site:segmentfault.com` |
| 英文深度文章 / 趋势 | `site:medium.com` 或 `site:news.ycombinator.com` |
| 算法 / 数据结构 / 基础 | `site:geeksforgeeks.org` |

### 2. 多源对比
同一问题应尝试从 2-3 个来源交叉验证：

| 目标 | 推荐组合 |
|------|----------|
| 英文精确方案 | GitHub + Stack Overflow + Medium |
| 中文实践方案 | 掘金 + 博客园 + 思否 |
| 社区口碑 / 趋势 | V2EX + Hacker News + linuxdo |
| 算法 / 基础 | GeeksforGeeks + Stack Overflow |

### 3. 结果优先级
搜索返回结果后，优先点开来自以上 10 个域名的链接进行深度阅读（WebFetch），再使用其他来源。

## 示例

**用户问："LangChain ChatOpenAI 怎么传 extra_body"**

搜索顺序：
```
1. site:github.com LangChain ChatOpenAI extra_body
2. site:stackoverflow.com LangChain extra_body model_kwargs
3. site:juejin.cn LangChain 自定义参数
4. site:segmentfault.com LangChain extra_body
```
