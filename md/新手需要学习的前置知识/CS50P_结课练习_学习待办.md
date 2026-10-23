# Python 基础结课练习：学习待办

> 本地练习由 enkidu-613 围绕 CS50P 的学习主题自行设计，非 Harvard 官方问题集。课程参考：David J. Malan 与 CS50 团队，Harvard University，[CS50P](https://cs50.harvard.edu/python/)。按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与许可](CS50P_来源与许可.md)。

把前面的函数、条件、循环、异常、模块、测试、文件和类连成一个能重复运行的小程序。只使用本地 Python，不需要 API Key、模型、数据库或网页。

## 需求与文件

在自己的练习目录建立三个文件，文件名就是模块导入时使用的名称：

| 文件 | 职责 |
| --- | --- |
| `task_tools.py` | 校验与格式化函数、Task 类 |
| `main.py` | 接收输入，调用函数，显示和保存结果 |
| `test_task_tools.py` | 独立检查函数和实例行为 |

先只做标题清理，跑通之后再逐项加入下面的行为：

1. 输入任务编号、标题和分钟数，例如 `TASK-001`、`复习 Python`、`20`。
2. 清理标题两端空白，拒绝空标题；编号符合 `TASK-` 加三个 ASCII 数字；分钟数是正整数。
3. 创建两个 Task 实例，只完成其中一个；打印各自标题和完成状态。
4. 把标题写入练习用的 `tasks.txt`。本阶段允许用 `w` 每次覆盖；关闭后重新读取，显示保存结果。
5. 为正常标题、空标题、非法分钟数、错误编号及两个实例的独立状态写测试。

函数输入输出：标题函数接收 `str`，返回清理后的 `str`，不合法时抛 `ValueError`；分钟函数接收 `str`，返回正整数；编号函数接收 `str`，返回 `bool`。界面提示由 `main.py` 负责，校验函数里不写 `input()`。

## 运行与验收

激活自己的虚拟环境后，从三个文件所在目录执行：

```bash
python main.py
python -m pytest test_task_tools.py -q
```

本项目根目录的现成示例只供对照局部机制：

```bash
poetry run python -m pytest examples/python-basics-cs50p/test_task_tools.py -q
```

验收时实际输入一次合法数据，再分别输入空标题、`abc` 分钟数和错误编号；程序应显示对应提示，不把错误数据当成功结果。确认两个 Task 的状态独立，重新读到保存的标题，故意改错一条测试预期后能见到失败。

报错时先看最后一行的异常类型，再找到自己的文件与行号。导入失败先检查当前目录和文件名；测试通过但界面出错时，检查 `main.py` 有没有调用同一个校验函数。

以上是本项目 Python 基础的实践验收，不自动改写你已有学习进度。完成后从 [19. Git 安装与首次身份配置](19_Git安装与首次身份配置.md) 继续；想正式完成 CS50P 的 Final Project，应按 [官方要求](https://cs50.harvard.edu/python/project/) 另行准备和提交。
