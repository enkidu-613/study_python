# 试卷：Alembic 数据库迁移_补考

- 日期：2026-06-19
- 章节：第 19 节 Alembic 数据库迁移
- 总分：10 分
- 通过线：8 分
- 答题方式：直接在每题“我的答案”下面作答
- 注意：本补考重点不是背完整命令，而是判断边界、概念和流程。命令大致方向正确即可。

---

## 1. migration 和 backup 的边界（2 分）

请用自己的话解释：

- migration 是什么；
- backup 是什么；
- 为什么不能把 Alembic migration 叫成“数据库备份”。

**我的答案：**

1. 是一系列历史迁移文件的称呼
2. 是指的是将当前状态完整备份
3. 因为 alembic 只是备份的数据库的表的历史结构

---

## 2. Alembic 命令和概念匹配（2 分）

下面几个词分别是什么类型？

- `stamp head`
- `migration`
- `revision`
- `upgrade`
- `alembic_version`

请用“指令 / 文件或一次迁移 / 版本号 / 执行动作 / 数据库版本记录表”这类词来说明。

**我的答案：**

1. 不执行sql 只是标记当前数据库是最新版本
2. 历史迁移文件的统称
3. 创建一个新的迁移文件
4. 将迁移文件更新到数据库
5. 记录数据库更新到那个迁移文件

---

## 3. `alembic_version` 和 `stamp head`（2 分）

已有数据库里已经有 `users`、`documents` 等表，现在你才接入 Alembic。

请说明：

1. `alembic_version` 表记录什么；
2. `stamp head` 做什么；
3. 为什么 `stamp head` 不等于执行建表迁移。

**我的答案：**

1. 当前数据库对应的迁移文件版本
2. 不执行sql，宣称数据库是最新的
3. 因为不执行sql

---

## 4. 空数据库能不能靠 migration 变成最新结构？（2 分）

请判断并解释：

一个空数据库执行：

```bash
poetry run alembic upgrade head
```

能不能马上变成当前项目的最新表结构？需要满足什么前提？如果初始 migration 里只有 `pass` 会怎样？

**我的答案：**
1. 可以
2. 必须是真空的数据库
3. 会是一个空的迁移


---

## 5. 结构和数据都要迁移时怎么选工具？（2 分）

请分别写出下面三种情况应该用什么：

1. 把整个数据库搬到新机器，结构和真实数据都要；
2. 给 `users` 表新增 `email` 字段；
3. 新增 `email` 字段后，要给少量旧用户补默认邮箱。

**我的答案：**

1. alembic 和 database
2. alembic
3. sql 或者orm上加default 使用alembic更新，如果数据支持的话

---

## 批改区

> 等用户答完后追加评分、错题、弱点和复习计划。

---

## 批改结果（2026-06-19）

### 总分

- 得分：7.2 / 10
- 通过线：8 / 10
- 结果：接近通过，但还差一个关键点：空数据库能否 upgrade 到最新结构的前提。

这次比初考进步明显。`stamp head`、`alembic_version`、`upgrade` 的作用已经基本稳定了。现在真正需要补的是两个边界：

1. migration 不是“备份表结构历史”，而是“结构变化脚本”。
2. 空库能不能靠 Alembic 变成最新结构，关键不在“空”，而在“迁移历史是否完整”。

### 逐题评分

| 题号 | 得分 | 批改 |
|---|---:|---|
| 1 | 1.2 / 2 | 你答对 backup 是完整状态备份，但 migration 仍说成“一系列历史迁移文件”和“备份数据库表历史结构”。更准确：一个 migration 是一次结构变化脚本；migrations 才是一系列历史。 |
| 2 | 1.6 / 2 | 大部分对。`stamp head`、`upgrade`、`alembic_version` 理解不错；`revision` 更准确是版本号，`alembic revision` 才是创建迁移文件的命令；`migration` 是一次迁移/迁移文件，不只是统称。 |
| 3 | 2 / 2 | 正确。`alembic_version` 记录当前数据库对应的 revision；`stamp head` 不执行 SQL，只标记当前数据库是最新。 |
| 4 | 1.1 / 2 | 方向对了一半。空数据库可以靠 `upgrade head` 变成最新结构，但前提不是“必须是真空数据库”，而是 migration 历史必须完整，初始 migration 里要有 `create_table`。如果初始 migration 只有 `pass`，空库执行后仍然没有表。 |
| 5 | 1.3 / 2 | 第 2 点正确。第 1 点完整搬家应优先使用数据库备份工具，不需要先 Alembic；第 3 点少量旧数据修正最好写在 Alembic migration 里的 `op.execute(...)`，不是只靠 ORM default。 |

### 当前已经掌握

- `stamp head` 是命令，不执行 SQL，只盖章。
- `alembic_version` 记录当前数据库到了哪个 revision。
- `upgrade` 是把迁移应用到数据库。
- 新增字段这类结构变化应该用 Alembic。

### 还需要补的 2 句

1. **migration 的准确边界**

```text
一个 migration = 一次结构变化脚本；
migrations = 一系列结构变化历史；
backup = 当前完整状态备份，包含真实数据。
```

2. **空库升级的准确前提**

```text
空库能不能 upgrade 到最新结构，不取决于它是不是空，而取决于迁移历史是否完整。
初始 migration 有 create_table，空库就能建出表；
初始 migration 只有 pass，空库 upgrade 后仍然是空。
```

### 最小补救

不需要整章重考。只需要再确认 2 个问题：

1. 为什么“空数据库”不是 `upgrade head` 成功建表的充分条件？
2. 为什么完整搬家优先用数据库备份，而不是先用 Alembic？
