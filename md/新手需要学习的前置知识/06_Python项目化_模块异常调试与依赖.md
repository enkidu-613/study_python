# 06. Python 项目化：模块、异常、调试与依赖

> **一句话理解：项目化就是把代码分文件、把第三方包隔离在虚拟环境中，并在出错时沿着 Traceback 定位真实位置。**

## 本章学什么，不学什么

学：模块导入、虚拟环境、第三方包、`try/except` 与 Traceback。

不学：复杂架构和线上部署；先让本地小项目稳定运行。

## 准确术语

| 术语 | 准确含义 |
| --- | --- |
| 模块 | 一个 `.py` 文件，可被另一个 Python 文件导入。 |
| import | 让当前文件使用其他模块公开的名字。 |
| 虚拟环境 | 为一个项目单独安装 Python 包的目录。 |
| 依赖 | 项目运行所需要的第三方包。 |
| 异常 | 程序运行中出现的可报告错误对象。 |
| Traceback | Python 从调用起点到出错位置的调用记录。 |

## 最小模板：拆成两个模块

`text_tools.py`：

```python
def normalize_text(text: str) -> str:
    return text.strip().lower()
```

`main.py`：

```python
from text_tools import normalize_text

raw_text = "  Hello AI  "
print(normalize_text(raw_text))
```

`from text_tools import normalize_text` 的意思是：从同目录模块 `text_tools.py` 导入函数对象 `normalize_text`，然后由 `main.py` 调用它。

## 最小模板：安全处理可预期错误

```python
try:
    age = int(input("请输入年龄："))
    print(f"明年你将 {age + 1} 岁")
except ValueError:
    print("请输入整数，例如 18")
```

`try` 运行可能失败的代码；若 `int(...)` 无法转换文本，它抛出 `ValueError`，`except ValueError` 处理这个具体情况。不要写空的 `except:` 把所有错误悄悄吞掉。

## 最小模板：建立虚拟环境

在项目目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests
python -m pip show requests
```

第一条创建 `.venv`；第二条激活它；后两条在该环境中安装并检查 `requests`。以后优先使用 `python -m pip`，确保包安装到当前 Python 对应的环境。

## Traceback 的阅读顺序

1. 先看最下面一行：异常类型和直接原因。
2. 找到最靠近自己项目文件的文件名与行号。
3. 复现一次，做最小修复，再运行验证。

## 常见坑

- 安装了包却仍然 `ModuleNotFoundError`：可能没有激活同一个 `.venv`。
- 文件命名为 `requests.py`：会遮住第三方 `requests` 包。
- 用 `except Exception: pass`：错误被藏起来，之后更难查。
- 只看报错第一行：真正原因通常在最后一行。

## 检查点

- [ ] 能说出模块、虚拟环境和依赖的分工。
- [ ] 能让 `main.py` 导入并调用另一个文件的函数。
- [ ] 能从 Traceback 中指出自己的文件名、行号和异常类型。
- [ ] 能创建并激活 `.venv`。

## 小练习

把上一章的 `format_task` 放进 `task_tools.py`，由 `main.py` 导入。再让用户输入完成状态；输入不是 `yes/no` 时抛出并处理一个 `ValueError`。

## 下一步

继续：[07. Git 与 GitHub：保存代码历史](07_Git与GitHub_保存代码历史.md)。
