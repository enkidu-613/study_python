# 14. 调试 Traceback 与小项目整理

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 3](https://cs50.harvard.edu/python/notes/3/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：调试不是猜；先复现，再读最后一行异常和自己文件的行号。**
## 学什么，不学什么
学：Traceback、最小修复、项目目录。 不学：复杂断点工具。
## 术语
Traceback=调用记录；异常类型=错误类别；复现=用同样步骤再次触发问题。
## 最小模板
```text
ai-beginner/
├── main.py
├── text_tools.py
├── note.txt
└── .venv/
```
看到报错后：1) 看最末行；2) 找自己的文件和行号；3) 只改那一处；4) 重跑。
## 常见坑
- 看到报错就同时改很多行。
- 搜索报错前没读行号。
- 把 `.venv` 当作自己写的代码修改。
## 检查点
- [ ] 能解释 `ModuleNotFoundError` 和 `NameError` 分别表示什么。
- [ ] 能整理出上面的项目目录。
## 小练习
故意把 `normalize` 拼错，按四步定位并修复。
## 下一步
[13. Python 模块、虚拟环境与依赖](13_Python模块_虚拟环境与依赖.md)。
