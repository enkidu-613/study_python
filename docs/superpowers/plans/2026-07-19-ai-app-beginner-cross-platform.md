# AI 应用开发新手前置课程跨平台修订 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the beginner curriculum usable by Windows PowerShell, macOS zsh, and Linux Bash learners without duplicating system-independent lessons.

**Architecture:** Keep the shared teaching content unchanged and add concise command matrices only around system-dependent actions. The README defines the reading rule; chapters 01, 02, 06, 07, and 09 supply the concrete operating-system guidance.

**Tech Stack:** Markdown, Python 3, Git, SQLite, Windows PowerShell, macOS zsh, Linux Bash.

## Global Constraints

- Windows 10/11 uses PowerShell and does not require WSL.
- macOS uses Terminal/iTerm with zsh; Linux uses a terminal with Bash.
- System-specific commands must have Windows PowerShell and macOS/Linux Shell forms.
- Python, HTTP, SQL, Git concepts and checkpoints remain shared.
- Do not alter the course sequence, existing tutorial handoff, or AI-application scope.

---

### Task 1: Establish cross-platform reading and path conventions

**Files:**
- Modify: `md/新手需要学习的前置知识/README.md`
- Modify: `md/新手需要学习的前置知识/01_电脑文件与开发环境.md`
- Modify: `md/新手需要学习的前置知识/02_终端命令与程序运行.md`

- [x] **Step 1: Add the supported operating systems and the “choose your column” rule to README.**
- [x] **Step 2: Add Windows, macOS, and Linux development-environment entry points and path examples to chapter 01.**
- [x] **Step 3: Replace macOS-default terminal instructions in chapter 02 with PowerShell and macOS/Linux command matrices for opening a terminal, locating a project, listing files, and running Python.**
- [x] **Step 4: Verify command blocks contain `python hello.py` for Windows and `python3 hello.py` for macOS/Linux.**

Run:

```bash
rg -n "Windows|PowerShell|macOS|Linux|python hello.py|python3 hello.py" md/新手需要学习的前置知识/{README,01_*,02_*}.md
```

Expected: all three operating systems appear; both Python execution commands appear in chapter 02.

### Task 2: Make project tooling and SQLite instructions cross-platform

**Files:**
- Modify: `md/新手需要学习的前置知识/06_Python项目化_模块异常调试与依赖.md`
- Modify: `md/新手需要学习的前置知识/07_Git与GitHub_保存代码历史.md`
- Modify: `md/新手需要学习的前置知识/09_数据库与SQL入门.md`

- [x] **Step 1: Add side-by-side virtual-environment creation, activation, and package commands to chapter 06.**
- [x] **Step 2: Explain PowerShell execution-policy failure safely: use a process-scoped bypass only when the learner understands the message, then activate the local `.venv`.**
- [x] **Step 3: Add Git cross-platform and Windows-path notes to chapter 07 without changing Git commands.**
- [x] **Step 4: Add three-system terminal guidance and a no-install fallback to chapter 09.**
- [x] **Step 5: Audit all curriculum Shell examples for an accompanying PowerShell or macOS/Linux form.**

Run:

```bash
rg -n "Activate.ps1|source \.venv/bin/activate|Set-ExecutionPolicy|PowerShell|macOS/Linux" md/新手需要学习的前置知识/{06_*,07_*,09_*}.md
```

Expected: the virtual-environment activation pair and three-system instructions are present.

### Task 3: Verify scope, links, and cross-platform coverage

**Files:**
- Modify: `docs/superpowers/plans/2026-07-19-ai-app-beginner-cross-platform.md`

- [x] **Step 1: Run a Markdown audit for all three operating systems, required activation commands, teaching-contract headings, relative links, and Python code syntax.**
- [x] **Step 2: Confirm no chapter presents macOS as the default operating system or requires WSL.**
- [x] **Step 3: Mark this plan complete only after the audit passes.**

Run:

```bash
python3 -c "from pathlib import Path; text='\n'.join(p.read_text(encoding='utf-8') for p in Path('md/新手需要学习的前置知识').glob('*.md')); assert 'PowerShell' in text and 'macOS' in text and 'Linux' in text; assert '.\\.venv\\Scripts\\Activate.ps1' in text and 'source .venv/bin/activate' in text; print('cross-platform audit: PASS')"
```

Expected: `cross-platform audit: PASS`.
