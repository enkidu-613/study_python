# AI 应用开发新手前置课程跨平台设计

## 目标

将 `md/新手需要学习的前置知识/` 修订为可供 Windows、macOS 与 Linux 初学者独立使用的课程，不再把 macOS 当作默认系统。

## 受支持的命令环境

| 操作系统 | 本课程采用的终端 |
| --- | --- |
| Windows 10/11 | PowerShell；不要求安装 WSL。 |
| macOS | Terminal 或 iTerm 中的 zsh。 |
| Linux | 常见终端中的 Bash。 |

Windows 的 Command Prompt 不作为主教学环境，WSL 只作为以后可选工具，不是前置要求。

## 文档规则

- 每个系统相关动作都给出“Windows PowerShell”和“macOS/Linux Shell”并列命令；不适用的命令明确说明原因。
- Python 代码、HTTP、SQL、Git 概念和检查点保持系统无关，不复制三份内容。
- 路径示例同时展示 Windows 的反斜杠与 macOS/Linux 的斜杠，并说明用户必须替换为自己的目录。
- 虚拟环境章节展示 Windows 激活命令和 macOS/Linux 激活命令，并解释 Windows PowerShell 执行策略受限时的安全处理方式。
- 首次出现终端时，说明 Windows 从开始菜单打开 PowerShell，macOS 从应用程序/实用工具打开 Terminal，Linux 从应用菜单打开 Terminal。
- README 明确三种系统均受支持，并提示读者始终选择自己系统对应列。

## 影响文件

| 文件 | 修订内容 |
| --- | --- |
| README | 说明支持系统与阅读规则。 |
| 01 | 将开发环境和路径示例改为三系统可读。 |
| 02 | 以两列终端命令替代 macOS 默认命令。 |
| 06 | 并列虚拟环境创建、激活、包安装命令，补 PowerShell 常见错误。 |
| 07 | 说明 Git 命令跨系统一致，并补 Windows 路径提示。 |
| 09 | 说明 SQLite 命令可在三类终端运行，提供安装/不可用时的安全入口。 |

其余章节不包含系统专属命令，只在必要处补充“与系统无关”的说明。

## 验收标准

- 所有含 Shell 命令的章节均可找到 Windows PowerShell 和 macOS/Linux Shell 的对应入口。
- 文档不再声称 macOS 是默认学习系统。
- Windows 激活虚拟环境的命令为 `\.venv\Scripts\Activate.ps1`，macOS/Linux 为 `source .venv/bin/activate`。
- Markdown 链接、Python 示例、课程顺序与 AI 应用而非训练模型的边界保持不变。
