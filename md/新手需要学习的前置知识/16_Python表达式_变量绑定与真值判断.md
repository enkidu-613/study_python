# 16. Python 表达式、变量绑定与真值判断

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 1](https://cs50.harvard.edu/python/notes/1/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：表达式会计算出值；Python 变量是名字绑定到对象，不是装数据的固定盒子。**
## 学什么，不学什么
学：表达式、赋值、返回值、`None`、真值和显式转换。 不学：指针、C++ 左右值。
## 术语
表达式=`1 + 2`；绑定=`name = value`；`None`=没有有意义的值；真值=条件中被当作真或假的结果。
## 最小模板
```python
value = 0
result = value or 10
print(result)
```
输出 `10`，因为 `0` 在条件中是假值。若只想在值是 `None` 时给默认值，应明确判断：
```python
result = 10 if value is None else value
```
## 常见坑
- 误以为 `0`、`""`、`[]` 与 `None` 相同。
- 用 `or` 提供默认值却意外覆盖 0。
- 以为函数没有 `return` 会返回空字符串；实际返回 `None`。
## 检查点
- [ ] 能解释两段代码为何输出不同。
## 小练习
写 `display_name = name if name else "游客"`，分别测试空文本和正常名字。
## 下一步
[09. 循环部分](09_Python条件_循环与输入.md#循环对多项数据重复处理)。
