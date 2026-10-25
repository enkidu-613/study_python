# 02. Agent 上下文上限与多 Agent Memory 冲突

> 定位：这是 AI 应用开发的工程基础，回答两个高频问题——"单个 Agent 能记住多少东西？"和"很多 Agent 的记忆打架了怎么办？"。不是研究论文，是给你做多 Agent 系统时的取舍手册。

## 一句话心智模型

```text
上下文上限：窗口是广告值，只能用六七成
    ↓
多个 Agent 一起干活 → 记忆会冲突
    ↓
冲突解法：先结构化 → 再粗筛 → 最后精筛
    ↓
80% 的冲突用 SQL 就解决了，不需要 AI
```

## 学习顺序

1. 先理解"上下文窗口"到底是什么、广告值和实际值的差距。
2. 再理解为什么窗口大不等于记得牢（Lost in the Middle）。
3. 再看多 Agent 记忆冲突的三种典型场景。
4. 最后掌握"结构化 → 粗筛 → 精筛"的工程顺序。

---

## 1. Agent 上下文（Memory）上限：2026 年现状

### 1.1 广告值 vs 实际值

| 档位 | 模型示例 | 上下文窗口（广告值） | 实际可靠值 |
| --- | --- | --- | --- |
| 前沿主流 | GPT-5.6 / Claude 5 / Gemini 3.x / Qwen3.8 | 1M token | ~600~700K |
| 性价比档 | Claude Haiku / DeepSeek V3 | 200K / 128K | ~130K / ~85K |

**关键认知：广告值打 6~7 折才是能放心用的量。** 文档说 1M，实际塞到 70 万以上质量就开始滑坡。

### 1.2 为什么"窗口大"不等于"记得牢"

三个原因：

1. **Context Rot（上下文腐烂）**：塞得越多，模型对早期内容的记忆越模糊。超过窗口 65% 左右，质量陡降。
2. **Lost in the Middle（中间迷失）**：模型对**开头和结尾**的内容记得最牢（85-95% 召回），**中间段**最差（76-82%）。重要信息要放开头或结尾，别沉在中间。
3. **成本爆炸**：窗口翻一倍，算力大约 ×4（注意力机制是二次方增长）。1M 窗口不是白给的，是按 4 倍钱买的。

### 1.3 生活类比

> 上下文窗口 = 桌子的面积。
> 广告值 = 桌子标称能摆 100 件东西。
> 实际值 = 摆到 70 件就开始乱，摆到中间的东西你还容易找不到。
> 所以聪明人把重要的放桌边（开头结尾），中间只放"丢了也不心疼"的。

---

## 2. 多 Agent Memory 冲突：问题本质

### 2.1 三种典型冲突

| 场景 | 例子 | 严重度 |
| --- | --- | --- |
| **同 key 多 value** | 两个 Agent 都写了 `project_status`，一个说"完成"一个说"进行中" | 高 |
| **多 agent 抢写** | 3 个 Agent 同时更新同一个配置字段 | 高 |
| **版本过期** | Agent A 基于旧版本改数据，Agent B 已经更新了 | 中 |

### 2.2 先问一个更根本的问题

> **你的 memory 有结构化吗（schema）？**

如果没有 schema——每条记忆只是自由文本——那么"冲突"这个概念本身就**无法定义**。你怎么判断两段话在描述同一个东西？没法判。所以：

**没有结构化的记忆，谈不上冲突检测。** 这是整件事的第一块基石。

---

## 3. 正确工程顺序：结构化 → 粗筛 → 精筛

### 3.1 ① 结构化（成本：0）

给每条记忆定一个固定形状：

```python
from pydantic import BaseModel, Field
from datetime import datetime

class Memory(BaseModel):
    agent_id: str                      # 谁写的
    key: str                           # 记忆的主题（如 "project_status"）
    value: str                         # 值
    tags: list[str] = Field(default_factory=list)  # 分类
    timestamp: datetime                # 什么时候写的
    version: int = 1                   # 版本号，用于并发控制
```

**有了 schema，冲突才变得可计算**——同 key、多 agent、旧版本，这些都能用字段精确匹配。

### 3.2 ② 粗筛（成本：极低，用 SQL）

把记忆放进关系型数据库（PostgreSQL 单机可扛 10 万次写入/秒），用 SQL 找冲突：

```sql
-- 场景 1：同一个 key 被多个 agent 写过（同 key 多 value）
SELECT key, COUNT(DISTINCT agent_id) AS agent_count
FROM memories
GROUP BY key
HAVING COUNT(DISTINCT agent_id) > 1;

-- 场景 2：同一个 key 存在多个不同 value（抢写）
SELECT key, COUNT(DISTINCT value) AS value_count
FROM memories
GROUP BY key
HAVING COUNT(DISTINCT value) > 1;

-- 场景 3：版本过期（同一 agent 写了新版本，还有旧版本残留）
SELECT key, agent_id, version, MAX(version) OVER (PARTITION BY key, agent_id) AS latest
FROM memories
WHERE version < MAX(version) OVER (PARTITION BY key, agent_id);
```

**关键认知：前 80% 的冲突用 SQL 就能解决，不需要 LLM。**

### 3.3 ③ 精筛（成本：中，用 embedding / LLM）

SQL 搞不定的"语义级冲突"（两个 value 字面不同但意思相近），才轮到 AI：

| 相似度 | 处理 |
| --- | --- |
| > 0.95 | 去重（同一件事的两种写法） |
| 0.7 ~ 0.95 | 标记为"关联"，合并展示 |
| < 0.7 | 交给 LLM 仲裁（谁对 / 谁新 / 怎么合并） |

### 3.4 完整链路图

```text
1000 个 agent 写入
    ↓ ① 结构化（schema 字段齐全）
存入 PostgreSQL
    ↓ ② 粗筛（SQL）
同 key 多 value / 多 agent 抢写 / 版本过期   ← 80% 在这里解决
    ↓ ③ 精筛（embedding 相似度 + LLM 仲裁）
语义级冲突                             ← 剩下 20%
```

---

## 4. 工程心态：别被"规模"吓住

讨论中有人提醒得对：**"你有点太极端了"**。

- 1000 个 agent 听起来吓人，但**"规模焦虑"是次要问题**；
- **"没结构化"才是根本问题**——没 schema，1 个 agent 的冲突你都说不清，更别说 1000 个。
- 正确顺序永远是：**先让数据可计算（schema）→ 用便宜的算（SQL）→ 最后才用贵的算（AI）**。

> 类比：一千个人在同一个白板上写字，肯定打架。但解决办法不是发明"高级防打架算法"，而是先给每人发一张**有编号、有姓名、有时间的便签纸**（结构化）——然后再看谁和谁写了同一个编号（SQL 粗筛），最后才需要人去仲裁语义（LLM 精筛）。

---

## 5. 理解检查

1. 1M 上下文窗口，实际能放心用多少？
2. 为什么重要信息要放上下文开头或结尾？
3. 没有 schema 的记忆，为什么无法做冲突检测？
4. 1000 个 agent 的冲突，前 80% 用什么解决？
5. 粗筛和精筛的分界在哪里？

## 与现有文档的关系

- [01_文本进入模型_Token与Pooling](./01_文本进入模型_Token与Pooling.md)：理解单条文本怎么变成向量，这是精筛（embedding 相似度）的前置知识。
- [第 32 章 Hugging Face 生态](../32_HuggingFace生态.md)：学习 embedding 的实践基础，对应 3.3 节精筛的相似度计算。
