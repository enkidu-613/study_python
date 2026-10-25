# CS50 / CS50P 许可核查笔记

核查时间：2026-10-20
核查方式：直接抓取官方页面正文（`curl`，因本机 Clash fake-IP 导致 `198.18.x.x`，
`web_fetch` 的公网 IP 校验会误拒，见文末「取数踩坑」）

## 一、结论

| 项目 | 结论 |
| --- | --- |
| 许可协议 | **CC BY-NC-SA 4.0**（CS50x 与 CS50P 同款） |
| 翻译是否被允许 | **允许**。CC 的 `Adapt` 权利明确包含 remix / transform / build upon，翻译属于改编 |
| 是否需要单独申请授权 | **不需要**（只要遵守署名、非商业、相同方式共享三条） |
| 是否可商用 | **不可以** |
| 改编后是否要开源同协议 | **要**，衍生部分必须以 CC BY-NC-SA 4.0 发布 |
| 作业答案能否公开 | **不建议**，违反 CS50 学术诚信条款（见第三节） |

官方原话（引用自课程 license 页）：

> This course is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
> International (CC BY-NC-SA 4.0) license.

> **Adapt** — remix, transform, and build upon the material

并且课程首页明确鼓励教学改编：

> If you are a teacher, you are welcome to adopt or adapt these materials for your own course,
> per the license.

## 二、CC BY-NC-SA 4.0 四条约束的落地要求

1. **Attribution（署名）**
   - 注明来源：CS50 / Harvard University，附课程链接
   - 附许可协议链接：<https://creativecommons.org/licenses/by-nc-sa/4.0/>
   - **明确标注"已做修改"**（例如"本文为 CS50P 第 4 讲的中文改编"）
   - 不得暗示 CS50 为本项目背书

2. **NonCommercial（非商业）**
   - 本项目无付费、无广告、无捐赠入口 → 合规
   - 一旦加入任何变现（付费专栏、赞助、付费课程打包）→ 该部分必须撤下

3. **ShareAlike（相同方式共享）**
   - 改编章节必须以 CC BY-NC-SA 4.0 发布，**不能**改成 MIT / 私有协议
   - ⚠️ 实务要点：把 CS50 改编内容混进现有原创课程，会牵连该部分协议。
     → 建议**独立目录 + 独立 LICENSE/NOTICE**，避免 SA 扩散到全仓库
   - 纯聚合（各自独立文件、互不改编）可在仓库内保留不同协议

4. **No additional restrictions**
   - 不能加 DRM、不能加"禁止转载"之类更严格的条款

## 三、学术诚信条款（与版权是两件事）

版权允许你改编作业题，但 CS50 的 honesty policy 另外约束"公开答案"行为。
<https://cs50.harvard.edu/x/2026/honesty/> 的 **Not Reasonable** 列表包含：

> Providing or making available solutions to assessments to anyone, whether a past, present...

**实践建议：**

- 讲义 / 课堂讲解 / 示例代码 → 可翻译、可改编、可公开（带署名）
- 作业题原文 → 可翻译，但别配"标准答案 + 完整可运行代码"
- 自己的作业解答 → 放私有仓库，或只保留思路与伪代码
- 练习 → **自出题**，只借鉴难度与题型

## 四、对本项目的落地口径

推荐路线（而非"逐段翻译"）：

1. 借用 CS50P 的**主题顺序与难度曲线**（10 周：Functions/Variables → Conditionals →
   Loops → Exceptions → Libraries → Unit Tests → File I/O → Regular Expressions →
   OOP → Et Cetera）
2. 正文、例子、练习**自己写**
3. 若确实要直译某几讲：单独放 `md/cs50p-中文版/`，目录内放
   `LICENSE`（CC BY-NC-SA 4.0 全文）+ `NOTICE`（署名与修改声明）
4. 全项目 README 里加一行来源说明，避免与原创章节混淆

这样既合规，也不会让 SA 条款覆盖掉你原来的原创内容。

## 五、取数踩坑（复现用）

症状：`web_fetch https://cs50.harvard.edu/...` 报
`URL hostname resolves to a non-public IP address`。

根因：本机 Clash TUN + fake-IP 模式，`dig cs50.harvard.edu` 返回 `198.18.1.117`，
即使 `dig @223.5.5.5` 也一样（TUN 劫持了 DNS）。而 TUN 在路由层会把该假 IP 正确
送回代理还原真实域名，实际连通没问题。

绕法：直接用 `curl`，不让工具做"解析后校验 IP"这一步。

```bash
curl -sS -L --max-time 25 -o page.html \
  -w "HTTP %{http_code} | size %{size_download}\n" \
  https://cs50.harvard.edu/python/license/
```

正文提取：去掉 `<script|style|nav|header|footer>`，取 `<main>` 内的纯文本。

## 六、原文链接

- CS50x License：<https://cs50.harvard.edu/x/license/>
- CS50P License：<https://cs50.harvard.edu/python/license/>
- CS50P 课程首页：<https://cs50.harvard.edu/python/>
- CS50P 周次索引：<https://cs50.harvard.edu/python/weeks/>
- CS50 学术诚信：<https://cs50.harvard.edu/x/2026/honesty/>
- CC BY-NC-SA 4.0 全文：<https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode>
