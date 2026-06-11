---
name: chapter-review-quizzer
description: Conducts chapter review quizzes based on learning history and mistake records. Invoke when user asks to be tested, review mistakes, or check chapter mastery.
---
# 章节复习检测器

## 功能概述

根据学习历史、对话记录和错题本，自动生成检测试卷，评估用户对当前章节知识点的掌握程度。

## 🆕 试卷模式（推荐）

**流程**：生成试卷文件 → 用户在答题区填写 → 用户说"答完了" → AI 批改。

### 试卷生成

1. 确定当前章节（从 `learning_plan.json` 的 `current_stage_id`）
2. 读取相关对话记录和学习文档，提取核心知识点
3. 读取 `md/错题本.md`，找出历史薄弱点
4. 生成试卷文件 `md/试卷_<章节名>.md`，分三轮

### 试卷文件格式

```markdown
# 试卷：<章节名>

> 生成时间：YYYY-MM-DD | 章节：<stage_id>
> 三轮共 N 题，请在各题答题区填写答案。

---

## 第一轮：基础概念（5题）

### 题1：<题目内容>

**答题区**（在 ``` 内填写）：
```text
（在此填写你的答案）
```

### 题2：<题目内容>

**答题区**：
```text

```
...
```

**规则**：
- 必答题使用 ```` ```text ````，代码题使用 ```` ```python ```` 等对应语言
- 用户直接在每题的代码块内填写答案
- 选择题填选项字母，填空题直接写，代码题写完整代码

### 批改流程

1. 用户说"答完了"或类似信号后，AI 读取试卷文件 `md/试卷_<章节名>.md`
2. 逐题批改：读取每个答题区的用户答案 → 对比正确答案 → 标记 ✅/⚠️/❌
3. 在原试卷文件末尾追加批改结果：

```markdown
---

## 📝 批改结果（YYYY-MM-DD）

| 题号 | 结果 | 得分 | 点评 |
|------|:----:|------|------|
| 1 | ✅ | 1/1 | ... |
| 2 | ⚠️ | 0.5/1 | 核心对但漏了X |
| 3 | ❌ | 0/1 | ... |

**总分**: X / N（X%）
**评定**: 🟢通过 / 🟡补漏 / 🔴回炉

### ⚠️ 错题分析
[每道错题简要分析，记录到错题本]
```

4. 将错题同步写入 `md/错题本.md`
5. 按评定决定是否推进阶段

### 三轮结构

| 轮次 | 题数 | 题型 |
|------|------|------|
| 第一轮：基础概念 | 5 | 2核心概念 + 2流程理解 + 1易混淆点 |
| 第二轮：细节深挖 | 5 | 2错题变种 + 2边界情况 + 1综合应用 |
| 第三轮：场景应用 | 2-3 | 代码补全 / 报错诊断 / 设计决策 |

## 评分标准

| 得分 | 状态 | 建议 |
|------|------|------|
| 90-100% | 🟢 通过 | 标记阶段完成，进入下一章 |
| 70-89% | 🟡 补漏 | 记录错题，3天后重做 |
| <70% | 🔴 回炉 | 重新学习本章文档 |

## 错题记录格式

写入 `md/错题本.md`：

```markdown
#### ❌ 错题N：[简短描述]

**题目**: [题目内容]
**我的答案**: [用户答案]
**正确答案**: [正确答案]
**错误原因**: [一句话]
**掌握度**: ⭐⭐ → 需复习
**一句话总结**: [记忆口诀]
```

半对题用 `⚠️` 标记。

## 数据文件位置

```
.trae/memory/
├── learning_plan.json              # 学习计划，获取当前阶段
├── learning_history_index.json     # 历史索引，获取相关对话
├── conversations/                  # 对话内容，提取知识点
│   └── YYYY-MM-DD.md
├── learning_notes.md
└── code_patterns.md

md/错题本.md                         # 错题记录，确定薄弱点
md/试卷_*.md                         # 生成的试卷文件
md/                                  # 学习文档 00_* ~ 15_*
```

## 操作步骤（试卷模式）

1. 读取学习计划，确认当前阶段
2. 读取历史索引和相关对话文件，提取知识点
3. 读取 `md/错题本.md`，了解历史薄弱点
4. 生成试卷 `md/试卷_<章节名>.md`，按三轮结构出题
5. 告知用户试卷位置，等待用户答完
6. 用户答完后，读取试卷逐题批改，在原文件末尾追加批改结果
7. 错题写入 `md/错题本.md`
8. 根据评定决定是否更新学习计划阶段状态

## 跨框架同步规范

当本技能需要修改或同步 Reasonix 框架的文件时，必须严格遵守 Reasonix 的地址规范：

| 操作目标 | 必须使用路径 |
|----------|-------------|
| Reasonix 历史索引 | `.reasonix/memory/learning_history_index.json` |
| Reasonix 学习计划 | `.reasonix/memory/learning_plan.json` |
| Reasonix 对话记录 | `.reasonix/memory/conversations/YYYY-MM-DD.md` |
| Reasonix 学习笔记 | `.reasonix/memory/learning_notes.md` |
| Reasonix 代码模式 | `.reasonix/memory/code_patterns.md` |

**原则**：操作哪套框架的文件，就使用哪套框架的路径前缀。禁止在修改 Reasonix 文件时使用 `.trae/` 路径，反之亦然。

## 学习计划同步逐条对比规范

当同步 `.trae/memory/learning_plan.json` 与 `.reasonix/memory/learning_plan.json` 时，**禁止使用全局字符串替换**。必须：

1. **逐 stage 对比**：打开两边文件，按 `id` 字段逐个 stage 核对
2. **关键字段全覆盖**：除了 `status` 和 `current_stage_id`，必须检查 `documents`、`dependencies`、`completed_at` 等字段
3. **以最新版本为准**：以 `updated_at` 较新的文件为基准，将差异逐条应用到另一份文件
4. **验证**：同步后，用 `grep -n "documents"` 对比两边的行号和内容，确保完全一致

**反例**：全局替换 `"documents": []` → `"documents": ["xxx.md"]` 会误改其他 stage 的 documents 字段。
**正例**：定位到目标 stage 的完整 JSON 块，精确替换该块内的 documents 字段。
