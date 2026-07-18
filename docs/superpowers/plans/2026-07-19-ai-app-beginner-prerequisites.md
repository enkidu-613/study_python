# AI 应用开发新手前置课程 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a self-contained, zero-to-AI-application-engineering prerequisite curriculum under `md/新手需要学习的前置知识/`.

**Architecture:** Thirteen short Markdown documents form an ordered learning path. Each chapter uses the project teaching contract—mental model, terminology, scope, minimal runnable example, pitfalls, checkpoints, exercise, and next step—and links into the existing AI-application curriculum only after the prerequisite path is complete.

**Tech Stack:** Markdown, Python 3 command examples, Git, SQLite SQL.

## Global Constraints

- Create only the files specified by the approved design in `md/新手需要学习的前置知识/`.
- Do not modify the existing numbered tutorials under `md/`.
- Target macOS commands while noting the Windows/Linux difference only where it matters.
- Exclude model training, algorithm-job preparation, and mathematics-heavy content.
- Keep examples copyable and safe; never include real API keys or destructive shell commands.

---

### Task 1: Create route overview and computer foundations

**Files:**
- Create: `md/新手需要学习的前置知识/README.md`
- Create: `md/新手需要学习的前置知识/00_从零到AI应用开发的学习地图.md`
- Create: `md/新手需要学习的前置知识/01_电脑文件与开发环境.md`
- Create: `md/新手需要学习的前置知识/02_终端命令与程序运行.md`
- Create: `md/新手需要学习的前置知识/03_编程思维与问题拆解.md`

- [x] **Step 1: Write README with the required sequence, time estimates, outputs, and project handoff.**
- [x] **Step 2: Write chapters 00–03 using the agreed teaching contract and only concepts introduced by the current or prior chapter.**
- [x] **Step 3: Verify headings, internal links, and safe terminal commands.**

Run:

```bash
rg -n "一句话理解|本章不学|最小|常见坑|检查点|小练习|下一步" md/新手需要学习的前置知识/{00,01,02,03}_*.md
```

Expected: each chapter exposes all seven teaching-contract sections.

### Task 2: Create independent Python foundations

**Files:**
- Create: `md/新手需要学习的前置知识/04_Python入门_变量条件循环.md`
- Create: `md/新手需要学习的前置知识/05_Python核心_函数容器与文件.md`
- Create: `md/新手需要学习的前置知识/06_Python项目化_模块异常调试与依赖.md`

- [x] **Step 1: Write chapter 04 for variables, string/number/bool, input/output, conditions, and loops.**
- [x] **Step 2: Write chapter 05 for functions, list, dict, file reading/writing, and a small data-processing exercise.**
- [x] **Step 3: Write chapter 06 for imports, packages, virtual environments, dependencies, exceptions, and traceback-first debugging.**
- [x] **Step 4: Verify every Python snippet is syntactically valid by extracting or manually running representative minimal examples.**

Run:

```bash
rg -n "```python|一句话理解|检查点|小练习" md/新手需要学习的前置知识/{04,05,06}_*.md
```

Expected: each chapter contains runnable Python examples and a learner-verifiable checkpoint.

### Task 3: Create engineering and web foundations

**Files:**
- Create: `md/新手需要学习的前置知识/07_Git与GitHub_保存代码历史.md`
- Create: `md/新手需要学习的前置知识/08_互联网_HTTP与JSON.md`
- Create: `md/新手需要学习的前置知识/09_数据库与SQL入门.md`
- Create: `md/新手需要学习的前置知识/10_数据结构与性能直觉.md`

- [x] **Step 1: Write Git chapter with a safe initial repository workflow and API-key protection boundary.**
- [x] **Step 2: Write HTTP/JSON chapter using a browser-to-server request flow and inspectable JSON examples.**
- [x] **Step 3: Write SQL chapter with a one-table SQLite example and safe CRUD commands.**
- [x] **Step 4: Write data-structure chapter limited to list, dict, set and simple performance intuition, not interview algorithms.**
- [x] **Step 5: Verify the Git and SQL samples use valid command syntax and the chapter boundaries exclude algorithm-job content.**

Run:

```bash
rg -n "git add|HTTP|SELECT|dict|不学算法题" md/新手需要学习的前置知识/{07,08,09,10}_*.md
```

Expected: all four practical foundations have a concrete example and an explicit non-goal.

### Task 4: Create AI application orientation and audit the curriculum

**Files:**
- Create: `md/新手需要学习的前置知识/11_AI应用开发基本地图.md`

- [x] **Step 1: Write chapter 11 to distinguish model API, Prompt, RAG, Agent, fine-tuning, and model training without implementation frameworks.**
- [x] **Step 2: Link chapter 11 and README to `md/00_环境配置与PyCharm使用.md` as the handoff into the existing project route.**
- [x] **Step 3: Count files and audit every chapter against the teaching contract.**
- [x] **Step 4: Review all new documents for broken relative links, accidental API secrets, placeholders, and training/algorithm-course drift.**

Run:

```bash
find md/新手需要学习的前置知识 -maxdepth 1 -name '*.md' -type f | wc -l
rg -n "TODO|TBD|API_KEY=sk-|反向传播|CUDA|分布式训练" md/新手需要学习的前置知识
```

Expected: 13 Markdown files; zero placeholder, secret, or out-of-scope training matches.
