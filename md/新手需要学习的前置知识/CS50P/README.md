# CS50P：Python 编程入门中文讲义

原课程是 David J. Malan 与 CS50 团队（Harvard University）的 **CS50’s Introduction to Programming with Python**。本目录由 enkidu-613 按官方讲义的单元顺序、知识范围与问题集入口编写中文改编讲义，作为本项目的 Python 入门课程。[原课程](https://cs50.harvard.edu/python/) · [来源与 CC BY-NC-SA 4.0 许可](来源与许可.md)。

这是非官方中文改编，不是逐字翻译或 Harvard 官方中文版。课堂例子用于理解机制，正式作业使用官方问题集；问题集的具体要求、评阅与提交始终以链接中的官方页面为准。

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

这次课程更换将以前拆开的 Python 文件统一为上述顺序。你只需要从 0 往后读，不再对照原来的 `07–18` 编号。

## 开始前准备到哪里

会创建 `.py` 文件、打开终端、切换到文件所在目录并运行 Python，即可开始第 0 单元。需要补这些动作时，先读上一级的 [01–06 环境准备](../README.md)。

已在当前项目用 Poetry 的学习者，可以用 `poetry run python 文件名.py` 运行自己的练习；在独立练习目录使用已激活的虚拟环境时，用 `python 文件名.py`。后者是讲义中的默认写法，切勿在同一练习里混用不同 Python 环境安装依赖。终端命令放在终端执行，Python 代码放进 `.py` 文件。

每个单元的课堂实验先运行，再改输入观察，再独立重写。每个例子前给出的文件名只适用于当前例子；新建独立练习目录可避免课程里反复使用的 `hello.py`、`student.py` 等覆盖你之前的练习。

## 自学与正式提交

按官方“Lecture → Shorts（建议）→ Problem Set”的路线练习。中文讲义帮助理解官方材料，既有学习进度保留；这次热身不会自动将任何单元标为完成。

如果只是热身，可以按自己的节奏使用课堂练习。若注册并向 CS50P 正式提交问题集或最终项目，应遵守[课程的学术诚信规则](https://cs50.harvard.edu/python/honesty/)；该规则对 AI 辅助和作业答案有明确要求。这里提供概念与课堂示例，不提供官方问题集的成品答案。

## 完成后去哪

本次热身之后，按新的[计算机基础路线](../../计算机基础/README.md)进入 CS50x，再做系统、网络和数据库等补充实验。它们是另一个阶段，不属于 CS50P 的课程完成要求。

上一级 [19. Git 安装与首次身份配置](../19_Git安装与首次身份配置.md)至 27 篇仍是工程衔接参考；已会的 Git、HTTP、SQL 可以查缺补漏，不必重复从头学习。
