# AI 应用开发新手自学课程扩写 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the overview-level prerequisite curriculum with 25 self-contained, cross-platform Markdown lessons that a programming beginner can complete without screenshots.

**Architecture:** Split each prerequisite into a single observable action. The curriculum moves from computer setup, to Python practice, to a full Git/GitHub remote-repository loop, then to web/data concepts and the existing AI-application curriculum handoff.

**Tech Stack:** Markdown, Python 3, Git, GitHub web UI, SQLite, Windows PowerShell, macOS zsh, Linux Bash.

## Global Constraints

- Only replace files under `md/新手需要学习的前置知识/`; do not modify the existing project numbered tutorials.
- Use text, code blocks, tables, concrete UI labels, expected-output checks, and recovery guidance; do not require screenshots or videos.
- Every system-dependent operation shows Windows PowerShell and macOS/Linux Shell forms.
- Each lesson includes: mental model, scope, terminology, a minimum template, pitfalls, checkpoints, exercise, and next step.
- Do not include real credentials, model training, or algorithm-job content.

---

### Task 1: Replace onboarding and environment lessons

**Files:**
- Create: `md/新手需要学习的前置知识/README.md`
- Create: `md/新手需要学习的前置知识/00_课程使用方法与学习地图.md`
- Create: `md/新手需要学习的前置知识/01_认识电脑文件与开发工具.md`
- Create: `md/新手需要学习的前置知识/02_安装编辑器并创建第一个项目.md`
- Create: `md/新手需要学习的前置知识/03_安装Python并验证环境.md`
- Create: `md/新手需要学习的前置知识/04_路径_文件夹与文件扩展名.md`
- Create: `md/新手需要学习的前置知识/05_打开终端与定位目录.md`
- Create: `md/新手需要学习的前置知识/06_运行第一个Python程序与读报错.md`

- [x] Write 00–06 as independent, cross-platform setup lessons with first-run verification and recovery from missing commands.
- [x] Verify every system-specific action includes Windows and macOS/Linux guidance.

### Task 2: Replace Python foundation lessons

**Files:**
- Create: `md/新手需要学习的前置知识/07_编程思维_输入处理输出.md`
- Create: `md/新手需要学习的前置知识/08_Python变量_类型与运算.md`
- Create: `md/新手需要学习的前置知识/09_Python条件_循环与输入.md`
- Create: `md/新手需要学习的前置知识/10_Python函数_参数与返回值.md`
- Create: `md/新手需要学习的前置知识/11_Python列表_字典与集合.md`
- Create: `md/新手需要学习的前置知识/12_Python文件读写与异常处理.md`
- Create: `md/新手需要学习的前置知识/13_Python模块_虚拟环境与依赖.md`
- Create: `md/新手需要学习的前置知识/14_调试Traceback与小项目整理.md`

- [x] Write 07–14 with copyable examples, one incremental task per chapter, and input/output-based validation.
- [x] Compile every Python fence after writing.

### Task 3: Replace Git and GitHub lessons

**Files:**
- Create: `md/新手需要学习的前置知识/15_Git安装与首次身份配置.md`
- Create: `md/新手需要学习的前置知识/16_Git本地仓库_提交与回退.md`
- Create: `md/新手需要学习的前置知识/17_GitHub注册_安全设置与个人主页.md`
- Create: `md/新手需要学习的前置知识/18_创建GitHub仓库并首次推送.md`
- Create: `md/新手需要学习的前置知识/19_克隆_同步_分支与PullRequest入门.md`

- [x] Teach installation and `user.name`/`user.email` before any commit.
- [x] Teach registration, security, remote repository creation, `origin`, first push, browser verification, clone, pull, and a minimal Pull Request workflow as separate actions.
- [x] Keep authentication instructions credential-free and use the official GitHub browser flow.

### Task 4: Replace web/data/AI-handoff lessons and audit

**Files:**
- Create: `md/新手需要学习的前置知识/20_互联网_HTTP_URL与JSON.md`
- Create: `md/新手需要学习的前置知识/21_数据库_SQLite与SQL实操.md`
- Create: `md/新手需要学习的前置知识/22_数据结构选择与性能直觉.md`
- Create: `md/新手需要学习的前置知识/23_AI应用开发地图与进入项目主线.md`

- [x] Write 20–23 and update README links for all 24 numbered lessons.
- [x] Remove the old `00`–`11` files only after their replacements exist.
- [x] Verify there are 25 Markdown files, all lesson headings are present, Python fences compile, the handoff link resolves, and the GitHub first-push path is documented.

Run:

```bash
find md/新手需要学习的前置知识 -maxdepth 1 -name '*.md' -type f | wc -l
rg -n "git config --global user.name|github.com|git remote add origin|git push -u origin main|Pull Request" md/新手需要学习的前置知识
```

Expected: 25 files and all five Git/GitHub milestone commands or UI terms are present.
