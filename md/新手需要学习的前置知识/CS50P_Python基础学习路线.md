# 以 CS50P 为骨架的 Python 基础路线

> 原课程：David J. Malan 与 CS50 团队，Harvard University，[CS50P](https://cs50.harvard.edu/python/)。本项目由 enkidu-613 中文改编、重排并加入原创练习，按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[完整署名与范围](CS50P_来源与许可.md)。

先完成本目录 `00–06`，确认能在自己的电脑上运行 `.py` 文件。然后按下表学习；左列是 CS50P 的单元号，链接里的数字是本项目原有文件编号，两者不需要一致。

## 十个单元怎么接起来

贯穿练习是“学习待办”：先输出标题，再添加判断、批量处理、输入校验、函数拆分、测试和文件保存。每次只增加一个能力。

| CS50P 单元 / 官方笔记 | 本项目中文讲义与顺序 | 本地最低验收结果 |
| --- | --- | --- |
| [0. Functions, Variables：函数与变量](https://cs50.harvard.edu/python/notes/0/) | [07 输入处理输出](07_编程思维_输入处理输出.md) → [15 程序如何运行](15_Python程序如何运行_源码解释器与报错.md) → [08 变量与类型](08_Python变量_类型与运算.md) → [10 函数](10_Python函数_参数与返回值.md) | `format_task(title)` 返回整理后的标题；能区分 `return` 和 `print` |
| [1. Conditionals：条件](https://cs50.harvard.edu/python/notes/1/) | [09 的条件部分](09_Python条件_循环与输入.md#条件根据输入选择输出) → [16 表达式与真值](16_Python表达式_变量绑定与真值判断.md) | 空标题给提示，正常标题继续处理；能说出哪个分支执行 |
| [2. Loops：循环](https://cs50.harvard.edu/python/notes/2/) | [09 的循环部分](09_Python条件_循环与输入.md#循环对多项数据重复处理) → [11 容器](11_Python列表_字典与集合.md) | 用列表保存三项待办，逐项输出；解释循环变量每轮的值 |
| [3. Exceptions：异常](https://cs50.harvard.edu/python/notes/3/) | [12 的异常部分](12_Python文件读写与异常处理.md#先学异常) → [14 Traceback](14_调试Traceback与小项目整理.md) | 输入 `abc` 不会被当作学习时长；能定位最后一条异常及触发位置 |
| [4. Libraries：库](https://cs50.harvard.edu/python/notes/4/) | [13 模块与依赖](13_Python模块_虚拟环境与依赖.md) | 主文件从另一个模块导入标题处理函数，解释标准库与第三方库区别 |
| [5. Unit Tests：单元测试](https://cs50.harvard.edu/python/notes/5/) | [补充讲义：单元测试](CS50P_05_单元测试.md) | 正常、空白和非法输入分别有测试；故意写错预期会失败 |
| [6. File I/O：文件输入输出](https://cs50.harvard.edu/python/notes/6/) | [12 的文件部分](12_Python文件读写与异常处理.md#再学文件) | 保存待办标题后，关闭程序再读出；能解释 `with` 和写入模式 |
| [7. Regular Expressions：正则表达式](https://cs50.harvard.edu/python/notes/7/) | [补充讲义：正则表达式](CS50P_07_正则表达式.md) | 验证任务编号 `TASK-001`，并拒绝前后多余字符 |
| [8. Object-Oriented Programming：面向对象](https://cs50.harvard.edu/python/notes/8/) | [18 类与实例](18_Python类_对象与实例.md) | 创建两个 Task，只完成其中一个，另一个状态不变 |
| [9. Et Cetera：常用补充](https://cs50.harvard.edu/python/notes/9/) | [补充讲义：常用写法](CS50P_09_常用写法与阅读边界.md)；[17 Lambda 与闭包](17_Python函数进阶_Lambda与闭包.md) 按需补充 | 把普通循环改成列表推导式；解释类型注解不会自动转换输入 |

本地路线提取进入 AI 项目最常用的部分，**不是 CS50P 全部内容的等量替代**。文件 I/O 的 CSV、面向对象的属性与继承、Et Cetera 的命令行解析与生成器等进阶内容，可继续阅读各单元官方讲义；它们不全部成为本地入门阶段的通关要求。

## 每个单元怎么学

1. 先看讲义里的最小代码，预测一次输出。
2. 自己运行，逐步说清输入、调用和返回结果。
3. 改一个输入，观察行为；异常和测试单元还要主动触发一次失败。
4. 不看完整示例，完成表格右列的任务。会做的单元直接通过，不因更换课程骨架重新清零学习进度。

本地练习是项目自编任务。官方问题集、提交与评阅遵循 CS50P 自己的课程要求；本路线不提供官方作业的标准答案。

## 接回工程主线

完成 [Python 基础结课练习](CS50P_结课练习_学习待办.md)，再从 [19. Git 安装](19_Git安装与首次身份配置.md) 开始，继续 `19–27`。主目录 `md/01–03` 可在进入项目后作为复习和进阶参考；不用把相同语法再完整学一遍。
