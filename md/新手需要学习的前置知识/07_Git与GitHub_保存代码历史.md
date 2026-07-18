# 07. Git 与 GitHub：保存代码历史

> **一句话理解：Git 在你的电脑上记录代码每一次可信快照；GitHub 是可选的远程协作与备份平台。**

## 本章学什么，不学什么

学：仓库、工作区、暂存区、提交、差异与 `.gitignore`。

不学：复杂分支策略或团队发布流程；先把自己的代码安全保存下来。

## 准确术语

| 术语 | 准确含义 |
| --- | --- |
| 仓库（repository） | Git 管理的一组文件及其历史。 |
| 工作区 | 你正在编辑、还未提交的文件状态。 |
| 暂存区（staging area） | 下一次提交准备包含的文件清单。 |
| 提交（commit） | 一个带说明的、可回看的代码快照。 |
| 远程仓库 | 在 GitHub 等服务上的仓库副本。 |
| `.gitignore` | 告诉 Git 不要追踪哪些文件的规则文件。 |

## 最小模板：完成第一次提交

进入你的项目目录后执行：

```bash
git init
git status
git add main.py text_tools.py
git commit -m "完成文本处理小工具"
git log --oneline
```

`git init` 建立本地仓库；`git status` 显示状态；`git add` 把指定文件放进暂存区；`git commit` 创建快照；`git log --oneline` 查看历史。提交信息写“做了什么”，不要写“更新”。

## 最小模板：不提交私密配置

新建 `.gitignore`：

```gitignore
.venv/
__pycache__/
.env
```

`.env` 常用于放本机环境变量，例如模型服务密钥。它应该留在自己电脑，不应提交到 Git 或截图发送。程序需要配置时提交 `.env.example`，只保留变量名，不填写真实值。

## 看懂差异

修改 `main.py` 后：

```bash
git diff
git status
```

`git diff` 显示还没有暂存的变化；确认是你想要的，再 `git add` 和提交。

## 常见坑

- `git add .` 前不看 `git status`：可能把临时文件或私密文件一起加入。
- 以为 GitHub 等于 Git：没有网络也能使用本地 Git。
- 提交后继续修改却以为已保存：新的修改还在工作区，需要新提交。
- 已提交密钥才添加 `.gitignore`：`.gitignore` 不会删除历史中的秘密，应立刻轮换该密钥。

## 检查点

- [ ] 能用一句话区分工作区、暂存区与提交。
- [ ] 能执行一次 `status → add → commit → log`。
- [ ] 知道 `.env` 和 `.venv/` 为什么应被忽略。

## 小练习

为上一章的项目创建仓库，完成两次提交：第一次是可运行版本，第二次只改欢迎文本。运行 `git log --oneline`，能看到两条历史。

## 下一步

继续：[08. 互联网、HTTP 与 JSON](08_互联网_HTTP与JSON.md)。
