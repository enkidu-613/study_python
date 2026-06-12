---
name: firecrawl-karpathy-research
description: Firecrawl 网页研究与 Karpathy 风格 AI 工程准则。用于 scrape/crawl/map/search/extract 网页、文档、API、产品或技术资料，并输出来源可靠、步骤小、可验证、可实现的上下文。
---

# Firecrawl Karpathy Research

把网页、文档、API 或产品资料整理成工程可用上下文。优先官方/一手来源，保留 URL，并区分事实、推断和建议。

## 工作流

1. 明确研究目标：URL、域名、文档区块、产品、API 或具体问题。
2. 选择最小 Firecrawl 操作：
   - `scrape`：已知单页。
   - `crawl`：有边界的站点区块或文档目录。
   - `map`：先发现 URL，再决定 crawl 范围。
   - `search`：不知道目标页面在哪里。
   - `extract`：需要结构化字段。
3. 先设边界：允许域名、最大页数、深度、格式、include/exclude 路径。
4. 先读抓取内容再总结；标题、snippet、搜索结果只能当线索。
5. 关键结论尽量用官方/一手来源交叉验证。
6. 输出时保留来源、置信度、缺口和下一步。

## Firecrawl 规则

- 只使用环境中已经配置好的 API key、MCP 或工具；不要编造凭证。
- 尊重 robots、付费墙、登录墙、隐私数据和站点条款。
- 文档/文章优先 markdown；需要结构、selector 或元数据时再取 HTML。
- 技术研究要记录版本号、日期、弃用说明和迁移说明。
- 大站点先 `map` 或小范围 crawl，检查后再扩大。
- 临时失败时先缩小范围或简化格式重试一次。
- 保留原始 URL，方便用户审计证据链。

## Karpathy 风格准则

- 上下文就是产品：收集“下一步正确行动”所需的最小完整上下文。
- 保持短循环：读、改、跑、看，再重复。
- 优先简单、可检查、数据流清楚的实现，避免过早抽象。
- 让中间状态可见：日志、样例、小 fixture、截图或原始输出。
- 区分“来源说了什么”“我推断什么”“我建议什么”。
- 从研究进入实现时，先做最小可运行切片，再扩展。
- 把 prompt、检索 query、schema、示例当成需要版本化和测试的代码。

## 输出格式

研究回答：

- `Finding`：直接结论。
- `Sources`：URL + 每个来源贡献了什么。
- `Confidence`：high / medium / low，并说明原因。
- `Gaps`：缺失、过期、不可访问或假设。
- `Next step`：最小可执行下一步。

实现交接：

- 相关来源 URL。
- 必要 API、环境变量、限制。
- 最小可运行路径。
- 验证命令或人工检查。
- 优先测试的风险点。

## 起点

- Firecrawl docs: `https://docs.firecrawl.dev/`
- Firecrawl site: `https://www.firecrawl.dev/`
- Karpathy: `https://karpathy.ai/`

