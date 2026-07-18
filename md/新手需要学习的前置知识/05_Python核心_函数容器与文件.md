# 05. Python 核心：函数、容器与文件

> **一句话理解：函数把重复步骤命名，list 保存有顺序的多个值，dict 用键找到对应值，文件让数据跨程序运行保存。**

## 本章学什么，不学什么

学：函数、参数、返回值、list、dict，以及 UTF-8 文本文件读写。

不学：模块拆分、依赖安装和异常处理；下一章处理它们。

## 准确术语

| 术语 | 准确含义 |
| --- | --- |
| 函数 | 可重复调用的一段代码。 |
| 参数 | 调用函数时交给它的输入值。 |
| 返回值 | 函数用 `return` 交回调用者的结果。 |
| list | 有顺序、可修改的多个值，例如待办列表。 |
| dict | 键和值的映射，例如 `{"name": "小明"}`。 |
| 编码 | 文本和字节互相转换的规则；本项目统一使用 UTF-8。 |

## 最小模板：把一件事做成函数

```python
def format_task(task_name: str, done: bool) -> str:
    mark = "✓" if done else "·"
    return f"{mark} {task_name}"


message = format_task("学习函数", False)
print(message)
```

`def` 定义函数，不会立刻运行函数体；`format_task(...)` 才是调用。`task_name` 与 `done` 是参数，`return` 的字符串回到 `message`。类型标注 `str`、`bool` 帮人和工具理解预期类型，Python 初学阶段不会强制它们。

## 最小模板：list 与 dict

```python
tasks = [
    {"title": "学习 Python", "done": True},
    {"title": "写小练习", "done": False},
]

for task in tasks:
    print(format_task(task["title"], task["done"]))
```

外层 `tasks` 是 list；每一个 `task` 是 dict。`task["title"]` 用键取到标题。

## 最小模板：保存与读取文本

```python
note = "今天运行了第一个 Python 程序。\n"

with open("study_note.txt", "w", encoding="utf-8") as file:
    file.write(note)

with open("study_note.txt", "r", encoding="utf-8") as file:
    saved_note = file.read()

print(saved_note)
```

`open` 返回文件对象；`with` 在代码块结束后自动关闭文件。`"w"` 是写入模式，会覆盖同名文件；`"r"` 是读取模式。

## 常见坑

- 忘记 `return`：函数会返回 `None`，而不是你以为的计算结果。
- 用不存在的 dict 键：`task["name"]` 会报错；先确认键名。
- 用 `"w"` 打开重要文件：它会覆盖旧内容；练习时使用新文件名。
- 把 list 下标和 dict 键混用：`items[0]` 是按位置，`user["name"]` 是按名称。

## 检查点

- [ ] 能区分定义函数和调用函数。
- [ ] 能说明 list 与 dict 各适合保存什么。
- [ ] 能用 `with open(..., encoding="utf-8")` 读取一个文本文件。

## 小练习

写 `tasks.py`：定义三个待办 dict，循环打印它们；把所有标题写入 `my_tasks.txt`。运行后打开文件确认内容正确。

## 下一步

继续：[06. Python 项目化：模块、异常、调试与依赖](06_Python项目化_模块异常调试与依赖.md)。
