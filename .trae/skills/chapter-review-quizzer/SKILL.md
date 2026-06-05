---
name: chapter-review-quizzer
description: Conducts chapter review quizzes based on learning history and mistake records. Invoke when user asks to be tested, review mistakes, or check chapter mastery.
---

# 章节复习检测器

## 功能概述

根据学习历史、对话记录和错题本，自动生成三轮检测题目，评估用户对当前章节知识点的掌握程度。

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
md/                                  # 学习文档 00_* ~ 15_*
```

## 检测流程

### 第一轮：基础概念（5题）
- 2题核心概念（是什么、为什么）
- 2题流程理解（怎么做、顺序是什么）
- 1题易混淆点（A和B的区别）

**规则**：每答一题立即告诉对错，不要等全部答完。

### 第二轮：细节深挖（5题）
- 2题第一轮错题的变种（换角度考同一知识点）
- 2题边界情况（失败场景、异常处理）
- 1题综合应用（串联多个知识点）

### 第三轮：场景应用（2-3题）
- 代码补全
- 报错诊断
- 设计决策

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

## 操作步骤

1. 读取 `.trae/memory/learning_plan.json`，确认当前阶段
2. 读取 `.trae/memory/learning_history_index.json` 和相关对话文件，提取知识点
3. 读取 `md/错题本.md`，了解历史薄弱点
4. 按三轮流程出题，每题即时反馈
5. 每轮结束后记录错题到 `md/错题本.md`
6. 检测结束后生成总结报告
7. 更新 `.trae/memory/learning_plan.json` 阶段状态（如通过）

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
