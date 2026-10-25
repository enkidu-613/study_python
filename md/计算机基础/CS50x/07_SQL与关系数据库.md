# 07 SQL 与关系数据库：让数据关系由数据库守住

> **作者与来源**：David J. Malan / CS50 团队，Harvard University。本文是非官方中文改编与补充，不代表 Harvard University 或 CS50 官方。课程材料依其许可使用；本改编按 [CC BY-NC-SA 4.0](./来源与许可.md) 说明。
> **官方材料**：[CS50x Week 7: SQL](https://cs50.harvard.edu/x/weeks/7/) · [Lecture 7 Notes](https://cs50.harvard.edu/x/notes/7/) · [Problem Set 7 入口](https://cs50.harvard.edu/x/weeks/7/)

## 本章要做什么

上一章的 Python 列表和字典适合小数据处理，但程序一退出，内存数据通常就消失；数据多了，筛选、关联和多人同时写入会变复杂。CSV 可以保存表格，却不自动保证 id 唯一、引用一定存在，也不擅长安全地并发修改。

本章把同一个知识文档目录放进 SQLite：owner 7 有 Python/HTTP 文档，owner 9 有 SQL 文档；文档有标签，标签和文档是多对多关系。先看完整可执行实验，再拆 SQL 的读取、写入、约束、关系、索引、安全和事务。

**本章目标**

- 直接读写 SQL（Structured Query Language，结构化查询语言），理解关系数据库与平面 CSV 的区别。
- 设计 SQLite 表结构，使用主键、外键、NOT NULL、UNIQUE，理解 SQLite 类型亲和性与 NULL。
- 用 SELECT / INSERT / UPDATE / DELETE 完成 CRUD，并使用 WHERE、AND、OR、LIKE、ORDER BY、LIMIT、DISTINCT。
- 使用 COUNT、AVG、MIN、MAX、GROUP BY、HAVING、JOIN 与子查询回答目录问题。
- 解释多对多关系为何需要连接表，索引如何加速读取、为何增加写入与存储成本。
- 从 Python 标准库 sqlite3 安全执行参数化查询，说明事务、竞态、锁等待和权限边界。

**边界**：本章练 SQLite 和关系模型；不讲生产级 PostgreSQL 运维、ORM、迁移工具、连接池、隔离级别全谱、Web 登录认证或真实用户数据迁移。第 09 章 Flask 会把 Web 请求接到数据库，但不是本章前置。

**前置**：能读 Python 字典/列表和函数；上一章介绍过 CSV/JSON。SQL 本身从零解释，不假设此前数据库章节已经教过。

## 1. 先看完整程序与输出

这是一个本地 SQLite 教学实验。它用 Python 标准库 sqlite3 在内存中创建数据库，不会打开项目真实数据库或持久化用户数据。程序建表、插入样例、执行查询、展示事务回滚、建立索引并用绑定参数搜索。程序结束后，内存数据库自动消失。

文件名：examples/cs50x/catalog_sql.py

~~~python
import sqlite3


SCHEMA_AND_DATA = """
PRAGMA foreign_keys = ON;

CREATE TABLE owners (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (owner_id) REFERENCES owners(id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE document_tags (
    document_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (document_id, tag_id),
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

INSERT INTO owners (id, name) VALUES
    (7, 'Lin'),
    (9, 'Kai');

INSERT INTO documents (id, title, owner_id, body) VALUES
    (1, 'Python 入门', 7, '变量、列表和函数'),
    (2, 'HTTP 请求', 7, '请求与响应'),
    (3, 'SQL 查询', 9, '关系表与查询');

INSERT INTO tags (id, name) VALUES
    (1, 'python'),
    (2, '基础'),
    (3, 'web'),
    (4, 'database');

INSERT INTO document_tags (document_id, tag_id) VALUES
    (1, 1), (1, 2),
    (2, 2), (2, 3),
    (3, 2), (3, 4);
"""


def main():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    try:
        connection.executescript(SCHEMA_AND_DATA)

        print("目录")
        rows = connection.execute(
            """
            SELECT documents.id, documents.title, owners.name AS owner
            FROM documents
            JOIN owners ON owners.id = documents.owner_id
            ORDER BY documents.id
            """
        ).fetchall()
        for row in rows:
            print(f'{row["id"]}: {row["title"]} / {row["owner"]}')

        print("标签统计")
        rows = connection.execute(
            """
            SELECT tags.name, COUNT(*) AS document_count
            FROM tags
            JOIN document_tags ON document_tags.tag_id = tags.id
            GROUP BY tags.id, tags.name
            HAVING COUNT(*) >= 2
            ORDER BY tags.name
            """
        ).fetchall()
        for row in rows:
            print(f'{row["name"]}: {row["document_count"]}')

        print("参数查询")
        rows = connection.execute(
            """
            SELECT documents.title
            FROM documents
            JOIN document_tags ON document_tags.document_id = documents.id
            JOIN tags ON tags.id = document_tags.tag_id
            WHERE tags.name = ?
            ORDER BY documents.id
            """,
            ("基础",),
        ).fetchall()
        print(", ".join(row["title"] for row in rows))

        connection.execute("BEGIN")
        connection.execute(
            "INSERT INTO documents (id, title, owner_id) VALUES (?, ?, ?)",
            (4, "临时草稿", 7),
        )
        connection.rollback()
        remaining = connection.execute(
            "SELECT COUNT(*) FROM documents WHERE id = 4"
        ).fetchone()[0]
        print(f"回滚后临时记录数: {remaining}")

        connection.execute("CREATE INDEX idx_documents_owner ON documents(owner_id)")
        plan = connection.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM documents WHERE owner_id = ?",
            (7,),
        ).fetchall()
        print(f"查询计划包含索引: {any('idx_documents_owner' in row[3] for row in plan)}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
~~~

从仓库根目录运行：poetry run python examples/cs50x/catalog_sql.py

预期输出：

~~~text
目录
1: Python 入门 / Lin
2: HTTP 请求 / Lin
3: SQL 查询 / Kai
标签统计
基础: 3
参数查询
Python 入门, HTTP 请求, SQL 查询
回滚后临时记录数: 0
查询计划包含索引: True
~~~

最后一行依赖 SQLite 对小型数据集查询计划的选择；计划文本可能随版本变化。该实验建立的索引适用于 owner_id 条件；若版本/数据规模选择扫描，应以本机 EXPLAIN QUERY PLAN 为准，而不要把布尔值当作跨版本保证。本文没有执行这段完整代码，输出是预期行为说明，验证状态见末尾。

## 2. 平面文件与关系表解决的问题不同

### 2.1 CSV 能做什么，不能保证什么

CSV 可以保存行列文本；上一章用 DictReader 把每行读成字典。对一次性导出、交换数据、小规模单表记录，CSV 简单直接。它自身不强制 id 不重复、不保证 owner_id 指向现存 owner，也不提供多条关联查询、并发事务或字段约束。

若把 owner 名称、文档标题和多个标签塞进一张表，常见结果是 owner 名重复、标签写成带逗号字符串、修改一个 owner 名却要改很多行。关系数据库把实体拆到不同表中，用键表达关系，由数据库执行查询与约束。

### 2.2 SQL 是声明“想要什么”

SQL 是面向关系数据的领域专用语言。Python 通常逐步说明怎么循环；SQL 更常描述要哪些列、从哪些表取、按什么条件筛选。SQLite 是实现 SQL 数据库的一种嵌入式软件，本课用它创建本地文件数据库或内存数据库。

SQLite CLI 若已安装，可在仓库根目录运行 sqlite3 :memory:，在提示符输入 SQL；退出用 .quit。CLI 的 .schema、.tables、.mode 是客户端命令，不是 SQL。完整 Python 实验使用标准库，无需 CLI。

## 3. 表、列、类型与约束

### 3.1 四张表怎样表示目录

- owners：每位 owner 一行。
- documents：每篇文档一行，owner_id 指向其 owner。
- tags：每个不同标签一行。
- document_tags：一行表示“某文档贴了某标签”。

id 是主键（PRIMARY KEY），唯一识别一行。owner_id、document_id、tag_id 是外键（FOREIGN KEY），声明某个值必须引用另一张表中存在的主键。外键把“指向谁”变成数据库可检查的关系。

一篇文档有一个 owner，一个 owner 可有多篇文档，是一对多。一个标签可贴多篇文档，一篇文档也可有多个标签，是多对多。关系拆到 document_tags 连接表，每个关联一行；联合主键 (document_id, tag_id) 阻止重复贴相同标签。

### 3.2 约束：让非法状态难以写入

主程序使用的约束：

- INTEGER PRIMARY KEY：SQLite 中通常是行标识别名；插入时可省略，由 SQLite 分配整数 id。
- NOT NULL：该列不能缺值。
- UNIQUE：值不可重复，例如 owner 名和标签名。
- FOREIGN KEY：引用必须对应父表中的记录。
- DEFAULT：插入时省略 body 列，则使用空字符串。

复合主键由多列共同唯一确定一行。SQLite 外键检查需启用；实验执行 PRAGMA foreign_keys = ON。应用的每个连接都应设置此项，不能假设 SQLite 默认已启用外键。

约束不是输入校验的替代品，而是最后一道数据完整性保障。程序仍应给用户友好提示；数据库约束保护所有写入路径，包括脚本、管理任务和未来 API。

### 3.3 SQLite 类型亲和性与 NULL

SQLite 有五种存储类别：NULL、INTEGER、REAL、TEXT、BLOB。列声明通常形成类型亲和性（type affinity），表达建议的存储类别；除 STRICT 表等额外限制外，SQLite 一般允许其他存储类别的值。因此声明 age INTEGER 不等于严格拒绝所有非整数输入。

NULL 表示缺失/未知，不是 0、空字符串或字符串 "NULL"。与 NULL 比较要用 IS NULL / IS NOT NULL，不能写 value = NULL，因为 SQL 三值逻辑会让比较结果成为 UNKNOWN。COUNT(column) 忽略 NULL，COUNT(*) 统计行数。

字段必须有值时用 NOT NULL；“未知”是合法业务状态时，可保留 NULL 并在查询中明确处理。空字符串表示有一个长度为零的文本值，含义不同。

## 4. CRUD 与查询条件

CRUD 指 Create / Read / Update / Delete：创建、读取、更新、删除。SQL 对应 INSERT、SELECT、UPDATE、DELETE；CREATE TABLE 属于定义结构的 DDL。

除第 10 节明确自包含的完整实验外，本章第 4 至第 9 节 SQL 片段均依赖第 1 节创建的 schema 与样例数据；也可先执行第 10 节的完整 SQL，再逐段尝试。不要把依赖查询片段单独当作建库脚本运行。

这些片段是分别讲机制，不是一份必须连续执行的脚本。插入、改名、删除会改变后续查询结果；要对照正文的原始三篇文档，请新开一个内存数据库并重新运行第 10 节初始化实验，再尝试当前片段。Python 的 `main()` 返回后连接已经关闭，不能在它之外直接使用局部变量 `connection`。

### 4.1 读取：SELECT、WHERE 与排序

SELECT 指定列，FROM 指定表，WHERE 按条件过滤。以下 SQL 片段依赖第 1 节同名表结构和样例数据；它们不是单独建库脚本。

~~~sql
SELECT id, title
FROM documents
WHERE owner_id = 7 AND title LIKE '%Python%';
~~~

AND 要求两边都为真；OR 只需一边为真。混合 AND/OR 时用括号明确逻辑，例如 WHERE owner_id = 7 AND (title LIKE '%Python%' OR title LIKE '%HTTP%')。

LIKE 是模式匹配：% 匹配任意长度文本，_ 匹配一个字符。模式 '%thon%' 查找任意位置含 thon 的值。SQLite 的 LIKE 对 ASCII 字符通常不区分大小写；非 ASCII 大小写不应想当然，需要语言级规范化时应显式实现。

ORDER BY title ASC 按升序；DESC 降序。没有 ORDER BY 时不能依赖固定返回顺序。LIMIT 2 限制最多返回两行；大数据分页还需稳定排序键。

~~~sql
SELECT DISTINCT owner_id
FROM documents
ORDER BY owner_id;
~~~

DISTINCT 去除结果中的重复行；这里返回出现过的 owner id。它不修复数据表中的重复数据，只影响查询结果。

### 4.2 写入：INSERT、UPDATE、DELETE

INSERT 指定表和列，再提供对应值。显式列名比依赖列顺序更清楚：

~~~sql
INSERT INTO documents (title, owner_id, body)
VALUES ('向量索引', 7, '向量检索笔记');
~~~

UPDATE 修改匹配行：

~~~sql
UPDATE documents
SET title = 'HTTP 与响应'
WHERE id = 2;
~~~

DELETE 删除匹配行。当前 schema 没有设置 ON DELETE CASCADE；id=3 在 document_tags 中有引用，因此不能直接删除 documents.id=3。外键会阻止删除仍被引用的父行，避免留下孤儿关联。正确顺序是先删关联行，再删文档，并把两步放在同一事务中：

~~~sql
BEGIN;
DELETE FROM document_tags
WHERE document_id = 3;
DELETE FROM documents
WHERE id = 3;
COMMIT;
~~~

如果任一步失败，应 ROLLBACK，不能留下“关联已删但文档还在”这种半完成状态。也可以在 schema 中定义 ON DELETE CASCADE，但本章 schema 没有这样做，所以示例显式删除连接行。UPDATE/DELETE 漏掉 WHERE 会作用于整张表。运行前先将相同 WHERE 放进 SELECT 检查目标；生产操作还需备份、授权与迁移流程。本章只在内存数据库实验。

实际业务通常让 INTEGER PRIMARY KEY 自动分配 id，然后通过 cursor.lastrowid 或 RETURNING（需确认 SQLite 版本）取得新 id。

## 5. 聚合：从行变成统计结果

聚合函数把多行压缩成统计值。COUNT(*) 计行数，COUNT(column) 忽略 NULL，MIN/MAX 求极值，AVG 求平均值，SUM 求和。GROUP BY 按列分组，每组计算聚合：

~~~sql
SELECT owner_id, COUNT(*) AS document_count
FROM documents
GROUP BY owner_id
ORDER BY document_count DESC;
~~~

AS document_count 给结果列取别名。主程序标签查询把 tags 和连接表合并，按标签分组；HAVING COUNT(*) >= 2 在分组后筛掉数量不足的组。

WHERE 与 HAVING 职责不同：WHERE 在分组前筛原始行；HAVING 在聚合后筛分组。统计每个 owner 的文档数且只保留至少两篇：

~~~sql
SELECT owner_id, COUNT(*) AS n
FROM documents
GROUP BY owner_id
HAVING COUNT(*) >= 2;
~~~

## 6. JOIN 与子查询：跨表回答问题

### 6.1 JOIN 如何把关系暂时拼起来

JOIN 根据相关列组合行。主程序查询目录：

~~~sql
SELECT documents.id, documents.title, owners.name AS owner
FROM documents
JOIN owners ON owners.id = documents.owner_id
ORDER BY documents.id;
~~~

每篇文档用 documents.owner_id 到 owners.id 找匹配行，输出合并后的列。省略 JOIN 类型时默认 INNER JOIN：没有匹配 owner 的行不出现在结果中。外键保证正常数据中 owner 存在，但仍需写清连接条件。

多表连接时给列加表名前缀，避免 id、name 等字段歧义。也可用短别名：FROM documents AS d JOIN owners AS o ON o.id = d.owner_id。

### 6.2 多对多：文档标签连接表

若把多个标签塞进 documents.tags 一列，查找、统计、重命名都会脆弱。连接表 document_tags 让每条关系独立存在。查询含“基础”标签的文档：

~~~sql
SELECT documents.title
FROM documents
JOIN document_tags ON document_tags.document_id = documents.id
JOIN tags ON tags.id = document_tags.tag_id
WHERE tags.name = '基础'
ORDER BY documents.id;
~~~

追踪一行：documents 的 id 1 匹配 document_tags.document_id 1；该连接记录 tag_id=2；tags.id=2 对应“基础”，因此得到“Python 入门”。id 2 和 3 也各有“基础”，结果有三篇。

### 6.3 子查询：先求一组 id，再外层读取

子查询是嵌在另一查询中的 SELECT。找 owner 名为 Lin 的文档标题：

~~~sql
SELECT title
FROM documents
WHERE owner_id = (
    SELECT id FROM owners WHERE name = 'Lin'
);
~~~

内层先取得 Lin 的 id=7，外层再查 owner_id=7。若内层可能返回多行，单值等号不合适，可改 IN (SELECT ...)。许多子查询也能用 JOIN 表达；选择更清楚、正确且计划合理的写法，不因嵌套“显得高级”就优先使用。

## 7. 索引与 EXPLAIN QUERY PLAN

索引（index）是数据库为特定列维护的辅助查找结构，像书末索引，能避免每次从头扫描。SQLite 常用 B-tree 索引；索引占空间，并使 INSERT、UPDATE、DELETE 额外维护结构。

为 owner_id 建索引并检查查询计划：

~~~sql
CREATE INDEX IF NOT EXISTS idx_documents_owner ON documents(owner_id);
EXPLAIN QUERY PLAN
SELECT id, title FROM documents WHERE owner_id = 7;
~~~

`IF NOT EXISTS` 表示该名字的索引已存在时不重复创建，便于在刚执行过完整实验的连接里查看计划；它不会验证一个已有同名索引是否采用你想要的列，真实迁移仍需核对结构。

计划可能显示 SCAN（扫描）或 SEARCH ... USING INDEX（通过索引搜索）。查询计划用来理解策略，不是性能计时器。样例只有 3 行，扫描往往更便宜；数据足够大且筛选有选择性时索引才更可能有益。不要对每列盲目加索引，也不要凭极小样本断言快慢。

常用于筛选、JOIN、排序的列可能适合索引；主键/UNIQUE 约束通常也会建立相应索引。索引不是权限控制，也不会自动阻止重复，除非是唯一索引/UNIQUE 约束。

## 8. Python 调用 SQL：连接、参数与返回行

主程序用 Python 标准库 sqlite3，不需额外依赖。sqlite3.connect 创建连接对象，表示应用与数据库的一次会话；connection.execute 执行 SQL 并返回游标；fetchall() 取出结果列表。设置 row_factory=sqlite3.Row 后，可按列名或位置访问行。

### 8.1 参数化查询防注入

SQL 注入（SQL injection）是把不可信输入拼进 SQL 文本，让输入意外变成 SQL 语法。下面仅为危险形状示意，不要运行：

~~~text
query = "SELECT id FROM owners WHERE name = '" + user_input + "'"
~~~

输入包含引号和 SQL 片段时可能改变查询含义。正确方式是绑定参数：

~~~python
row = connection.execute(
    "SELECT id FROM owners WHERE name = ?",
    (user_input,),
).fetchone()
~~~

问号是参数占位符；第二个参数是值序列，单个参数写成 (user_input,) 才是一个元素的 tuple。驱动把参数作为数据绑定，不会把其中引号解释为 SQL 语法。不能用字符串格式化、f-string 或拼接替代绑定。

参数通常只能绑定值，不能绑定表名、列名、关键字或 ASC/DESC。动态查询结构应从代码定义的白名单中选择标识符，再组合固定 SQL 片段；不能让用户提交任意 SQL。

参数化不等于权限校验。它阻止输入改变 SQL 结构，但不会自动限制用户能读哪些文档或是否有权修改某 owner 的数据。授权须在业务层/数据库权限边界单独检查；同一操作系统用户直接读写本地 SQLite 文件时，应用层检查无法阻止其绕过应用。

### 8.2 Python 到 SQLite 的完整调用链

以主程序标签搜索为例：

1. connection.execute 收到固定 SQL 文本和 tuple ("基础",)。
2. SQLite 驱动把值绑定到 SQL 中的问号，不把它解析成 SQL 代码。
3. 数据库执行 JOIN / WHERE / ORDER BY 并产生行。
4. fetchall() 把游标剩余行读成列表；row_factory 使每行可用 row["title"] 访问。
5. Python 的 join 把标题列表合并为逗号分隔文本，再打印。

写入也要绑定值。sqlite3 的事务行为由连接配置控制；主程序显式 BEGIN 和 rollback() 展示原子撤销。需要保留的改动必须提交；with connection 可在成功时提交、出错时回滚，具体使用前要理解连接上下文管理器不负责关闭连接。

## 9. 事务、原子性、竞态与锁

事务（transaction）把多条数据库操作作为一个整体。ACID 常用来描述：原子性（Atomicity，一起成功或一起撤销）、一致性（Consistency，约束维持合法状态）、隔离性（Isolation，并发操作按数据库规则彼此隔离）、持久性（Durability，提交后按存储保障保留）。本章重点实验原子性；SQLite 锁策略与隔离细节不等于所有数据库相同。

主程序 BEGIN 后插入 id=4，再 rollback()；随后查询计数应为 0，表示未提交插入已撤销。改成 commit()，查询会得到 1，但内存数据库关闭后仍消失。

竞态条件（race condition）是结果取决于多个并发操作交错顺序的情形。库存逻辑若先读库存，再在应用层判断，随后写回新值，两个请求可能都读到 1 并都认为有货。

- **覆盖写（lost update / lost-update oversell）**：两个请求都计算出新库存 0，再分别执行 SET stock = 0。最终数字仍是 0，但系统可能已接受两笔订单，实际只有一件库存，发生超卖/丢失更新；这个交错本身不必然让库存变负。
- **无条件递减**：两个请求都基于旧读数判断成功，随后各执行 SET stock = stock - 1。若数据库允许这两次更新依次生效，库存可能变成 -1。

这两种写法的问题和结果不同。事务能把多步操作组合起来，但仅仅把“先读、后判断、再写”包进事务，不代表所有数据库隔离级别下都自动正确。更稳妥的库存扣减通常把条件与变更合并为一条原子语句，然后检查受影响行数：

~~~sql
UPDATE inventory
SET stock = stock - 1
WHERE item_id = 42 AND stock > 0;
~~~

受影响 1 行表示扣减成功，0 行表示没有该商品或库存不足。若此更新属于更大的多表业务操作，再用事务保证整体原子性。具体并发结果仍取决于数据库的锁与隔离语义；SQLite 并发写入可能等待或返回 SQLITE_BUSY，调用方应有明确的冲突处理。

SQLite 支持并发读取，但写入会受到数据库锁和忙等待策略限制；多个写者同时修改可能等待或遇到 SQLITE_BUSY。事务不会自动解决所有并发问题，也不替代重试边界、幂等设计或业务约束。避免长事务；锁错误用有限重试和日志处理，不可无限重试。

最小 SQL 事务形状：

~~~sql
BEGIN;
UPDATE documents SET title = '新标题' WHERE id = 1;
UPDATE documents SET body = '新内容' WHERE id = 1;
COMMIT;
~~~

若步骤失败且决定放弃，则执行 ROLLBACK。事务期间不要等待用户输入或外部网络响应，否则会长时间占锁。

## 10. 完整原始 SQL 实验

若希望直接读 SQL，而非 Python 封装，可从仓库根目录运行 sqlite3 :memory:，再按顺序粘贴下列代码。内存数据库只活在当前 CLI 会话。以下从建表、数据、查询到事务完整自含；不要粘贴到真实数据库。

~~~sql
PRAGMA foreign_keys = ON;

CREATE TABLE owners (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES owners(id),
    body TEXT NOT NULL DEFAULT ''
);
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE document_tags (
    document_id INTEGER NOT NULL REFERENCES documents(id),
    tag_id INTEGER NOT NULL REFERENCES tags(id),
    PRIMARY KEY (document_id, tag_id)
);

INSERT INTO owners (id, name) VALUES (7, 'Lin'), (9, 'Kai');
INSERT INTO documents (id, title, owner_id) VALUES
    (1, 'Python 入门', 7),
    (2, 'HTTP 请求', 7),
    (3, 'SQL 查询', 9);
INSERT INTO tags (id, name) VALUES
    (1, 'python'), (2, '基础'), (3, 'web'), (4, 'database');
INSERT INTO document_tags (document_id, tag_id) VALUES
    (1, 1), (1, 2), (2, 2), (2, 3), (3, 2), (3, 4);

SELECT id, title FROM documents
WHERE owner_id = 7 AND title LIKE '%Python%'
ORDER BY id LIMIT 10;

SELECT DISTINCT owner_id FROM documents ORDER BY owner_id;

SELECT tags.name, COUNT(*) AS n
FROM tags
JOIN document_tags ON document_tags.tag_id = tags.id
GROUP BY tags.id, tags.name
HAVING COUNT(*) >= 2
ORDER BY tags.name;

SELECT documents.title
FROM documents
JOIN document_tags ON document_tags.document_id = documents.id
JOIN tags ON tags.id = document_tags.tag_id
WHERE tags.name = '基础'
ORDER BY documents.id;

CREATE INDEX idx_documents_owner ON documents(owner_id);
EXPLAIN QUERY PLAN
SELECT id FROM documents WHERE owner_id = 7;

BEGIN;
INSERT INTO documents (id, title, owner_id) VALUES (4, '临时草稿', 7);
ROLLBACK;
SELECT COUNT(*) FROM documents WHERE id = 4;
~~~

预期查询结果依次包含 Python 入门、owner 7/9、基础标签计数 3、三篇带“基础”的文档、查询计划，以及回滚后的计数 0。EXPLAIN 输出与索引是否被选中取决于 SQLite 版本和数据规模。建表语句只适用于全新内存数据库；在已有库重复执行会报表已存在。

## 11. 小改动验证

1. 在原始 SQL 实验再插入 owner_id=404 的文档。外键启用且 owner 不存在，预期插入失败；SQLite CLI 可能继续执行后续语句，读取错误信息。
2. 重复插入同一文档-标签关系。复合主键应拒绝重复 document_id/tag_id。
3. 把标签统计的 HAVING 条件从 >= 2 改为 >= 3。基础仍显示，其他标签不显示。
4. 把参数查询改成标签 web，预期仅得到 HTTP 请求。SQL 结构不变，只有数据不同。
5. 在 Python 实验把 rollback() 改为 commit()，预期临时记录数变为 1。恢复 rollback() 后应为 0。

## 12. 独立练习：文档与标签查询

**需求**：为目录增加作者和文档分类实体。设计表与约束，支持按 owner 查文档、按标签查文档、统计每标签关联数、只显示至少 2 篇文档使用的标签、修改文档标题；并在事务中把一个标签关联到两篇文档，若任一 id 不存在则撤销整个修改。

**输入输出契约**

- 初始数据至少 3 个 owner、5 篇文档、4 个标签；至少一篇文档有两个标签，至少一标签关联两篇文档。
- 按标签查询按文档 id 升序输出标题；不存在标签时为空结果。
- 重复插入同一文档-标签关系必须被拒绝。
- 引用不存在 owner 的文档必须被外键拒绝。
- 修改非法 id 后回滚；原有文档与标签关系保持不变。
- 用户输入须参数绑定；不能拼接输入到 SQL。

先写 schema，再写 seed 数据，再逐条写查询。用 sqlite3 :memory: 或 Python 内存连接，不接真实项目数据库。允许本章 SELECT、JOIN、子查询、聚合、约束和事务；不使用 ORM。

## 13. 常见坑与安全检查

- **漏 WHERE**：UPDATE/DELETE 可能影响整表；先用 SELECT 验证目标。
- **把 NULL 当 0**：NULL 表示缺失/未知；用 IS NULL，理解 COUNT(column) 忽略它。
- **误以为 SQLite 类型声明绝对严格**：了解类型亲和性，应用端仍要校验。
- **忽略外键启用**：每个 SQLite 连接执行 PRAGMA foreign_keys = ON。
- **多对多塞逗号字符串**：用连接表表达每条关联。
- **依赖返回顺序**：没有 ORDER BY 不保证固定顺序。
- **滥用索引**：它会占空间并增加写入成本；用查询计划验证。
- **拼接用户输入**：使用 ? 占位符；标识符从白名单选择。
- **把参数化当授权**：绑定阻止输入改变 SQL 语法，不校验用户能否访问该行。
- **把事务当并发万能药**：事务仍受锁、隔离和业务逻辑影响；短事务、条件更新、检测冲突。
- **把执行成功当持久化**：确认提交；异常时回滚；关闭连接前确认事务状态。

## 14. 课后压缩

**心智模型**：表保存实体，主外键表达关系，约束阻止非法状态，查询声明要取什么；事务把多步变更作为整体。

**最小模板**：

~~~python
rows = connection.execute(
    "SELECT id, title FROM documents WHERE owner_id = ? ORDER BY id",
    (owner_id,),
).fetchall()
~~~

**两个边界**：索引以额外存储和写入成本换取某些查询更快；参数化防 SQL 结构注入，但不代替授权。

**复习问题**：为什么一篇文档与多个标签要用连接表？COUNT(*) 和 COUNT(column) 有何差别？回滚证明了什么、又没有证明什么？

## 15. 对应官方问题集

当前 [Problem Set 7](https://cs50.harvard.edu/x/psets/7/) 包括 Songs（歌曲数据查询）、Movies（电影与人物关联查询）、Fiftyville（用 SQL 逐步查证线索）。按官方实时任务、提交方式及 Academic Honesty 规则为准，不在这里提供查询答案。中文复习主题：

- **SQL 筛选与排序**：选列、组合 WHERE、模式匹配、排序、去重与限制行数。
- **聚合与分组**：按类别统计、排序聚合结果，辨认 WHERE 与 HAVING 阶段差异。
- **关联查询**：理解键，组合多个表并确认连接条件不会漏行或重复计数。
- **正确性与安全**：约束、参数绑定、边界输入、NULL 和事务失败路径。

这里只解释主题与入口，不提供官方题解、SQL 成品答案或提交内容。

## 16. 前后导航

- 上一章：[06 Python 与高级语言](./06_Python与高级语言.md)：用 list/dict、CSV/JSON 表示目录与文件数据。
- 本章产物：owners/documents/tags/document_tags 关系模式，以及从 Python 执行安全查询的调用链。
- 下一篇：[AI 专题](./11_AI专题.md)，按官方目录位于 SQL 后；之后进入 [08 HTML、CSS、JavaScript](./08_HTML_CSS_JavaScript.md)，从浏览器界面组织输入与结果；此处数据库仍由本地 Python 直接调用。
- 第 09 章会把 Web 请求接到数据库；届时应考虑用户身份、授权、CSRF/输入校验、部署数据库和迁移。本章内存实验不构成生产配置。

## 官方主题覆盖依据

依据 CS50x **2026** [Week 7 页面](https://cs50.harvard.edu/x/weeks/7/) 与 [Lecture 7 Notes](https://cs50.harvard.edu/x/notes/7/) 实际讲义。官方讲义从 CSV 平面文件过渡到关系数据库，也包含 Python 调用 SQL、竞态与注入。

| 官方主题 | 本文正文 |
| --- | --- |
| Flat-File Database、Relational Databases | 第 2 节：CSV 能力边界和实体拆表理由 |
| SELECT、INSERT、DELETE、UPDATE | 第 4 节与第 10 节完整 SQL 实验 |
| 表、类型、主键/外键、NOT NULL、UNIQUE | 第 3 节及完整 schema |
| WHERE、AND、OR、LIKE、ORDER BY、LIMIT、DISTINCT | 第 4 节 |
| COUNT、AVG、MIN、MAX、GROUP BY、HAVING | 第 5 节；函数含义与分组筛选均有解释 |
| IMDb 关系样例、JOIN、多对多与子查询 | 第 3、6 节以文档-标签模型具体展示 |
| Indexes、B-tree、速度与空间权衡 | 第 7 节含 CREATE INDEX 与 EXPLAIN QUERY PLAN |
| Using SQL in Python | 第 1、8 节使用标准库 sqlite3 的完整实验 |
| Race Conditions、Transactions | 第 9 节：库存交错、BEGIN/COMMIT/ROLLBACK 和 SQLite 锁边界 |
| SQL Injection Attacks | 第 8.1 节：危险形状、参数绑定和授权边界 |
