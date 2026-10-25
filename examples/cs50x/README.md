# CS50x Practice Environment

对应中文课程：[CS50x 目录](../../md/计算机基础/CS50x/README.md)。这里放你自己创建的课堂程序和练习；最初只提供说明，不预先放入官方作业解答。

从仓库根目录进入：

```bash
cd examples/cs50x
```

每段完整例子前都给文件名。两个都有 `main` 的 C 程序应各存一个文件，不能直接粘成同一程序。

## C

课程用 C 观察编译、数组、内存与结构，不把本项目后端改成 C。先检查是否已有编译器：

```bash
cc --version
```

按 01 章创建 `01_catalog.c` 后，在本目录运行：

```bash
cc -std=c11 -Wall -Wextra 01_catalog.c -o 01_catalog
./01_catalog
```

`cc` 是编译入口，`-o 01_catalog` 是输出名，`./01_catalog` 才执行当前目录的程序。本地例子使用标准库，不依赖 `cs50.h`；官方代码可能使用 `cs50.h`、`get_int` 或 `get_string`，它们需要课程库与工具环境，不能只复制导入行就认为电脑已有该库。

没有本机编译器或遇到系统许可/安装问题时，可先使用官方 [cs50.dev](https://cs50.dev/)，跟随原课的 `make`。其登录、网络与专用检查工具需你实际确认；本轮不要求为热身在电脑上另装整套工具链。上述本机命令适用于当前 macOS/Linux 有 C 编译器的情形，不声称在 Windows PowerShell 原样适用。

警告应读懂再处理。越界、释放后使用、未初始化访问属于错误示意时，讲义标成只读，不靠“我运行一次没崩”证明安全。动态内存例子可用受支持的 AddressSanitizer 额外检查，具体已验证范围见课程验收记录。

## Python 与 SQL

按 06 章创建 `catalog.py` 后，在当前项目环境中运行：

```bash
poetry run python catalog.py list
```

目标为 Python 3.12+。标准库示例无需安装新依赖；SQLite 可通过 Python `sqlite3` 模块练习，不要求另装数据库服务器。SQL 代码若依赖前面建表，按该章说明顺序执行，不直接对项目真实库操作。

## 网页

08 章单文件 HTML 可直接在浏览器打开。静态过滤不依赖后端；出现请求服务端的代码时，则必须先按后续章节启动相应服务。浏览器运行 JavaScript，Python/Flask 在服务端运行，两者不能混为同一个运行环境。

## Flask 独立环境

Flask 是第三方 Web 框架，当前项目主要使用 FastAPI；不要为这门课修改主项目的依赖清单或混装到全局 Python。

macOS/Linux 在本练习目录建立独立环境：

```bash
poetry run python -m venv .venv-flask
.venv-flask/bin/python -m pip install 'Flask>=3.1,<4'
```

Windows 可使用已安装的 Python 建环境，并使用相应路径：

```powershell
py -m venv .venv-flask
.venv-flask\Scripts\python.exe -m pip install "Flask>=3.1,<4"
```

这是版本范围，不承诺未来安装到相同补丁版本；验收记录会注明本次实际验证的版本。网络安装命令只在需要学习 Flask 时执行。

创建 09 章的应用和测试文件后，用这个环境运行它们，不再用指向主项目环境的 `poetry run python`。例如应用名为 `app.py` 时，macOS/Linux 用 `.venv-flask/bin/python app.py`；测试文件名按讲义选择。同一目录里的 `app.py` 仅是练习文件，不是仓库根目录的 `app/` 包。

密钥按章节通过环境变量设置，不放进代码、日志或 Git。课堂服务只监听 `127.0.0.1`；会话、表单和演示身份不等于生产认证系统，不直接公开部署。

## 不覆盖什么

这里的运行准备不等于正式课程注册或评阅。`check50`、`style50`、`submit50` 和题目专用文件按官方当期问题集说明使用，不在未配置时假定它们已安装。
