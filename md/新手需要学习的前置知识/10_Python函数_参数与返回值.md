# 10. Python 函数、参数与返回值

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 0](https://cs50.harvard.edu/python/notes/0/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：函数把可重复步骤取一个名字；参数进来，返回值出去。**
## 学什么，不学什么
学：`def`、参数、`return`。不学：文件读写。
## 术语
函数=可调用代码块；参数=调用时输入；返回值=`return` 交回的结果。
## 最小模板
```python
def format_task(title: str, done: bool) -> str:
    mark = "✓" if done else "·"
    return f"{mark} {title}"

message = format_task("学习函数", False)
print(message)
```
`def` 只定义；`format_task(...)` 才调用。`return` 后面的字符串交给 `message`。
## 常见坑
- 忘记 `return`，结果是 `None`。
- 定义了函数却没调用。
- 参数顺序写反。
## 检查点
- [ ] 能指出参数、调用与返回值。
## 小练习
写 `is_passed(score)`，返回布尔值；用它判断两名学生。
## 下一步
[09. 条件部分](09_Python条件_循环与输入.md#条件根据输入选择输出)，再按 [CS50P 路线表](CS50P_Python基础学习路线.md) 补真值判断和循环。
