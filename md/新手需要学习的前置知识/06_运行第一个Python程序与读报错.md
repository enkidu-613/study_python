# 06. 运行第一个 Python 程序与读报错

> **一句话理解：运行程序是让解释器读取文件；报错先看最后一行、自己的文件名和行号。**

## 学什么，不学什么

学：运行 `hello.py`、读 `NameError`。  
不学：调试器；错误类型与捕获会在 CS50P 第 3 单元展开。

## 术语

| 术语 | 含义 |
| --- | --- |
| `print` | Python 内置函数，把值输出到终端。 |
| Traceback | 从运行起点到出错行的调用记录。 |
| `NameError` | 使用了尚未定义的名字。 |

## 最小模板

`hello.py`：

```python
print("你好，AI 应用开发！")
```

在项目目录运行：

| Windows PowerShell | macOS / Linux |
| --- | --- |
| `python hello.py` | `python3 hello.py` |

应看到同一句文字。把 `print` 故意写成 `prnit` 再运行；最后一行会出现 `NameError`，修回 `print` 后再验证。

## 常见坑

- 修改后没保存。
- 报错后只看英文第一行；先读最后一行和行号。
- 把终端命令输入进 Python 文件；命令与代码位置不同。

## 检查点

- [ ] 成功运行一次 `hello.py`。
- [ ] 故意制造并修复一次 `NameError`。

## 小练习

让程序打印三行：你的名字、目标、今天日期。

## 下一步

[CS50P 00. 函数与变量](CS50P/00_函数与变量.md) · [CS50P 课程目录](CS50P/README.md)
