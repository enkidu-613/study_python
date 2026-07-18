# 09. 数据库与 SQL 入门

> **一句话理解：数据库用表长期、可查询地保存结构化数据；SQL 是向数据库表达“要什么数据”的语言。**

## 本章学什么，不学什么

学：表、行、列、主键、CRUD 与最小 SQLite SQL。

不学：ORM、迁移、高并发数据库设计或向量数据库；它们在项目主线中学习。

## 准确术语

| 术语 | 准确含义 |
| --- | --- |
| 数据库 | 专门保存和查询数据的软件系统。 |
| 表（table） | 同一类记录组成的二维结构。 |
| 行（row） | 一条记录，例如一项待办。 |
| 列（column） | 每条记录的一个字段，例如标题。 |
| 主键（primary key） | 唯一标识一行的列。 |
| CRUD | Create、Read、Update、Delete，增删改查。 |
| SQL | 操作关系型数据库的声明式语言。 |

## 最小模板：一张待办表

如果本机有 SQLite，终端执行：

```bash
sqlite3 tasks.db
```

进入 SQLite 后依次执行：

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
);

INSERT INTO tasks (title, done) VALUES ('学习 SQL', 0);
SELECT id, title, done FROM tasks;
UPDATE tasks SET done = 1 WHERE id = 1;
DELETE FROM tasks WHERE id = 1;
```

每条 SQL 后的分号表示语句结束。`WHERE id = 1` 非常关键：没有它的 `UPDATE` 或 `DELETE` 会影响表中所有行。

## 从业务到表

“用户有很多待办”可先设计：

| 列 | 含义 |
| --- | --- |
| `id` | 这条待办的唯一编号 |
| `title` | 用户看到的文字 |
| `done` | 是否完成 |
| `created_at` | 创建时间 |

先问“每条记录是什么”，再决定每一列，而不是先背 SQL。

## 常见坑

- 忘记 `WHERE`：更新或删除范围过大。
- 用标题当唯一标识：两个任务可以同名，主键才稳定。
- 把数据库当 Excel：数据库更适合被程序稳定查询和修改。
- 直接拼接用户输入到 SQL：后续要使用参数化查询，不能拼字符串。

## 检查点

- [ ] 能区分表、行、列和主键。
- [ ] 能解释 CRUD 的四个动作。
- [ ] 能说明 `WHERE id = 1` 为什么重要。
- [ ] 能写出“查询所有未完成待办”的 SQL：`SELECT ... WHERE done = 0`。

## 小练习

为“学习笔记”设计一张表，至少有 `id`、标题、正文、创建时间四列；写一条插入语句和一条按标题查询的语句。

## 下一步

继续：[10. 数据结构与性能直觉](10_数据结构与性能直觉.md)。
