# CS50P：Python 编程入门中文讲义

原课程是 David J. Malan 与 CS50 团队（Harvard University）的 **CS50’s Introduction to Programming with Python**。本目录由 enkidu-613 按官方讲义的单元顺序、知识范围与问题集入口编写中文改编讲义，作为本项目的 Python 入门课程。[原课程](https://cs50.harvard.edu/python/) · [来源与 CC BY-NC-SA 4.0 许可](来源与许可.md)。

这是非官方中文改编，不是逐字翻译或 Harvard 官方中文版。课堂例子用于理解机制，正式作业使用官方问题集；问题集的具体要求、评阅与提交始终以链接中的官方页面为准。

**本目录是一套独立的 Python 入门课程。** 从下面的环境准备，到第 0–9 单元和最终项目，按本目录就能开始学习；不需要先学习 Git、FastAPI、AI 应用或本仓库其他章节，也不要求使用 Poetry。练习代码统一放在仓库的 `examples/cs50p/`，课程环境与主应用依赖分开。

## 按这个顺序学习

| 单元 | 中文讲义 | 官方讲义 | 官方作业 |
| --- | --- | --- | --- |
| 0 | [函数与变量](00_函数与变量.md) | [Functions, Variables](https://cs50.harvard.edu/python/notes/0/) | [Problem Set 0](https://cs50.harvard.edu/python/psets/0/) |
| 1 | [条件判断](01_条件判断.md) | [Conditionals](https://cs50.harvard.edu/python/notes/1/) | [Problem Set 1](https://cs50.harvard.edu/python/psets/1/) |
| 2 | [循环](02_循环.md) | [Loops](https://cs50.harvard.edu/python/notes/2/) | [Problem Set 2](https://cs50.harvard.edu/python/psets/2/) |
| 3 | [异常](03_异常.md) | [Exceptions](https://cs50.harvard.edu/python/notes/3/) | [Problem Set 3](https://cs50.harvard.edu/python/psets/3/) |
| 4 | [库与模块](04_库与模块.md) | [Libraries](https://cs50.harvard.edu/python/notes/4/) | [Problem Set 4](https://cs50.harvard.edu/python/psets/4/) |
| 5 | [单元测试](05_单元测试.md) | [Unit Tests](https://cs50.harvard.edu/python/notes/5/) | [Problem Set 5](https://cs50.harvard.edu/python/psets/5/) |
| 6 | [文件输入输出](06_文件输入输出.md) | [File I/O](https://cs50.harvard.edu/python/notes/6/) | [Problem Set 6](https://cs50.harvard.edu/python/psets/6/) |
| 7 | [正则表达式](07_正则表达式.md) | [Regular Expressions](https://cs50.harvard.edu/python/notes/7/) | [Problem Set 7](https://cs50.harvard.edu/python/psets/7/) |
| 8 | [面向对象编程](08_面向对象编程.md) | [Object-Oriented Programming](https://cs50.harvard.edu/python/notes/8/) | [Problem Set 8](https://cs50.harvard.edu/python/psets/8/) |
| 9 | [更多 Python 特性](09_更多Python特性.md) | [Et Cetera](https://cs50.harvard.edu/python/notes/9/) | 本单元进入最终项目，没有另设 Problem Set 9 |
| 最终项目 | [项目要求与准备](10_最终项目.md) | [Final Project](https://cs50.harvard.edu/python/project/) | 按官方要求自行实现 |

官方单元从 0 编号，所以第一篇是“第 0 单元：函数与变量”，不是第 1 单元的条件判断。按表从上往下学，不必对照本仓库其他课程编号。下面的环境准备是本地讲义的使用说明，不是另加一个官方单元。

## 开始前准备

已经能在自己的 Python 环境中创建并运行 `.py` 文件，可以直接进入[第 0 单元](00_函数与变量.md)。还不熟悉时，按以下步骤做一次即可，不用先读另一套环境课程。

### 1. 确认 Python

准备一个代码编辑器和终端即可。编辑器用来创建、修改、保存文件；终端用来执行命令、输入数据和查看结果，不是同一个输入位置。macOS 可打开“终端”，Windows 可打开 PowerShell；编辑器自带的终端也可以使用。不指定必须使用哪个编辑器。

本地讲义建议 Python 3.12 或更新的稳定版本；这是本讲义的运行建议，不是对官方课程额外规定。需要安装时使用 [Python 官方下载入口](https://www.python.org/downloads/)，选择对应操作系统的稳定版并按安装器说明操作，完成后重新打开终端。不为了第一节课安装数据库、Node.js 或其他框架。

macOS / Linux 在终端检查：

```bash
python3 --version
```

Windows PowerShell 检查：

```powershell
py --version
```

应显示 `Python 3.x.x`。Windows 若没有 `py`，但 `python --version` 可用，后面的 `py -m venv` 可以相应改成 `python -m venv`。两者都找不到时，先完成 Python 安装，不要把“命令不存在”当成程序语法错误。

### 2. 建立项目内练习环境

先在编辑器中打开本项目的仓库根目录，再打开终端。下面的命令都从仓库根目录运行；若已经在 `examples/cs50p/`，不要重复创建目录，直接进入该目录并创建环境即可。练习代码放在 `examples/cs50p/`，不放在用户主目录，也不放进主应用的 `app/`。

macOS / Linux：

```bash
mkdir -p examples/cs50p
cd examples/cs50p
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force examples/cs50p | Out-Null
Set-Location examples/cs50p
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

`mkdir` / `New-Item` 建目录，`cd` / `Set-Location` 切换当前工作目录。`venv` 是 Python 标准库模块，`-m venv .venv` 让它在 `.venv` 中创建一个包环境；激活命令只让当前终端优先使用它的解释器。它不安装第三方课程依赖，不是操作系统安全沙箱，也不替你保存代码。练习文件放在 `examples/cs50p/`，不要放进 `.venv`。仓库的 `.gitignore` 已忽略 `.venv/`，不会把环境里的文件提交进 Git。

Windows 若限制执行激活脚本，不必修改执行策略或申请管理员权限。在练习目录直接运行 `.\.venv\Scripts\python.exe --version`；后续把命令开头的 `python` 换成 `.\.venv\Scripts\python.exe` 即可，例如 `.\.venv\Scripts\python.exe hello.py`。macOS / Linux 不激活时同样可直接用 `.venv/bin/python hello.py`。

进入环境后，再检查一次实际解释器：

```bash
python -c "import sys; print(sys.executable)"
```

路径应指向当前练习目录的 `.venv`。这个 `-c` 命令只用于确认环境：它让解释器直接执行一小段检查代码；`sys` 是随 Python 提供的模块，正式的模块使用会在第 4 单元展开。环境创建与激活的依据见 [Python venv 官方文档](https://docs.python.org/3.13/library/venv.html)。

### 3. 创建并运行第一个文件

用编辑器打开 `examples/cs50p/`，新建 `hello.py`，写入下面这一行并保存。文件后缀是 `.py`，不是 `.py.txt`；代码不要写到终端的命令提示符后。

```python
print("hello, world")
```

回到终端，确认当前仍在 `examples/cs50p/`，执行：

```bash
python hello.py
```

预期显示一行：

```text
hello, world
```

`python` 是运行程序的解释器，`hello.py` 是要执行的文件名。相对文件名从终端的当前工作目录查找，不是从讲义所在目录查找。macOS / Linux 用 `pwd` 看当前位置、`ls` 看文件；PowerShell 对应使用 `Get-Location` 和 `Get-ChildItem`。

终端若显示 `>>>`，说明进入了 Python 交互模式：输入 `exit()` 回到终端，再执行 `python hello.py`。不要把 `>>>` 或终端提示符复制进文件。

### 4. 再次打开终端

新终端中先在编辑器打开本项目，再打开它的终端，并确认终端当前位置是仓库根目录；然后进入练习目录并激活环境，不用重新创建 `.venv`。macOS / Linux：

```bash
cd examples/cs50p
source .venv/bin/activate
python hello.py
```

Windows PowerShell：

```powershell
Set-Location examples/cs50p
.\.venv\Scripts\Activate.ps1
python hello.py
```

不能激活时，继续使用上面的解释器完整相对路径。练习结束可在已激活的终端执行 `deactivate`，退出包环境；它不会删除代码或卸载 Python。不要用删除练习目录的方式“退出环境”。

### 5. 读懂最小报错

先看错误末尾，再看指出的文件和行号；根据类别查一件事：

| 现象 | 先检查什么 |
| --- | --- |
| `command not found` / 无法识别命令 | Python 是否安装；当前使用的是 `python3`、`py` 还是激活后的 `python` |
| `can't open file` / `No such file or directory` | 当前目录、文件是否保存、文件名及 `.py` 后缀 |
| `SyntaxError` | 报错行附近的引号、括号、冒号；真正漏写的位置可能在上一行 |
| `NameError` | 名字是否拼错，使用前是否已经赋值或定义 |
| `ModuleNotFoundError` | 先确认所选解释器；第 4 单元起再按对应章节检查包安装或同目录模块 |

故意把 `hello.py` 的右括号漏掉一次，运行并观察 `SyntaxError` 指向哪里，再补回、保存、重跑。这里先会辨认和定位，不要求提前学 `try/except`；异常处理在第 3 单元讲。若出现权限错误，先确认本机授权，不提权绕过，也不把密码发给别人排错。

### 依赖安装边界

即使练习代码放在本仓库中，也使用 `examples/cs50p/.venv`，不要用仓库根目录的 `poetry run` 或向主应用的 `pyproject.toml` 添加 CS50P 练习依赖。后续讲义中的 `python -m pip install ...` 在激活练习环境后执行；第 0–3 单元只用内置功能和标准库，不需要提前安装课程后半部分的包。

## 每个单元怎样练习

每个单元先运行课堂例子，再改输入观察，最后独立重写。前置知识应来自本目录已经学过的单元；只在后续提及的内容会明确标注，不要求跳到 AI 或后端课程补齐。

每个例子给出的文件名只适用于当前实验。同一文件的多个版本应替换运行，不要把多个完整程序直接拼在一起；先保存旧版本，避免覆盖自己的成果。进入下一单元时可在 `examples/cs50p/` 下新建 `unit00`、`unit01` 等子目录，并切到该目录运行；`.venv` 继续复用 `examples/cs50p/` 根目录那一个。多文件例子应按讲义放在同一个实验目录。

第 4 单元才开始按需安装第三方库，第 5 单元增加 pytest，第 6 单元按图像例子需要安装 Pillow，第 9 单元的 mypy 按讲义说明使用；不用在开课前全部安装。包安装、外网 API、官方判题和图像输入各有自己的条件，能运行第 0 单元不代表这些后续条件已经验证。

## 自学与正式提交

按官方“Lecture → Shorts（建议）→ Problem Set”的路线练习。中文讲义帮助理解官方材料，既有学习进度保留；这次热身不会自动将任何单元标为完成。

如果只是热身，可以按自己的节奏使用课堂练习。若注册并向 CS50P 正式提交问题集或最终项目，应遵守[课程的学术诚信规则](https://cs50.harvard.edu/python/honesty/)；该规则对 AI 辅助和作业答案有明确要求。这里提供概念与课堂示例，不提供官方问题集的成品答案。

后续课程仅在[最终项目的结课说明](10_最终项目.md#结课后的可选方向)提供入口，不作为本课前置或额外完成要求。

开始：[第 0 单元：函数与变量](00_函数与变量.md)。
