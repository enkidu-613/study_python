# 09. Python 条件、循环与输入

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 1](https://cs50.harvard.edu/python/notes/1/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：条件选一条路，循环对多项数据重复同一动作。**
## 学什么，不学什么
学：`input`、`if/elif/else`、`for`、`while`。本章只练习执行分支和重复操作。
## 术语
`input()` 返回用户输入的字符串；`if` 判断真假；`for` 逐个取出列表项目；缩进表示代码块。
## 条件：根据输入选择输出
```python
name = input("名字：")
if name == "":
    print("请输入名字")
else:
    print(f"你好，{name}")
```

`input()` 先返回字符串，`name == ""` 得到布尔值；`if` 为真时执行提示，为假时执行 `else`。需要区分三个以上情况时，在两者之间加 `elif 条件:`，从上到下只执行第一个满足的分支。

## 循环：对多项数据重复处理

```python
for task in ["学习", "运行", "复习"]:
    print(task)

remaining = 3
while remaining > 0:
    print(remaining)
    remaining = remaining - 1
```

`for` 从列表中逐个取出字符串，每轮把当前字符串绑定给 `task`。`while` 每轮先检查条件；这里输出 `3`、`2`、`1`，随后 `remaining` 为 `0`，停止重复。删掉最后一行会使条件持续为真，程序不会自行结束；终端可用 Ctrl+C 中断。
## 常见坑
- `input()` 得到的是文本，数字计算前用 `int(...)` 转换。
- `=` 是赋值，`==` 是比较。
- `if` 和 `for` 内的代码必须统一缩进。
## 检查点
- [ ] 输入空名字会输出提示；输入名字会问候。
- [ ] 能解释循环中的 `task` 每轮是什么。
## 小练习
输入分数，输出“及格”或“复习”；再用循环打印三项待办。
## 下一步
条件部分之后学习 [16. 表达式与真值](16_Python表达式_变量绑定与真值判断.md)；完成循环部分后学习 [11. 列表、字典与集合](11_Python列表_字典与集合.md)。
