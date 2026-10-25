# 06 Python 与高级语言：把注意力从内存搬回问题

> **作者与来源**：David J. Malan / CS50 团队，Harvard University。本文是非官方中文改编与补充，不代表 Harvard University 或 CS50 官方。课程材料依其许可使用；本改编按 [CC BY-NC-SA 4.0](./来源与许可.md) 说明。
> **官方材料**：[CS50x Week 6: Python](https://cs50.harvard.edu/x/weeks/6/) · [Lecture 6 Notes](https://cs50.harvard.edu/x/notes/6/) · [Problem Set 6 入口](https://cs50.harvard.edu/x/weeks/6/)

## 本章要做什么

这不是“忘掉 C，背 Python 语法”。我们把已经学过的计算、数组、函数和内存模型带过来，观察高级语言替我们承担了哪些杂务，同时保留对类型、数据和错误的判断能力。

贯穿例子是一个极小的知识文档目录：文档 id=1 是 Python 笔记，id=2 是 HTTP 笔记，id=3 是 SQL 笔记；前两篇 owner 都是 7，第三篇 owner 是 9。此前你接触过 Python、FastAPI 与 RAG，但基础可能有断层。本章从可运行代码重新接线，不假设“见过”就等于学会。

**本章目标**

- 把 C 中的数组、字符串和显式内存操作映射到 Python 的 `list`、`str`、引用与自动内存管理。
- 读写变量、条件、循环、函数、参数、返回值、类/对象/方法与异常。
- 用 `dict` 统计目录、搜索条目，用 `csv` / `json` 处理文件，并用命令行参数控制程序。
- 解释 Python 解释器执行路径、整数与浮点数边界，以及模块、包、第三方依赖与环境。
- 通过小改动和独立练习验证理解，而不靠“代码看起来熟悉”。

**边界**：本章学 Python 语言基础和本地文件处理；不讲 SQL 数据库查询（下一章）、网页前端 JavaScript（第 08 章）、Flask（第 09 章）、异步并发、类型系统细节或机器学习框架。CS50 辅助库 `cs50` 会被提及以便读懂官方代码，但本机练习不依赖它。

**前置**：能运行一个 C 程序，理解变量、数组、函数、循环、条件和指针/动态内存的大致作用。忘了也没关系，对照会重新搭桥。

## 1. 先看完整程序，再拆开它

下面是一份自包含小程序。它支持查看列表、按 id 查找、按标签统计；错误输入有明确反馈。它不读写真实应用或数据库。

文件名：examples/cs50x/catalog.py

~~~python
import sys


DOCUMENTS = [
    {"id": 1, "title": "Python 入门", "owner_id": 7, "tags": ["python", "基础"]},
    {"id": 2, "title": "HTTP 请求", "owner_id": 7, "tags": ["web", "基础"]},
    {"id": 3, "title": "SQL 查询", "owner_id": 9, "tags": ["database", "sql"]},
]


def find_document(document_id):
    for document in DOCUMENTS:
        if document["id"] == document_id:
            return document
    return None


def count_tags(documents):
    counts = {}
    for document in documents:
        for tag in document["tags"]:
            counts[tag] = counts.get(tag, 0) + 1
    return counts


def main(arguments):
    if len(arguments) == 1 or arguments[1] == "list":
        for document in DOCUMENTS:
            print(f'{document["id"]}: {document["title"]} (owner {document["owner_id"]})')
        return 0

    if arguments[1] == "show":
        if len(arguments) != 3:
            print("用法: catalog.py show ID")
            return 2
        try:
            document_id = int(arguments[2])
        except ValueError:
            print("ID 必须是整数")
            return 2
        document = find_document(document_id)
        if document is None:
            print("未找到文档")
            return 1
        print(f'{document["title"]}: tags={", ".join(document["tags"])}')
        return 0

    if arguments[1] == "tags":
        for tag, count in sorted(count_tags(DOCUMENTS).items()):
            print(f"{tag}: {count}")
        return 0

    print("用法: catalog.py [list|show ID|tags]")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
~~~

从仓库根目录运行：

~~~bash
poetry run python examples/cs50x/catalog.py list
poetry run python examples/cs50x/catalog.py show 1
poetry run python examples/cs50x/catalog.py show nope
poetry run python examples/cs50x/catalog.py tags
~~~

预期输出；每条命令独立执行：

~~~text
1: Python 入门 (owner 7)
2: HTTP 请求 (owner 7)
3: SQL 查询 (owner 9)
Python 入门: tags=python, 基础
ID 必须是整数
database: 1
python: 1
sql: 1
web: 1
基础: 2
~~~

正常返回 0，找不到文档返回 1，格式错误返回 2。终端通常不显示 0，但可用 echo $? 查看上一条命令退出状态。

## 2. C 的显式步骤，到 Python 的数据对象

### 2.1 同一条记录，两种表示

C 中，一个小目录可能用几个数组并排保存。下面是只读结构片段，不是独立可编译程序：

~~~text
int ids[3] = {1, 2, 3};
int owner_ids[3] = {7, 7, 9};
char *titles[3] = {"Python 入门", "HTTP 请求", "SQL 查询"};
~~~

ids[1]、owner_ids[1]、titles[1] 必须始终属于同一条记录；插入或删除时要保持几个数组同步移动。真实 C 程序中的字符串存储和动态扩容还涉及分配、容量、边界检查和释放。这不是 C “不好”，而是 C 把控制权交给程序员，也把责任一起交过来。

Python 把一条记录写成字典（`dict`，键到值的映射），多条记录写成列表（`list`，按顺序保存的可变序列）：

~~~python
documents = [
    {"id": 1, "title": "Python 入门", "owner_id": 7},
    {"id": 2, "title": "HTTP 请求", "owner_id": 7},
]
print(documents[1]["title"])
~~~

输出是 HTTP 请求。`documents[1]` 取出第二个字典，`["title"]` 再按键取值。Python 仍在内存里保存对象和引用；它只是把分配、增长和回收的大部分日常工作交给运行时。普通列表不需要手写 `malloc` / `free`，但逻辑生命周期仍需管理：不再需要的数据应从容器移除，文件要关闭，资源要释放。

### 2.2 变量不是带类型的盒子

C 的 `int count = 0;` 同时声明名字和固定类型的存储位置。Python 写 `count = 0`，名字 `count` 绑定到整数对象；后续可重新绑定。类型属于值，不是名字永久固定的属性：

~~~python
count = 0
count = count + 1
label = "文档数"
print(label, count)
~~~

输出：文档数 1。赋值 `=` 更新绑定，比较相等用 `==`。Python 在运行时检查操作是否合法；`"3" + 2` 会抛 `TypeError`，不会猜你的意思。`input()` 返回字符串，运算前要转换：

~~~python
raw_count = input("数量: ")
count = int(raw_count)
print(count + 1)
~~~

输入 `3`，输出 `4`。输入 `three` 会在 `int()` 处抛 `ValueError`，后面会处理。

### 2.3 `str`、`list`、`dict` 和循环

`str`（字符串）表示文本，是不可变序列。索引从 `0` 开始；`title[0]` 取首字符，但空字符串不能这样取。字符串方法 `lower()` 返回新字符串，不会原地改旧字符串：

~~~python
title = "Python 入门"
normalized = title.lower()
print(title)
print(normalized)
~~~

`str` 是 Unicode 文本序列；不要把“一个字符”和“一个字节”混为一谈，编码存储属于另一层问题。

`list` 适合有顺序且可能增删的集合。`append(value)` 在末尾添加，`len(items)` 返回元素个数。索引越界会抛 `IndexError`，因此不能照 C 的习惯假设数组后还有可读空间。

~~~python
titles = ["Python 入门", "HTTP 请求"]
titles.append("SQL 查询")
for title in titles:
    print(title)
~~~

`for title in titles` 每轮让 `title` 绑定到一个元素，不需要自己维护下标。需要序号时可用 `enumerate(titles, start=1)`；需要循环次数时，`range(3)` 产生 `0`、`1`、`2`，终点不包含。

`dict` 按键保存值，适合用稳定标识关联信息：

~~~python
owner_by_id = {1: 7, 2: 7, 3: 9}
print(owner_by_id[2])
print(owner_by_id.get(99, "不存在"))
~~~

输出 `7` 和 `不存在`。`d[key]` 在键不存在时抛 `KeyError`；`d.get(key, default)` 返回默认值。`in` 检查字典的键，不是值。字典查找平均表现通常接近常数时间，但不是对任意输入和实现环境的硬性时限保证。

### 2.4 从搜索到统计：追踪函数调用

回到 `find_document(document_id)`。调用 `find_document(2)` 时：

1. Python 为本次调用创建局部变量 `document_id`，值为整数 `2`。
2. `for document in DOCUMENTS` 依次让 `document` 绑定到三个字典。
3. 第一个字典的 `id` 是 `1`，条件为假；第二个的 `id` 是 `2`，条件为真。
4. `return document` 立刻结束本次调用，把第二个字典的引用交还调用者；第三条不再检查。
5. 如果遍历结束仍未匹配，执行 `return None`。`None` 表示“这里没有值”，不等于数字 `0` 或空字符串。

`count_tags` 用 `counts.get(tag, 0) + 1` 累加：第一次遇见标签，旧次数默认 `0`，加一后存回字典；后续读取旧次数再加一。两篇带“基础”的文档使计数依次变为 `1`、`2`。`sorted(count_tags(...).items())` 将键值对按标签排序，让输出稳定。

### 2.5 函数、参数和返回值

函数（function）把一段有名字的操作封装起来。`def count_tags(documents):` 定义函数；`documents` 是参数，调用时给它实际列表；`return counts` 把结果交回调用者。没有显式 `return` 的函数返回 `None`。

Python 支持位置参数和命名参数：

~~~python
print("A", "B", sep=" | ", end="!\n")
~~~

`"A"`、`"B"` 按位置交给 `print`，`sep=`、`end=` 按名称传值。自定义函数也可有默认参数，例如 `def list_documents(limit=10):`。不要把可变列表直接当默认值，因为它会在多次调用间共享。

### 2.6 类、对象和方法：简单代码不必硬套类

对象（object）把数据和操作它的行为放在同一运行时实体里。类（class）描述如何创建一类对象；实例（instance）是具体对象；方法（method）是定义在类中的函数，调用时作用于某个实例。

目录只有几条数据时，字典足够。若每条文档需要统一摘要行为，可写：

~~~python
class Document:
    def __init__(self, document_id, title, owner_id):
        self.document_id = document_id
        self.title = title
        self.owner_id = owner_id

    def summary(self):
        return f"{self.document_id}: {self.title} (owner {self.owner_id})"


document = Document(1, "Python 入门", 7)
print(document.summary())
~~~

输出：1: Python 入门 (owner 7)。`Document(...)` 创建实例并触发 `__init__`；`self` 是当前实例，赋值把传入值保存为实例属性；`document.summary()` 找到类上的方法并把 `document` 作为当前实例传入。多个对象共享字段和规则时用类；只是处理一小批临时字典时，类反而增加跳转成本。本章不展开继承和元类。

## 3. 条件、循环与异常

### 3.1 条件表达式

Python 用缩进划分代码块，以冒号开始块；`elif` 表示“否则如果”，逻辑运算符为 `and`、`or`、`not`：

~~~python
document_id = 2
if document_id < 0:
    print("id 不能为负数")
elif document_id in (1, 2, 3):
    print("目录中可能存在")
else:
    print("id 不在当前示例范围")
~~~

输出：目录中可能存在。括号中的 `tuple`（元组）是固定顺序的不可变序列，此处只用于表达允许值。布尔值是 `True` / `False`；比较值用 `==`，对象身份比较 `is` 不能替代值比较。判断没有结果常写 `document is None`。

### 3.2 for 与 while

优先用 `for` 遍历已有集合；重复条件由运行时状态控制时用 `while`。`break` 结束最近一层循环，`continue` 跳到下一轮。`while True` 校验输入时，必须让成功分支 `break` 或 `return`，否则会无限循环。

~~~python
raw_id = ""
while not raw_id.isdecimal():
    raw_id = input("请输入非负整数 id: ")
document_id = int(raw_id)
print(document_id)
~~~

输入 `abc` 后再次提示；输入 `12` 后输出 `12`。`isdecimal()` 判断字符串是否由十进制数字构成。这个校验不覆盖负号、空白或业务 id 范围；真实输入要先定规则再校验。

### 3.3 异常：把可预期失败变成清楚的路径

异常（exception）是运行时报告错误的机制。`try` 包住可能失败的语句，`except ValueError` 只处理整数转换失败；不要用空 `except` 吞掉所有故障。文件解析、命令行参数、用户输入都可能失败。主程序中的转换捕获非法 id，给出提示并返回非零退出码。捕获应靠近能够恢复或解释问题的位置；不知道如何恢复就让错误带上下文向上报告，而非伪装成功。

## 4. Python 如何运行：解释与编译并不互斥

解释器（interpreter）是运行 Python 程序的实现/程序，例如本机 `python` 命令启动的 CPython。入门时直接运行 `python file.py`，不需要像 C 那样自己先执行 `cc file.c -o file`。这不表示 Python“从来不编译”：常见 CPython 会把源代码编译成字节码（bytecode），由虚拟机执行；字节码缓存可能写入 `__pycache__`。不同 Python 实现策略可能不同，有的还会编译热点代码。

~~~text
C 源文件 --cc 编译/链接--> 本机可执行文件 --操作系统运行--> 机器指令
Python 源文件 --python 启动解释器（内部可生成字节码）--> Python 运行时执行
~~~

重点是开发者使用的工作流不同，不是“C 绝对编译、Python 绝对解释”。解释器仍需读取文件、解析语法、导入模块并执行操作；动态类型更灵活，也意味着某些类型错误要运行到那一行才发现。

运行命令 `poetry run python examples/cs50x/catalog.py list`：`poetry run` 让命令在项目 Poetry 环境中执行；`python` 选择解释器；最后是源文件及其命令行参数。

## 5. 数值边界：整数变大，不代表浮点精确

Python 内置 `int` 是任意精度整数，受可用内存限制，不是固定 32/64 位 C 整数的同一范围。因此 `10**100` 可以表示，但数值越大运算成本也可能增长。语言规则不可互套。

Python 的 `/` 返回浮点数，即使两个操作数是整数；`//` 是向负无穷取整的地板除。二进制浮点不能精确表示很多十进制小数：

~~~python
print(1 / 3)
print(0.1 + 0.2 == 0.3)
print(round(1 / 3, 3))
~~~

预期：显示近似小数、`False`、`0.333`。格式化只能限制显示位数，不改变近似值。金额若需十进制精度，可用标准库 `decimal.Decimal` 并明确舍入规则；计数、索引和 id 用整数。不要直接用 `==` 比较可能有舍入误差的计算结果。

## 6. 模块、包和第三方依赖

模块（module）通常是可导入的 Python 源文件；`import sys` 载入标准库模块，`sys.argv` 访问其属性。包（package）把多个模块组织到一个命名空间。第三方库是标准库之外由外部项目发布的代码。导入和安装是两件事：`import` 只会在当前解释器搜索路径查找，不会自动下载。

完整程序只用标准库 `sys`；文件练习用标准库 `csv`、`json`。CS50 官方示例常用 `from cs50 import get_int, get_string`，提供课堂输入函数；`cs50` 不是 Python 内置模块，需在 CS50 环境或自行安装。本项目没有要求加入它，本章用 `input()` 和 `int()` 练习相同机制。

第三方库必须装进正确 Python 环境。当前项目练习从仓库根目录使用 `poetry run python`；本章不安装任何包。若使用项目已声明依赖，先查看 `pyproject.toml` 和锁文件，不用全局 `pip` 随手改环境。

后续 Flask 是第三方 Web 框架，第 09 章另用独立临时环境；本章不提前安装。标准库已能清晰解决需求时，不必增加依赖。引入第三方库前要考虑维护、许可、安全和环境成本。

## 7. 文件：CSV 与 JSON

### 7.1 CSV：表格行，不是数据库

CSV（逗号分隔值）用文本表示行列。字段可能含逗号、引号或换行，不能随意 `line.split(",")`；让 `csv` 模块处理边界。下面程序从内存数据生成 CSV，再读回统计 owner，不需准备输入文件。

文件名：examples/cs50x/catalog_csv.py

相对路径固定写到练习目录中的 examples/cs50x/catalog.csv；每次运行都会覆盖并重写本程序内置的三条样例记录，不是追加。请只从仓库根目录运行文中的命令，不要把真实数据放进这个文件。

~~~python
import csv
from pathlib import Path


rows = [
    {"id": 1, "title": "Python, 入门", "owner_id": 7},
    {"id": 2, "title": "HTTP 请求", "owner_id": 7},
    {"id": 3, "title": "SQL 查询", "owner_id": 9},
]
path = Path("examples/cs50x/catalog.csv")

with path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "title", "owner_id"])
    writer.writeheader()
    writer.writerows(rows)

owner_counts = {}
with path.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        owner_id = int(row["owner_id"])
        owner_counts[owner_id] = owner_counts.get(owner_id, 0) + 1

print(f"写入并读取 {len(rows)} 条记录")
print(f"owner 7: {owner_counts[7]}")
print(f"owner 9: {owner_counts.get(9, 0)}")
~~~

从仓库根目录运行：`poetry run python examples/cs50x/catalog_csv.py`。预期输出：

~~~text
写入并读取 3 条记录
owner 7: 2
owner 9: 1
~~~

`Path.open` 创建文件对象；`with` 块退出时自动关闭文件；`DictWriter` 按列名写标题和字典行；重新打开后 `DictReader` 按列名生成字典。CSV 字段读入时都是文本，因此 `owner_id` 显式转为整数。`newline=""` 是 `csv` 模块推荐的打开方式，避免平台换行规则互相干扰。打印 owner 9 时用 `owner_counts.get(9, 0)`：如果数据里已没有 owner 9，结果显示 0，而不是因访问缺失键抛 `KeyError`。

### 7.2 JSON：嵌套对象的文本表示

JSON（JavaScript Object Notation）是常见的数据交换文本格式。标准库 `json` 的 `dumps` 把 Python 值编码成 JSON 字符串，`loads` 把字符串解析回 Python 值。它不是数据库；完整性约束、并发写入和高效查询应由合适的存储层承担。

~~~python
import json


document = {"id": 1, "title": "Python 入门", "owner_id": 7, "tags": ["python", "基础"]}
payload = json.dumps(document, ensure_ascii=False)
restored = json.loads(payload)
print(payload)
print(restored["tags"][0])
~~~

预期输出：

~~~text
{"id": 1, "title": "Python 入门", "owner_id": 7, "tags": ["python", "基础"]}
python
~~~

JSON `null` 对应 Python `None`，布尔值对应 `True`/`False`，对象键通常是字符串。语法可解析不代表业务可信；不可信 JSON 还要考虑体积、深度和字段校验。读写文件时用 `with open(..., encoding="utf-8")` 以及 `json.dump`/`json.load`，并处理文件错误与 `JSONDecodeError`。

## 8. 命令行参数：让调用者提供输入

`sys.argv` 是 `sys` 标准库模块提供的列表：第 `0` 项通常是脚本名，后续项是命令行参数。调用 `catalog.py show 2` 时大致是 [脚本路径, `"show"`, `"2"`]；注意 `"2"` 是字符串，需显式转成整数。

`raise SystemExit(main(sys.argv))` 把 `main` 的返回整数作为进程退出码。成功返回 `0`，错误用非零值，方便 shell 判断。标准库 `argparse` 可在命令变复杂时提供类型转换、选项和帮助；先用 `sys.argv` 看清基本机制。

~~~bash
poetry run python examples/cs50x/catalog.py show 2
echo $?
poetry run python examples/cs50x/catalog.py show nope
echo $?
~~~

预期分别输出文档标题且退出码 `0`，再输出 ID 必须是整数且退出码 `2`。`echo $?` 必须紧接被检查命令执行。

## 9. 改动验证：小改，不靠猜

在完整程序中把第三条记录的 `owner` 改成 `7`，再运行 `tags` 不会变化，这是预期，因为标签统计与 owner 无关。若要检查 owner 统计，在 CSV 程序中把第三条记录的 `owner_id` 改成 `7`，重跑时程序会重写样例文件并输出：

~~~text
写入并读取 3 条记录
owner 7: 3
owner 9: 0
~~~

打印 owner 9 用 `owner_counts.get(9, 0)`；owner 9 缺席时得到零，而不是访问不存在的键并抛 `KeyError`。这证明统计依据输入行而非写死输出。

再把 `count_tags` 中的 `counts.get(tag, 0) + 1` 暂时改成 `counts.get(tag, 1) + 1`，预期标签首次出现就从 `2` 起步。运行 `tags` 可以观察错误。恢复后回到“基础: 2”。这是本地临时故意改错验证，错误版本不是可运行成品。

## 10. 独立练习：最近访问记录

**需求**：写 `recent.py` 管理 `3` 条最近访问记录。每条含 `id`、`title`、`owner_id`、`tags`。新增 `owner ID` 命令，只打印该 owner 的文档；新增 `tag TAG` 命令，打印含指定标签的文档。不得连接数据库或引入第三方库。

**接口与验收**

- 运行 `poetry run python examples/cs50x/recent.py owner 7`，只显示 owner 7 的两条记录。
- 运行 `poetry run python examples/cs50x/recent.py tag python`，显示 Python 入门记录。
- 未知 owner / 标签输出“没有匹配项”，退出成功；错误命令给用法并非零退出。
- `ID` 不是整数时不能出现 `traceback`；标签区分大小写，除非自己明确实现规范化。
- 添加一个字典条目后查询自动包含它，不应手工改多个平行数组。

允许范围：`list`、`dict`、循环、条件、函数、字符串方法、`sys.argv`、异常。暂不使用 ORM、数据库或 Flask。先追踪 owner 7 如何从 `sys.argv` 到筛选再到输出，再写代码。

## 11. 常见坑

- input() 始终返回 str；按需转换并处理 ValueError。
- Python 不要求显式运行 C 风格编译器，但常见实现会编译字节码；解释/编译不是简单二选一。
- 名字可重新绑定，操作仍受类型规则约束；不要让混合类型掩盖数据错误。
- == 比值，is 比对象身份；判断 None 用 is None。
- 列表索引可能越界；优先遍历元素或先检查长度。
- str 不可变；lower()/replace() 返回新字符串。
- CSV 不要手工按逗号切分，使用 csv 模块。
- 全局 pip 与 Poetry 环境可能不同；可运行 poetry run python -c 'import sys; print(sys.executable)' 查看解释器位置。
- 浮点金额不宜直接比较；先选十进制策略与舍入规则。
- 不要 except: pass；捕获具体且能处理的失败。

## 12. 课后压缩

**心智模型**：C 让我看见字节、容量和所有权；Python 把常见容器与内存管理包进运行时，我仍需对类型、输入和失败路径负责。

**最小模板**：for row in rows: counts[key] = counts.get(key, 0) + 1。遍历输入，按键取旧次数，写回新次数。

**边界**：Python int 不等于无限成本；float 仍有二进制近似。CSV/JSON 是文件格式，不是关系数据库。

**复习问题**：新增文档字段时，为什么列表里的字典比三个平行数组不易错？命令行里的 "7" 为什么要转成整数 7？

## 13. 对应官方问题集

当前 [Problem Set 6](https://cs50.harvard.edu/x/psets/6/) 包括 Hello、Mario（两种难度选一）、Cash/Credit（二选一）、Readability 和 DNA。前几项用 Python 重新实现先前 C 任务，DNA 练习字符串与数据匹配。具体任务与提交方式以官方实时要求和 Academic Honesty 规则为准。中文主题对应复习：

- **Python 版问题重写**：把先前 C 问题转成 Python，观察字符串、列表、循环和函数如何改变表达方式。
- **文本/数字处理**：检查输入解析、条件、字典累计、边界输入和异常路径。
- **独立调试**：比较期望与实际输出，定位类型、循环边界和格式问题。

这里只提供主题导览，不提供官方题目解答或提交代码。CS50P 可作为后续系统练习，但不是本章替代品；本章核心代码与概念可在本地完成。

## 14. 前后导航

- 上一章：[05 数据结构的实现](./05_数据结构的实现.md)：从 C 容器、指针和所有权理解 Python 自动管理的背景。
- 本章产物：以 list/dict 表达目录，能读写 CSV/JSON 并通过命令行参数调用。
- 下一章：[07 SQL 与关系数据库](./07_SQL与关系数据库.md)：当目录要按条件检索、保持关联并支持多用户修改时，把内存/平面文件数据提升为关系表。
- 本章不把目录连到真实 FastAPI/RAG 应用；后续整合必须明确隔离环境、迁移和权限边界。

## 官方主题覆盖依据

以下依据 CS50x **2026** 官方 [Week 6 页面](https://cs50.harvard.edu/x/weeks/6/) 与 [Lecture 6 Notes](https://cs50.harvard.edu/x/notes/6/) 的主题目录和正文，不是仅凭记忆列标题。

| 官方主题 | 本文正文 |
| --- | --- |
| Python 与 C 的关系、Speller/Filter 式高层抽象 | 第 1、2 节：C 数组/内存映射到列表、字典，解释便利与代价 |
| Functions、Libraries / Modules / Packages | 第 2.5、6 节：参数、返回、标准库/第三方包与调用 |
| Strings、位置与命名参数、Variables、Types | 第 2.2、2.3、2.5 节 |
| Calculator、Conditionals、Object-Oriented Programming、Loops、Abstraction | 第 2、3 节及完整主程序 |
| Truncation / Floating Point Imprecision、Exceptions | 第 3.3、5 节 |
| Mario 的循环控制与输入边界 | 第 3.2 节及第 10 节练习，解释循环机制而不照搬图形题 |
| Lists、Searching and Dictionaries | 第 2.3、2.4 节及完整主程序 |
| Command-Line Arguments、Exit Status | 第 1、8 节 |
| CSV Files | 第 7.1 节完整读写程序 |
| Third-Party Libraries | 第 6 节：CS50 库、项目环境与 Flask 后续边界 |
