# 试卷：Alembic 数据库迁移

- 日期：2026-06-19
- 章节：第 19 节 Alembic 数据库迁移
- 总分：20 分
- 通过线：16 分
- 答题方式：直接在每题“我的答案”下面作答
- 注意：本试卷不附答案。答完后让我批改，我会把评分、错题、弱点和复习计划追加到本文件。

---

## 一、核心概念题（每题 2 分，共 8 分）

### 1. Alembic 到底管什么？

请用一句话说明 Alembic 管的是“数据内容”还是“数据库结构”，并举一个 Alembic 应该处理的例子。

**我的答案：**

对数据库结构进行版本备份和迁移 比如在orm进行一个新增字段，alembic可以进行版本迁移文件的生成，通过upgrade对数据库进行更改

---

### 2. 为什么 `create_all()` 不适合长期替代 Alembic？

请说明 `create_all()` 适合什么阶段，以及长期保留它和 Alembic 同时管理结构会产生什么混乱。

**我的答案：**

因为 create_all 只适合初期阶段，因为那个时候只需要创建数据库就好了，有什么混乱我有点忘了，反正这个不适合数据库版本的管理

---

### 3. `target_metadata = Base.metadata` 是为了让 Alembic 看见什么？

请解释 `Base.metadata` 里大概包含哪些结构信息，以及如果 `target_metadata = None` 会发生什么。

**我的答案：**

包含的是orm模型的元数据，alembic无法读取orm设定的数据结构

---

### 4. Alembic、数据库备份、pip/Poetry 分别管什么？

请分别说明下面三类工具负责什么：

- Alembic
- 数据库备份工具，例如 SQLite `.backup` / PostgreSQL `pg_dump`
- pip / Poetry

**我的答案：**

1. alembic 是一个数据库表结构版本管理软件
2. 我通常使用navicat 或者 databsae和datagrip进行数据库数据的导出，防止数据丢失
3. pip/poetry 这些类似于node的npm 是依赖管理器

---

## 二、命令流程题（每题 2 分，共 6 分）

### 5. 初始化、生成迁移、执行迁移分别用什么命令？

本项目使用 Poetry。请写出：

1. 第一次初始化 Alembic 工作台的命令；
2. 模型变化后生成迁移草稿的命令；
3. 把迁移应用到数据库的命令。

**我的答案：**

有些忘了 我记得 初始化是 使用 init 迁移草稿是 revison -autogenerate 把迁移用到数据库的指令是 upgrade head

---

### 6. `revision` 和 `upgrade` 的区别是什么？

请说明：

- `poetry run alembic revision --autogenerate -m "..."`
- `poetry run alembic upgrade head`

分别在做什么。

**我的答案：**

第一个是生成备份迁移文件，第二个是将最新的备份迁移文件更新到数据库

---

### 7. `alembic_version` 表是干什么的？

请说明这个表记录什么，以及为什么已有数据库接入 Alembic 时可能需要 `stamp head`。

**我的答案：**

这个是记录表结构迁移文件的，后面那个忘记了

---

## 三、场景判断题（每题 2 分，共 4 分）

### 8. 为什么你的第一次 `--autogenerate` 可能生成空迁移？

场景：

项目之前运行过：

```python
Base.metadata.create_all(bind=engine)
```

数据库里已经有 `users`、`documents` 等表。现在你接好 `target_metadata = Base.metadata` 后执行：

```bash
poetry run alembic revision --autogenerate -m "init tables"
```

结果 `upgrade()` 里只有 `pass`。

请解释为什么。

**我的答案：**

可能是数据库在第一次迁移之前就已经创建了，所以生成的空的迁移文件，因为alembic不能和node prisma一样，第一次也会直接爬下数据库表结构来

---

### 9. 数据和结构都要迁移时，应该怎么组合工具？

请分别说明下面三种情况应该用什么：

1. 完整搬家：结构和数据都要复制到另一台机器；
2. 项目升级：新增字段、建索引、改表结构；
3. 结构变更时顺便修正少量旧数据。

**我的答案：**

1. 先使用alembic进行结构备份，然后使用datagrip类似的工具导出数据库
2. 只使用 alembic revision 然后 upgrade
3. 这个和第一种类似？ 或者使用sql或者orm进行操作旧数据，再此之前重复2

---

## 四、实战改错题（2 分）

### 10. 下面这份迁移流程有什么问题？请改成更安全的版本。

错误流程：

```bash
alembic init alembic
alembic revision --autogenerate -m "add email"
alembic upgrade head
```

背景：

- 项目使用 Poetry；
- 迁移文件生成后没有打开检查；
- 项目里的 `database.py` 已经从 `.env` 读取 `DATABASE_URL`。

请指出至少 2 个问题，并写出你认为更安全的流程。

**我的答案：**

项目里读取orm的元数据了吗，如果此前建立了数据库，迁移文件可能为空，env设定好地址了吗？
首先在env设置好地址
然后在文件中制定好orm元数据
检查有没有旧的数据库，然后创建一个新的空的数据库
然后执行以上操作


---

## 自评区

答完后先自己标记：

- [x] 我能说清 Alembic 和数据库备份不是一回事
- [ ] 我能说清 `create_all()` 和 Alembic 的边界
- [x] 我能说清 `target_metadata = Base.metadata`
- [ ] 我能写出 Poetry 项目的 Alembic 常用命令
- [x] 我能判断什么时候用备份，什么时候用 Alembic，什么时候写数据迁移 SQL

---

## 批改区

> 等用户答完后追加评分、错题、弱点和复习计划。

---

## 批改结果（2026-06-19）

### 总分

- 得分：13.7 / 20
- 通过线：16 / 20
- 结果：暂未通过，需要补一轮关键概念和命令精确度

你这次不是完全不会，而是“方向知道，工程边界和命令还不够硬”。最明显的好迹象是：你已经能区分 Alembic 不是数据备份工具，也能解释空迁移来自“数据库已有表，模型和数据库无差异”。

### 逐题评分

| 题号 | 得分 | 批改 |
|---|---:|---|
| 1 | 1.5 / 2 | 答对 Alembic 管数据库结构和生成迁移文件，但“版本备份”这个词不准确，容易和数据备份混淆。 |
| 2 | 1.2 / 2 | 知道 `create_all()` 适合初期，但没有说清混乱点：表可能已被 `create_all()` 建好，而 Alembic 的 `alembic_version` 不知道。 |
| 3 | 1.2 / 2 | 知道是 ORM 元数据，但结构信息说得太少；`target_metadata = None` 的结果应明确为 autogenerate 看不到模型，可能空迁移或报错。 |
| 4 | 2 / 2 | 三类工具边界清楚：Alembic 管结构，数据库工具管数据导出，pip/Poetry 管依赖。 |
| 5 | 1 / 2 | 命令方向记得，但缺少 Poetry 前缀和完整命令，`revision --autogenerate` 拼写也要更稳。 |
| 6 | 1.2 / 2 | 知道一个生成迁移、一个应用迁移，但仍把迁移文件叫“备份”，这个词要改掉。 |
| 7 | 0.7 / 2 | `alembic_version` 不是记录所有迁移文件，而是记录当前数据库处在哪个 revision；`stamp head` 忘了。 |
| 8 | 1.7 / 2 | 核心正确：数据库已经由 `create_all()` 建好，所以无差异生成空迁移；Prisma 对比也合理。 |
| 9 | 1.2 / 2 | 第 2 点正确；第 1 点应优先说数据库备份工具完整搬家，不是先 Alembic 结构备份；第 3 点要明确是 Alembic migration 里写少量 SQL/ORM 数据修正。 |
| 10 | 1 / 2 | 能想到 `.env`、metadata、旧数据库，但漏了两个最直接的问题：Poetry 项目要用 `poetry run`，迁移文件生成后必须先检查再 upgrade。 |

### 本轮主要错因

1. **把 migration 说成“备份”**

Alembic migration 不是备份，它是结构变更脚本。

```text
备份 = 保存当前完整状态
migration = 描述一次结构变化
```

2. **命令不够可复制**

本项目使用 Poetry，所以考试里命令必须写成：

```bash
poetry run alembic init alembic
poetry run alembic revision --autogenerate -m "add email"
poetry run alembic upgrade head
```

3. **`alembic_version` 和 `stamp head` 还没稳**

`alembic_version` 记录的是：

```text
当前数据库已经处在哪个 revision
```

`stamp head` 的意思是：

```text
不执行建表 SQL，只把当前已有数据库标记为已经到达最新 revision。
```

4. **结构迁移 vs 数据搬家边界还要再压实**

完整搬家优先用数据库备份工具：

```bash
sqlite3 my_database.db ".backup backups/my_database_backup.db"
```

项目结构升级用 Alembic：

```bash
poetry run alembic revision --autogenerate -m "add user email"
poetry run alembic upgrade head
```

结构升级时顺便修少量旧数据，才在 Alembic migration 里写：

```python
op.execute("UPDATE users SET email = username || '@example.com' WHERE email IS NULL")
```

### 最小复习计划

只补 4 个点，不扩大范围：

1. 背牢一句话：Alembic 是结构变更脚本，不是备份。
2. 重新默写三条 Poetry 命令：`init`、`revision --autogenerate`、`upgrade head`。
3. 用一句话解释 `alembic_version` 和 `stamp head`。
4. 区分三种场景：完整搬家用备份，结构升级用 Alembic，少量旧数据修正写进 migration。

### 需要补考的题型

下一轮只考 5 题：

- 1 题：migration vs backup 边界；
- 1 题：Poetry 命令默写；
- 1 题：`alembic_version` / `stamp head`；
- 1 题：已有数据库空迁移；
- 1 题：结构 + 数据迁移场景判断。
