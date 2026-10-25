---
name: review-scheduler
description: Use when the user says "复习", mentions forgetting something, when a chapter quiz is about to start or finishes, or when archiving a learning conversation. FSRS-based spaced repetition scheduler for learning topics.
---

# review-scheduler

## Description

基于 FSRS 间隔重复算法的复习调度技能。追踪学习主题的记忆状态(难度 D / 稳定性 S),在遗忘临界点前安排复习。信号来源:章节测验对错(主信号)、学习对话中的遗忘/回忆表现(辅助信号)。

## When to Use

- 用户说"复习"/"今天该复习什么" → 先跑 `due` 拉今日到期项
- 用户说"我忘了 X"/"X 是什么来着" → 该主题是遗忘信号,按评分表 `rate again`
- 章节测验(chapter-review-quizzer)出题前 → 跑 `due`,到期主题优先出题
- 章节测验结束 → 按对错 `rate`(答错 again,勉强过 hard,正常过 good,全对 easy)
- 学习对话归档(history-archiver)时 → 按下表把对话信号转为评分
- 用户学了一个新主题并表示理解 → `add` 入队

## How to Use

### 1. 查今日到期(复习入口)

```bash
poetry run python -m app.tools.review_scheduler due
poetry run python -m app.tools.review_scheduler due --json   # 程序处理用
```

输出按逾期时间排序,`有复习题` 标记的主题可直接用其 `review_material.prompt`(旧错题原文)出题;无标记的用 `source` 路径 + personal-kb 检索原文出题。

### 2. 记录复习评分(核心)

```bash
poetry run python -m app.tools.review_scheduler rate --topic "范数与余弦相似度" --rating good
poetry run python -m app.tools.review_scheduler rate --topic "SIMD" --rating again --note "刚学,还不稳"
```

**评分映射表(AI 判断的唯一依据)**:

| 信号 | 评分 | 说明 |
|------|------|------|
| quizzer 答错 / 用户明说"我忘了"/"X是什么来着" | `again` | 提取失败,间隔重置 |
| 补考勉强通过 / 重讲后才表示理解 | `hard` | 勉强提取 |
| 主动在新语境正确引用旧概念 / 测验正常通过 | `good` | 提取成功 |
| 能反过来给 AI 讲清楚 / 测验一次全对 | `easy` | 提取轻松 |

注意区分:用户问新概念(从未学过)→ 用 `add` 建卡,不是 rate;用户对已学概念的深化追问(如"为什么归一化后范数是 1")→ 说明记得住,是 `good` 信号。

### 3. 新主题入队

```bash
poetry run python -m app.tools.review_scheduler add --topic "主题名" --source "md/相对路径.md" --tag 标签
```

主题名建议与对话归档的 topics 粒度一致(概念级,如"threading.Lock",不是整章)。

### 4. 队列管理

```bash
poetry run python -m app.tools.review_scheduler list          # 全部主题及到期时间
poetry run python -m app.tools.review_scheduler stats         # 统计
poetry run python -m app.tools.review_scheduler migrate       # 旧阶梯版错题队列导入(已执行过)
```

## 数据文件

- **`.trae/memory/fsrs_queue.json`** — FSRS 队列(D/S 状态、history、review_material),由脚本管理,不要手改
- **`.trae/memory/review_queue.json`** — 旧阶梯版错题队列,是 chapter-review-quizzer 的契约文件,schema 被测试锁定,**只读勿改**

## 与其他 skill 的协作

- **chapter-review-quizzer**:出题前先 `due` 拉到期主题优先出题;测验结束按对错 `rate` 回流
- **history-archiver**:归档时检测对话中的遗忘/回忆信号,转成 `rate`
- **personal-kb**:到期主题无现成复习题时,用 `kb_search "主题关键词"` 检索原文出题

## Response Guidelines

1. `due` 有到期项时,主动告知用户"今日有 N 个主题到期",列出前几个
2. 复习完一个主题必须 `rate`,否则调度会失准
3. 评分宁低勿高:犹豫 between good/easy 时选 good,between hard/again 时选 hard
4. 不要替用户编造评分——只在有明确信号(答错、明说忘了、测验通过)时才 rate
5. `rate` 后把脚本输出的"下次到期"时间告诉用户,让用户知道复习节奏
