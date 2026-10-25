# 02. 开发工具：终端、Git 与排错

> **一句话理解：程序出问题时，先确认“在哪运行、用谁运行、输出了什么、以什么状态结束”，再读代码和变更。**

## 本章范围

本章沿用已经见过的 Python 变量、列表、字典、循环、函数、异常和 `print`。新出现的终端概念、`subprocess` 标准库和进程结果对象会在这里从代码形状讲起。

学：当前工作目录、解释器、运行环境、退出状态、标准输出与错误输出；安全地看 Git 状态、差异和历史；按顺序定位报错。

不学：Shell 脚本、管道重定向、虚拟环境如何创建、Git 分支合并/回退、调试器和性能测量。第 04 章先用执行步骤计数比较算法，不承诺完成真实性能分析；旧的 Git 安装、提交和 GitHub 操作见前置知识第 19–23 篇，那里是查表复习，本篇不重讲完整流程。

## 先看真实问题

假设知识文档程序说“找不到 `documents.json`”，但文件明明在项目里。原因可能不是文件消失，而是程序从另一个目录启动；也可能运行它的 Python 不是你以为的那个。另一个常见现场是程序打印了结果，同时报告失败：结果和错误本来就可以走不同输出通道，程序也会以非零状态结束。

先把运行现场拆成四个问题：

| 要确认什么 | 人话解释 | 本章观察方式 |
| --- | --- | --- |
| 当前工作目录（current working directory） | 程序把相对路径当作从哪里开始 | Python 的 `Path.cwd()` |
| 解释器（interpreter） | 哪个 Python 程序正在执行代码 | `sys.executable` |
| 标准输出与标准错误 | 正常结果和诊断信息分别写到哪里 | `stdout`、`stderr` |
| 退出状态（exit status） | 程序结束时给启动者的结果编号 | `returncode`，通常 0 表示成功 |

这四项能把“它在我电脑上明明可以”变成可核对的信息。它们不是程序正确性的全部证明，但能先排除大量环境和路径问题。

## 当前目录、解释器与环境

相对路径如 `examples/cs-foundations/02_terminal_git.py` 不自带电脑上的起点。它从**当前工作目录**开始解释。当前工作目录不是“这个 `.py` 文件所在目录”，而是启动程序的终端当时所在的目录。

在仓库根目录执行：

```bash
cd /Users/enkidu/PyCharmMiscProject
poetry run python -c "from pathlib import Path; import sys; print(Path.cwd()); print(sys.executable)"
```

第一行输出应为仓库根目录；第二行是 Poetry 环境实际使用的 Python 可执行文件路径。Poetry 已是本项目的环境入口，不需要为本章另装工具。接下来始终从仓库根目录进入练习目录：

`pathlib` 是处理文件路径的 Python 标准库；从中导入的 `Path` 是路径类。`Path.cwd()` 是取得当前工作目录的类方法，返回一个路径对象；`print` 把它显示为路径文本。`sys` 同样来自标准库，提供当前解释器等运行信息，不需要另外安装。

```bash
cd /Users/enkidu/PyCharmMiscProject/examples/cs-foundations
poetry run python 02_terminal_git.py
```

若你已经在独立 Python 环境中激活了解释器，也可以在同一目录运行 `python 02_terminal_git.py`。两种方式都在运行代码；`poetry run` 的额外价值是让项目声明的环境来启动它。不要只凭命令里出现了 `python` 就假设版本或环境相同。

### 带空格的路径

终端会把空格当作参数之间的分隔。路径 `my notes/summary.txt` 若不加引号，容易被拆成两个参数。把整个路径用一对引号括起来：

以下是路径写法示意，不是你电脑上已经存在的目录，不能原样执行：

```text
cd "/Users/enkidu/My Projects/PyCharmMiscProject/examples/cs-foundations"
```

引号属于 Shell 的写法。若路径来自代码，交给 Python 的路径对象处理，不要自己拼一整条 Shell 命令。本章的子进程实验会用参数列表，从而避免 Shell 再次拆分参数。

## 一个可运行的排错实验

以下程序只查看自身运行现场，并启动一个很小的 Python 子进程；它不改文件、不访问网络、不连接数据库。请把完整代码保存为 `examples/cs-foundations/02_terminal_git.py`。

```python
from pathlib import Path
import subprocess
import sys


print("当前工作目录:", Path.cwd())
print("当前解释器:", sys.executable)

child_code = (
    "import sys; "
    "print('子进程的正常结果'); "
    "print('子进程的诊断信息', file=sys.stderr); "
    "sys.exit(3)"
)

result = subprocess.run(
    [sys.executable, "-c", child_code],
    capture_output=True,
    text=True,
    check=False,
)

print("退出状态:", result.returncode)
print("标准输出:", repr(result.stdout))
print("标准错误:", repr(result.stderr))
```

从仓库根目录执行：

```bash
cd /Users/enkidu/PyCharmMiscProject/examples/cs-foundations
poetry run python 02_terminal_git.py
```

输出前两行的路径会因本机安装位置不同而不同；后三行应精确为：

```text
退出状态: 3
标准输出: '子进程的正常结果\n'
标准错误: '子进程的诊断信息\n'
```

### 逐步追踪调用

1. `sys.executable` 是 Python 标准库 `sys` 提供的属性，给出当前解释器的路径。父程序把它放在参数列表第一个位置，因此子程序由同一个 Python 解释器启动。
2. `subprocess` 是 Python 标准库，用来从 Python 启动并管理另一个进程。本例从其中调用函数 `subprocess.run(...)`；调用者是当前脚本，输入是“程序及参数”的列表，调用会等子进程结束，再返回一个 `CompletedProcess` 实例。
3. `-c` 告诉 Python 把下一个字符串当作代码运行。子代码先向标准输出打印，再把一行写到标准错误，最后 `sys.exit(3)` 以状态 3 结束。
4. `capture_output=True` 要求 `run` 收集两个输出流；`text=True` 让收集结果成为字符串，而不是字节；`check=False` 表示即使退出状态非零，也不因此抛出异常。
5. 返回值 `result` 是 `subprocess.CompletedProcess` 类的实例。`returncode` 是退出状态；`stdout` 与 `stderr` 是收集到的两段文本。`repr` 会把换行显示成 `\n`，所以可以清楚看见末尾换行。

`check` 参数的边界：设为 `True` 时，非零状态会使 `run` 抛出 `subprocess.CalledProcessError`，调用者不再正常拿到返回结果；设为 `False` 时，代码继续运行，由调用者自行检查 `result.returncode`。本实验刻意使用 `False`，让失败状态成为可观察数据，而不是让整段演示提前中断。

## 退出状态与两种输出

终端里看到的“打印内容”和命令结束状态是两回事。惯例上状态 `0` 表示命令成功完成，非零表示某种失败或特殊情况；非零具体代表什么，必须看该程序的约定。它不一定是 Python 异常编号，也不一定只有 `1`。

标准输出（stdout）通常放程序的正常结果；标准错误（stderr）通常放诊断信息，例如报错。它们是两个输出通道，不是“一个给用户、一个给开发者”的强制规则。程序可以不输出任何内容仍成功，也可以输出了部分结果后失败。

本实验的安全失败状态是 `3`。它不是异常演练：子程序明确调用 `sys.exit(3)`，父程序仍拿到退出状态、正常输出和错误输出。因为代码只启动当前 Python 并执行写在字符串中的短代码，不会删除或覆盖文件。

## 读报错：从最后一行往上找

Python 的 traceback（回溯信息）会给出调用经过。先看最末尾的异常类型和说明，再往上找到**最靠近自己代码**的文件名、行号和代码行；它们通常告诉你错误是什么，以及你的哪一行触发了它。

例如：

```text
Traceback (most recent call last):
  File "examples/cs-foundations/read_docs.py", line 12, in <module>
    print(document["owner"])
KeyError: 'owner'
```

最末行说字典里没有键 `owner`。回到第 12 行，检查实际数据的键名；本课程文档数据使用的是 `owner_id`。不要把完整回溯里最上面的库内部文件当成首要修复位置，也不要因为堆栈很长就跳过末尾。

排查顺序可以固定为：

1. 读最末尾的异常名称和说明，判断是路径、键、类型还是别的问题。
2. 往上找到自己项目中最近的一行，核对变量的实际值和这一行的输入。
3. 确认当前目录与解释器；若由另一个程序启动，核对那个程序的工作目录和环境。
4. 再看 stdout、stderr 和退出状态，避免把“显示了文字”误当成“程序成功”。

## Git：先看清，再决定

Git 是记录项目文件变化的版本控制工具。前置知识第 20 篇已教过仓库、工作区、暂存和提交；这里不重复提交流程，只练安全阅读。三个只读观察入口：

```bash
git status --short
git diff
git log -5 --oneline
```

- `git status --short` 简要列出哪些文件有改动、哪些尚未被 Git 跟踪。它是现状摘要，不会替你判断改动好坏。
- `git diff` 查看尚未暂存的文本改动，通常以 `-` 显示旧行、`+` 显示新行。若结果为空，可能没有未暂存差异，也可能改动已经暂存；再看 `git status`。
- `git log -5 --oneline` 阅读最近五条提交的简短记录，不会切换版本或改动文件。

只查看已暂存的差异可用 `git diff --cached`。本章把命令限制在读取状态、差异和历史：不执行 `git add`、`git commit`、`git restore`、`git reset` 或删除命令。看到陌生文件时先停下来核对，不要为了让状态“变干净”而清除它。

Git 能回答“文件相对某个版本改了什么”，不能证明代码运行正确；运行测试也不能替代读差异。排错时把两种证据放在一起看：当前代码如何变化，以及它实际输出了什么。

## 跟写：给子进程换一个状态

保留主实验其余内容，只把子代码字符串中的 `sys.exit(3)` 改为 `sys.exit(0)`，再运行一次。预测三项变化：退出状态、标准输出、标准错误。验收：退出状态变为 `0`；两段输出仍保留原内容。若输出也变化，检查你改动的位置是否只影响最后的退出状态。

再把 `check=False` 改为 `check=True` 是一个**只观察、不运行**的代码形状预览：在原来的非零子进程下，`run` 会抛出 `CalledProcessError`，因此后面的 `print("退出状态"...)` 不会执行。恢复 `check=False` 再运行。这个切换帮助你识别异常边界，不要求本章掌握异常捕获设计。

## 独立练习：查清一份报告

需求：写一个自含程序，启动同一解释器执行一段短代码；子程序把 `文档数=3` 写入正常输出，并以状态 `2` 结束。父程序必须分别显示工作目录、解释器路径、状态、stdout、stderr，并在状态非零时打印一句“子程序未成功”。

约束：只使用本章代码中已出现的标准库与参数；不能使用 Shell 字符串启动子程序，不读写仓库业务数据，不联网。保存为 `examples/cs-foundations/02_independent_report.py`，从该目录运行：

```bash
poetry run python 02_independent_report.py
```

验收：`returncode` 为 `2`；stdout 精确为一行 `文档数=3`（检查时允许末尾换行）；stderr 为空字符串；目录和解释器路径都能显示；状态提示出现一次。若结果不符，先检查参数列表、`capture_output`、`text` 和状态判断。

## 本章小结

- 相对路径从当前工作目录出发；`sys.executable` 让你看见正在用的 Python。
- 子进程的 `stdout`、`stderr` 与 `returncode` 是三项独立证据；`check` 决定非零状态是否转成异常。
- 报错先读末尾，再回到最近的自己代码；Git 先读 `status`、`diff`、`log`，本章不做更改或提交。
- 下一章会沿用“先确认数据长什么样、再决定怎么查”的做法，把固定的三份知识文档放进合适的数据结构。

## 四条理解检查

- [ ] 当前目录与 `.py` 文件所在目录有什么区别？相对路径从哪里开始？
- [ ] 解释器路径、stdout、stderr、退出状态各自能回答什么问题？
- [ ] `subprocess.run` 返回什么？`check=False` 与 `check=True` 在非零状态时有何差异？
- [ ] 如何只读地查看工作区现状、未暂存改动和最近历史？为什么它们不等于运行验证？

## 前后导航

- 上一篇：[01. CS50x 计算机科学入门](01_CS50x_计算机科学入门.md)
- 下一篇：[03. 数据结构：文档怎么存、怎么找](03_数据结构_文档怎么存怎么找.md)

## 参考资料

- [The Missing Semester 2026：课程总览与主题](https://missing.csail.mit.edu/2026/)；[命令行环境](https://missing.csail.mit.edu/2026/command-line-environment/)；[调试与性能分析](https://missing.csail.mit.edu/2026/debugging-profiling/)；[版本控制与 Git](https://missing.csail.mit.edu/2026/version-control/)。本章选取 Shell 环境、错误诊断和只读 Git 查看作为方向，不把整门课的工具清单塞进来。
- [Python 3.12 `subprocess` 官方文档](https://docs.python.org/3.12/library/subprocess.html)：`run`、`capture_output`、`text`、`check`、`CompletedProcess`、`returncode`、stdout/stderr 的行为。
- [Python 3.12 `sys` 官方文档](https://docs.python.org/3.12/library/sys.html)：`sys.executable` 与 `sys.exit`。

本篇不是 MIT 官方课程译本；上面来源用于核对事实与延伸阅读。
