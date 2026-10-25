# 09. 更多 Python 特性：把课程工具连起来

> 原作者：David J. Malan 与 CS50 team（CS50 团队），Harvard University。中文改编：enkidu-613。
> 原始资料：[Lecture 9 笔记](https://cs50.harvard.edu/python/notes/9/) · [Week 9](https://cs50.harvard.edu/python/weeks/9/)。
> 本文按官方 Et Cetera 的完整顺序进行中文改编，不是逐字翻译或 AI 项目知识子集；按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享，详见[来源与许可](来源与许可.md)。

## 起点、环境与边界

前置：前面各单元的函数、容器、异常、模块、测试、类与方法。本章完整学习官方主题；心智模型是用不同工具管理集合、作用域、调用接口与按需计算，明确各自契约。
本章保留官方学生、账户、叫声、金币、喊话与数羊场景，递归标为周短片补充；不展开高级类型、装饰器实现或异步生成器，项目设计在下一章。

在已激活的 Python 环境中，将各块放入标明的 `.py` 文件，在其目录运行 `python 文件名.py`。各 Python 块完整独立，同名文件后续版本替换前版，不要拼接。
除可选的 `mypy` 外，只用内置功能与标准库，本次未安装软件或修改依赖。命令与预期输出是学习说明，不冒充你已完成的交互或第三方验证。

## 1. set：让数据结构负责去重（houses.py）

```python
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
]
houses = set()
for student in students:
    houses.add(student["house"])
for house in sorted(houses):
    print(house)
```

只输出一次 `Gryffindor` 和一次 `Slytherin`。`set` 是内置集合类，`set()` 创建空实例；`add` 加入元素但不增加重复副本，返回 `None`。
集合没有可依赖的位置顺序，`sorted(houses)` 返回有序新列表。`{}` 是空字典；集合元素须可哈希，即具有稳定哈希值并满足相等比较契约，可变字典不能直接加入。
需保留重复或位置时用列表，只关心值是否出现时用集合；不要把“去重”误解为原学生记录被删除。

## 2. global：读取与重新绑定不同（bank.py）

```python
balance = 0


def deposit(amount):
    global balance
    balance += amount


def withdraw(amount):
    global balance
    balance -= amount


print("Balance:", balance)
deposit(100)
withdraw(50)
print("Balance:", balance)
```

顶层调用函数，余额从 0 变为 50。`global` 是作用域声明：仅读取通常不需要，本例 `+=` 重新绑定 `balance`，所以声明它属于模块最外层作用域，不是整个机器共享的名字。
若去掉声明，赋值使函数把 `balance` 视为局部名字，而 `+=` 先读再写，读到尚未绑定的局部变量会报 `UnboundLocalError`。
修改列表内容不等于重新绑定名字，不是所有修改都需 `global`。全局状态让依赖不明显，官方接着用账户实例保存余额：

```python
class Account:
    def __init__(self):
        self._balance = 0

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        self._balance -= amount


account = Account()
account.deposit(100)
account.withdraw(50)
print(account.balance)
```

调用者选择 `account`，方法更新其 `_balance`，getter 返回 50；不同账户可有不同余额。这里不含金额验证、余额不足检查或持久化，重点是状态归属。

## 3. 常量：大写不等于只读（constants.py）

```python
MEOWS = 3


class Cat:
    MEOWS = 2

    def meow(self):
        for _ in range(Cat.MEOWS):
            print("meow")


print(MEOWS)
Cat().meow()
```

先输出 3，再输出两次 `meow`；`Cat.MEOWS` 与模块的 `MEOWS` 不同。常量是约定不重赋值的名字，大写不构成只读限制。
`Cat.MEOWS` 是类属性，并非各实例的独立副本。

## 4. 类型提示与 mypy：契约不是转换（meows.py）

```python
def meow(n: int) -> None:
    for _ in range(n):
        print("meow")


number: int = int(input("Number: "))
meow(number)
```

输入 2 只打印两次 `meow`；函数隐式返回 `None`，但此处不使用它。`input` 返回字符串，`range` 需要整数；`n: int`、`-> None`、`number: int` 分别是参数、返回类型和变量注解，不是校验调用。
调用者提供整数；`meow` 的工作是打印这个副作用，不是返回一段文字。把它的调用结果用于赋值，`mypy` 还可能报 `func-returns-value`；修正输入转换后也不应保留这种赋值。
去掉转换后，类型提示不会自动将 `input` 的字符串转为整数，运行仍会 `TypeError`；非数字在 `int` 处会 `ValueError`，可复用异常单元的重试处理。

`mypy` 是第三方静态检查工具，读取源码与注解，帮助发现参数类型及返回值使用问题；它不是解释器，不需 `import mypy`，也不保证完全正确。以下可选指令本次未执行或写入项目依赖：

```bash
python -m pip install mypy
python -m mypy meows.py
```

可跳过安装；需检查时使用自己的练习环境。把 `number` 改成直接接收 `input`，比较修复前后的诊断；结果受注解、版本及配置影响，检查通过不证明所有输入合法。

## 5. docstring：把说明放在可读取的位置

替换 `meows.py` 为返回字符串的版本，打印与返回现在分开：

```python
def meow(n: int) -> str:
    """Return n meows, one per line.

    :param n: Non-negative repetition count.
    :return: One string containing the repeated lines.
    :raises ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return "meow\n" * n


print(meow(2), end="")
print(meow.__doc__)
```

docstring 是函数、类或模块主体开头的字符串字面量，保存在 `__doc__`。本版返回字符串，由外部 `print` 输出，与上一版 `-> None` 不同。
三引号便于多行，但并非任意位置的三引号字符串都是文档。`#` 注释主要供读源码，docstring 还可由 `help(meow)` 和文档工具读取。
参数、返回与异常说明须和代码一致，文字不自动执行规则。官方提及第三方 Sphinx 可据此生成文档，此处只认识、不安装。

## 6. argparse：解析命令行参数

`meows_cli.py` 把原先手工检查 `sys.argv` 长度、位置与 `-n` 的逻辑交给标准库：

```python
import argparse

parser = argparse.ArgumentParser(description="Print meows")
parser.add_argument("-n", default=1, type=int, help="number of meows")
args = parser.parse_args()
if args.n < 0:
    parser.error("-n must be non-negative")
for _ in range(args.n):
    print("meow")
```

`argparse` 是标准库，处理选项、转换、帮助与参数错误，不做业务计算。`ArgumentParser` 类创建解析器，`add_argument` 登记选项契约。
`parse_args()` 默认读命令行参数并返回 `Namespace`，`args.n` 取得整数；`type=int` 真正转换，`default=1` 提供默认值，与类型提示不同。
变量名 `args` 只是选择，与后文 `*args` 语法无自动联系；`argparse` 也不代替 `input` 的交互式提问。

```bash
python meows_cli.py
python meows_cli.py -n 3
python meows_cli.py --help
python meows_cli.py -n hello
```

依次应打印一次、三次、帮助信息、转换错误；`-n -1` 触发补充的范围检查，`parser.error` 报告错误并结束。不需重复 `int(args.n)`。

## 7. 解包：赋值与调用（coins.py）

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


first, last = "David Malan".split()
print(first, last)
coins = [100, 50, 25]
print(total(*coins), "Knuts")
named_coins = {"knuts": 25, "galleons": 100, "sickles": 50}
print(total(**named_coins), "Knuts")
```

赋值解包把右侧元素绑定给左侧名字，此处恰好两项，否则 `ValueError`。真实姓名未必两部分；`first, _` 的 `_` 也只是普通变量名。
调用处 `*coins` 展开位置实参，依次传入 100、50、25；`**named_coins` 按键名展开关键字实参，键顺序不影响换算，两次均为 `50775 Knuts`。
`*字典` 只展开键；`**` 的关键字名须为字符串，展开后仍须符合签名，缺项、未知关键字或重复提供同一参数都会报错。

## 8. *args 与 **kwargs：收集与展开（arguments.py）

```python
def inspect(*args, **kwargs):
    print("Positional:", args)
    print("Named:", kwargs)


inspect(100, 50, knuts=25)
print("This", "is", "CS50", sep="-", end="!\n")
```

定义处 `*args` 收集额外位置实参为元组，`**kwargs` 收集额外关键字实参为字典；名字可改，星号决定机制。输出含 `(100, 50)`、`{'knuts': 25}`，再是 `This-is-CS50!`。
调用处展开、定义处收集，方向不同。`print` 接收多个对象及 `sep/end` 等关键字，不表示任意函数都收任意关键字；固定接口仍宜使用明确命名参数。

## 9. map：把函数本身作为参数（yell.py）

```python
def yell(*words):
    uppercased = map(str.upper, words)
    print(*uppercased)


yell("This", "is", "CS50")
```

输出 `THIS IS CS50`。`map` 是内置类型，调用时接收可调用对象与可迭代数据，返回惰性迭代器；`str.upper` 不带括号，每次取值时才由 `map` 用当前字符串调用它。
这是把函数作为值传递的函数式思路，不是立即转换全部数据。`print(*uppercased)` 消费整个迭代器以展开实参；耗尽后不能从头再读。

## 10. 列表推导式：变换与筛选（gryffindors.py）

```python
words = ["This", "is", "CS50"]
uppercased = [word.upper() for word in words]
print(*uppercased)
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
]
names = [s["name"] for s in students if s["house"] == "Gryffindor"]
print(sorted(names))
```

列表推导式不是函数；求值时遍历输入、筛选并计算表达式，立即建立列表。读作“逐个学生，先判断学院，再取名字”，等价循环是条件成立才追加。
结果为 `['Harry', 'Hermione']`；原学生列表未变，`sorted` 返回新列表。推导式便于组合筛选与变换；规则长或有多步副作用时仍用普通循环。

## 11. filter 与 lambda：筛选原元素（filter_students.py）

```python
students = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
    {"name": "Hermione", "house": "Gryffindor"},
]
selected = filter(lambda s: s["house"] == "Gryffindor", students)
for student in sorted(selected, key=lambda s: s["name"]):
    print(student["name"])
```

`filter` 是内置类型，调用后返回惰性迭代器，取值时调用判断函数，保留真值对应的原元素，不自动取名字。`lambda s: ...` 是匿名函数表达式，创建返回冒号后表达式值的函数对象。
第一处 lambda 由 `filter` 判断学院，第二处由 `sorted` 取排序键，输出 Harry、Hermione。也可用普通 `def` 定义判断函数再传入函数名；复杂规则应起名。

## 12. 字典推导式与 enumerate（roster.py）

```python
students = ["Hermione", "Harry", "Ron"]
records = [{"name": name, "house": "Gryffindor"} for name in students]
houses = {name: "Gryffindor" for name in students}
print(records[0])
print(houses["Harry"])
for rank, name in enumerate(students, start=1):
    print(rank, name)
```

`records` 是字典组成的列表；`houses` 是字典推导式，冒号左右是键和值，立即建立映射。相同键的后值覆盖前值，不能盲目用姓名保存同名学生。
内置类型 `enumerate` 的调用返回迭代器，产生“计数、元素”二元组，由 `for` 解包。`start=1` 只改计数起点，不跳过元素或改变原索引，编号为 1、2、3。

## 13. 生成器、迭代器与 yield

官方数羊示例先拼完所有行再返回列表；`sleep.py` 用 ASCII 的 `sheep ` 避免字体差异，同时比较两种版本。规模保持很小，不用耗尽内存来验证：

```python
def sheep_list(n):
    flock = []
    for i in range(n):
        flock.append("sheep " * i)
    return flock


def sheep(n):
    print("Generator body starts")
    for i in range(n):
        yield "sheep " * i


print(sheep_list(3))
flock = sheep(3)
print("Generator created")
print(repr(next(flock)))
for row in flock:
    print(repr(row))
print(list(flock))
```

先输出列表与 `Generator created`，再输出 `Generator body starts`；首次 `next` 得空字符串，随后得到一只、两只羊的行，最后 `[]` 表示耗尽。内置 `repr` 返回可读表示，让空字符串和尾部空格可见。
含 `yield` 的 `def` 定义生成器函数；调用 `sheep(3)` 返回生成器对象，尚不进入函数体。`next(flock)` 开始或恢复函数，到 `yield` 交出值并暂停，保留局部变量和执行位置。
下次取值从暂停处继续，不从第一行重跑；`return` 则结束执行。函数体报错也可能延迟到取值时，“已创建”不等于全部计算成功。

可迭代对象能用 `iter` 取得迭代器，迭代器能用 `next` 逐项取值。生成器是一种迭代器；列表可迭代，但不能直接 `next`。
`for` 自动取迭代器并反复取值，遇 `StopIteration` 停止；手工对耗尽的迭代器取值会见到该异常。重新调用生成器函数创建新过程，`iter(flock)` 不会重置它。
生成器减少同时保存全部结果的需求，但每行仍分配随 i 增长的字符串，总字符量仍随 n 平方级增长；`list(sheep(n))` 又收集全部结果。
推导式立即收集，`map/filter` 延迟处理，生成器暂停自定义计算；惰性不是免费或永远更快。

## 周短片补充：递归

Week 9 另列 [Recursion 短片](https://cs50.harvard.edu/python/shorts/recursion/)，不同于生成器小节。`countdown.py` 给出机制对照，不混作 `yield` 原理：

```python
def countdown(n):
    if n <= 0:
        return
    print(n)
    countdown(n - 1)


countdown(3)
```

递归在执行中调用自己，依次打印 3、2、1，到基准条件返回并逐层结束；必须向停止条件靠近，且受调用深度限制，不能用无限递归代替循环。

## 自测、官方去向与全课收束

以下是讲义自测，不是官方作业题解：先追踪，再跟写，最后独立变更。
1. 运行 `houses.py`，再添加一个重复学院；说明为什么输出不增加，为什么还需要 `sorted`。
2. 删除 `bank.py` 中的 `global` 后预测错误位置；再恢复，解释读值与重新绑定的差别。
3. 独立把 `meows_cli.py` 增加一个字符串选项作为输出内容；验收默认值、三次重复、非法计数和帮助信息。
4. 不运行先写出数羊例子的输出顺序；再运行，分别说明“创建”“首次取值”“耗尽”时发生什么。
定位提示：类型问题看输入转换和返回契约；迭代问题看谁消费了数据，不能只看迭代器对象是否仍存在。

已核对 [Week 9](https://cs50.harvard.edu/python/weeks/9/) 指向 [Final Project](https://cs50.harvard.edu/python/project/)，没有单独的 Problem Set 9。主题是自行设计、测试并说明 Python 程序，含 `main` 和至少三个额外函数，为至少三个函数写 `pytest` 测试，细节见下一章及原页。
自测不是官方作业，读完也不等于通过课程。全课从函数与变量、条件、循环、异常、库、测试、文件、正则到类，本章将工具连起来，下一章再完成作品。

官方目录已覆盖：Et Cetera → set → Global Variables → Constants → Type Hints → Docstrings → argparse → Unpacking → args/kwargs → map → List Comprehensions → filter → Dictionary Comprehensions → enumerate → Generators and Iterators → Congratulations / This was CS50。周主题的 `mypy`、`print`、`yield` 与递归短片均保留；结语回顾十个单元。
四条理解标准：核心模型、解决的问题、替代方案、调用与结果。常见坑：把注解当强制；混淆收集与展开；重复消费迭代器；以为生成器免除全部计算成本。
补充依据：[Python 生成器教程](https://docs.python.org/3/tutorial/classes.html#generators)、[内置函数](https://docs.python.org/3/library/functions.html)、[mypy 入门](https://mypy.readthedocs.io/en/stable/getting_started.html)。本地 Python 3.13.15 已逐块运行 15 个示例；未运行 mypy 或安装依赖。

## 单元导航

[上一单元：08 面向对象编程](08_面向对象编程.md) · [课程目录](README.md) · [下一篇：最终项目](10_最终项目.md)
