# 12. Python 文件读写与异常处理

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 3](https://cs50.harvard.edu/python/notes/3/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：文件让数据留到下次运行；异常让程序能解释预期的错误。**
## 学什么，不学什么
学：`open`、`with`、`try/except`。不学：数据库。
## 术语
`with` 结束后自动关闭文件；`"w"` 写入并覆盖；`"r"` 读取；异常是运行时错误对象。
## 先学异常

按 CS50P 路线学习时，先完成本节，再学习 [13 模块](13_Python模块_虚拟环境与依赖.md) 和 [单元测试](CS50P_05_单元测试.md)，最后回来学文件。

```python
def parse_minutes(text: str) -> int:
    minutes = int(text)
    if minutes <= 0:
        raise ValueError("学习时长必须大于 0")
    return minutes


try:
    minutes = parse_minutes(input("学习分钟数："))
    print(minutes)
except ValueError as exc:
    print(f"请输入正整数：{exc}")
```

输入 `20` 时，`int` 返回整数，函数返回它；输入 `abc` 时，`int` 抛出 `ValueError`；输入 `0` 时，函数用 `raise` 主动抛出同类异常。两条错误路径都转到 `except`，没有继续执行 `try` 中的 `print(minutes)`。

`ValueError` 是内置异常类，用于值不符合要求的情况；`ValueError(...)` 创建异常实例，`raise` 中断正常执行并抛出它。`except ValueError as exc` 捕获匹配的异常，把实例绑定给 `exc`，便于输出说明。这里只处理知道怎样向用户解释的值错误。

## 再学文件

文件输入输出也叫 File I/O。`open` 是内置函数，返回文件对象；`with` 把它绑定给 `file`，在代码块退出时调用清理逻辑关闭文件，包括块内出现异常时。`file.write` 是文件对象的方法，接收要写入的字符串。

```python
with open("note.txt", "w", encoding="utf-8") as file:
    file.write("第一条学习笔记\n")

with open("note.txt", "r", encoding="utf-8") as file:
    text = file.read()
print(text)
```

相对路径相对于终端当前工作目录。先运行写入段，再单独运行读取段，应该仍能看到上一轮的文本。`with` 关闭的是文件资源，变量 `text` 不会因此消失。
## 常见坑
- `"w"` 会覆盖旧文件；练习用新文件名。
- 不指定 `utf-8` 可能造成中文乱码。
- 不写空 `except:`，只处理知道的异常类型。
## 检查点
- [ ] 能写入、关闭并重新打开 `note.txt`。
- [ ] 输入 `abc` 时程序不会崩溃而会显示提示。
## 小练习
把三条待办写进文本文件，再读出并打印。
## 下一步
只完成异常部分时，先读 [14. Traceback](14_调试Traceback与小项目整理.md)；完成文件部分时，进入 [CS50P 单元 7：正则表达式](CS50P_07_正则表达式.md)。
