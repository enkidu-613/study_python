# 11. Python 列表、字典与集合

> 课程主题参考：David J. Malan 与 CS50 团队（Harvard University）的 [CS50P 单元 2](https://cs50.harvard.edu/python/notes/2/)。enkidu-613 将本项目中文讲义纳入该主题路线并加入项目练习，非官方译本；本页按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 分享。[来源与改编说明](CS50P_来源与许可.md) · [本课程阅读顺序](CS50P_Python基础学习路线.md)。

> **一句话理解：list 保顺序，dict 按名字取值，set 判断是否出现过。**
## 学什么，不学什么
学：三种容器的选择。 不学：性能公式。
## 术语
list=`["a", "b"]`；dict=`{"name": "小明"}`；set=`{"a", "b"}`，set 不保留重复值。
## 最小模板
```python
tasks = [{"title": "学习", "done": False}]
seen = {"学习"}
print(tasks[0]["title"])
print("学习" in seen)
```
## 常见坑
- `tasks[0]` 是按位置；`task["title"]` 是按键。
- dict 键不存在会报错，必要时用 `get`。
- set 会自动去重，不适合保留重复记录。
## 检查点
- [ ] 能为“按用户 ID 找用户”选择 dict。
- [ ] 能为“已出现问题”选择 set。
## 小练习
建立三个待办 dict，用循环打印它们的标题。
## 下一步
[12. Python 文件读写与异常处理](12_Python文件读写与异常处理.md)
