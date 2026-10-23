# 15. Python 程序如何运行：源码、解释器与报错

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 0](https://cs50.harvard.edu/python/notes/0/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：你写的是源码文本；Python 解释器读取它、检查语法并在一个进程中执行。**
## 学什么，不学什么
学：源码、语法、解释器、进程、两类报错。 不学：解释器源码或性能优化。
## 术语
源码=`.py` 文本；语法=代码书写规则；解释器=执行 Python 的程序；进程=正在运行的程序实例。
## 最小模板
```python
message = "你好"
print(message)
```
运行时，Python 先检查代码能否按语法理解，再执行 `message = ...` 和 `print(...)`。漏写引号会得到 `SyntaxError`；变量拼错会在执行到那行得到 `NameError`。
## 常见坑
- 把语法错误当网络问题；先修代码形状。
- 把运行时错误当安装失败；先看 Traceback 指向哪一行。
- 以为解释器“理解业务”；它只按代码规则执行。
## 检查点
- [ ] 能区分 `SyntaxError` 与 `NameError`。
- [ ] 能说出 `python3 file.py` 启动了什么。
## 小练习
分别制造一次少引号和拼错变量名的错误，读最后一行后修复。
## 下一步
[08. Python 变量、类型与运算](08_Python变量_类型与运算.md)。
