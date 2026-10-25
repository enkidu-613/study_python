# CS50x 计算机科学入门：中文改编讲义

原课程为 David J. Malan 与 CS50 团队、Harvard University 的 [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/)。这里按官方主课主题编写中文讲义，不是逐字译本或官方中文版；改编与补充内容、署名和 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 范围见[来源与许可](来源与许可.md)。核对日期：2026-10-25。

与上一级原有的学习指引不同，本目录提供分单元正文和课堂实验。讲义帮助你理解机制；正式问题集、题目限制、评阅、提交和课程完成条件仍以官方为准。课堂代码不是官方问题集的成品答案。

## 从哪里开始

你已经会用 Python，可以把它当作对照，但不要跳过 C：C 的数组、地址和内存管理正是本轮补基础的重要内容。遇到新语法，先跑小例子、看变量如何变化，再记准确名称，不要求一次记完所有符号。

先读[环境与练习说明](../../../examples/cs50x/README.md)。各章完整程序放在同一个练习目录；示例文件名属于当前实验，运行前确认自己创建了哪个文件，别把几段各有 `main` 的程序拼在一起。

## 学习顺序

| 顺序 | 中文正文 | 官方主题与资料 |
| --- | --- | --- |
| 00 | [计算思维与 Scratch](00_计算思维与Scratch.md) | [Week 0](https://cs50.harvard.edu/x/weeks/0/) / [Notes](https://cs50.harvard.edu/x/notes/0/) |
| 01 | [C 语言与编译](01_C语言与编译.md) | [Week 1](https://cs50.harvard.edu/x/weeks/1/) / [Notes](https://cs50.harvard.edu/x/notes/1/) |
| 02 | [数组、字符串与命令行](02_数组字符串与命令行.md) | [Week 2](https://cs50.harvard.edu/x/weeks/2/) / [Notes](https://cs50.harvard.edu/x/notes/2/) |
| 03 | [算法、排序与递归](03_算法排序与递归.md) | [Week 3](https://cs50.harvard.edu/x/weeks/3/) / [Notes](https://cs50.harvard.edu/x/notes/3/) |
| 04 | [内存、指针与文件](04_内存指针与文件.md) | [Week 4](https://cs50.harvard.edu/x/weeks/4/) / [Notes](https://cs50.harvard.edu/x/notes/4/) |
| 05 | [数据结构的实现](05_数据结构的实现.md) | [Week 5](https://cs50.harvard.edu/x/weeks/5/) / [Notes](https://cs50.harvard.edu/x/notes/5/) |
| 06 | [Python 与高级语言](06_Python与高级语言.md) | [Week 6](https://cs50.harvard.edu/x/weeks/6/) / [Notes](https://cs50.harvard.edu/x/notes/6/) |
| 07 | [SQL 与关系数据库](07_SQL与关系数据库.md) | [Week 7](https://cs50.harvard.edu/x/weeks/7/) / [Notes](https://cs50.harvard.edu/x/notes/7/) |
| 专题 | [AI 专题](11_AI专题.md) | [Artificial Intelligence](https://cs50.harvard.edu/x/weeks/ai/) / [Notes](https://cs50.harvard.edu/x/notes/ai/) |
| 08 | [HTML、CSS、JavaScript](08_HTML_CSS_JavaScript.md) | [Week 8](https://cs50.harvard.edu/x/weeks/8/) / [Notes](https://cs50.harvard.edu/x/notes/8/) |
| 09 | [Flask 与 Web 应用](09_Flask与Web应用.md) | [Week 9](https://cs50.harvard.edu/x/weeks/9/) / [Notes](https://cs50.harvard.edu/x/notes/9/) |
| 10 | [课程收束与后续学习](10_课程收束与后续学习.md) | [Week 10](https://cs50.harvard.edu/x/weeks/10/) / [Notes](https://cs50.harvard.edu/x/notes/10/) |
| 最终项目 | [从需求到自己的作品](12_最终项目.md) | [Final Project](https://cs50.harvard.edu/x/project/) |

AI 专题文件编号 11 仅用于本地收纳，不代表官方 Week 11，也没有虚构 Problem Set 11。推荐在 SQL 后、网页前读，与官方目录位置相同；不阻止你先完成 08–10 后再复习专题。

## 每章怎样学

1. 先运行课堂例子，对照实际输出，找出输入、处理和结果。
2. 按解释追踪函数调用和数据变化，尤其说明数据由谁创建、谁修改、何时不能再使用。
3. 只改一个条件或输入，预测结果后运行；故意错误示意只阅读，不运行越界或释放后访问代码。
4. 独立完成本章自编练习，再按官方问题集页面的要求实践。不要把课堂示例改个名字交作正式作业。
5. 通过正常、边界和错误输入确认，不以“看完了”代替完成。

正式问题集的 AI 使用限制与普通自学不同，请读[学术诚信规则](https://cs50.harvard.edu/x/honesty/)。官方最终项目有单独说明，不能把其例外推广到其他问题集。

## 与现有课程的关系

- [CS50P](../../新手需要学习的前置知识/CS50P/README.md)仍是 Python 热身主线；本课 06 侧重与 C 的对照，不另替换整个 CS50P。
- 上一级 [02–08 基础补充](../README.md)继续作为应用实验：操作系统、网络和数据库的某些实践不属于 CS50x 完整展开的内容。
- 本课学完后仍按你原来的 [AI 应用主线](../../README.md)继续，不重新编号或自动清空进度。

[主题覆盖与质量验收](../../../docs/cs50x-course-acceptance.md)区分已核对内容、实际运行结果和未验证部分。能跑课堂例子不等于已经通过官方作业、项目或证书要求。

开始：[00. 计算思维与 Scratch](00_计算思维与Scratch.md)。
