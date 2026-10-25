---
name: personal-kb
description: Use when the user's question may be answered by their local learning notes, tutorials, project documentation, or personal knowledge base.
---

# personal-kb

## Description

个人学习知识库检索技能。基于本地 ChromaDB 向量数据库，检索用户自己的学习笔记和教程文章。知识库默认包含三个领域：Python/FastAPI/AI、NestJS 课程笔记、React 课程笔记。支持用户/AI 临时指定任意目录灌库。

## When to Use

当用户的问题可能在他们自己的学习笔记中有答案时，使用此技能检索相关内容。典型场景：

- 用户问 Python/FastAPI/Pydantic/SQLAlchemy/LangChain/ChromaDB/RAG/Agent 相关问题
- 用户问 NestJS/React/TypeScript/前端 相关问题
- 用户说"我之前学过这个"或"我的笔记里有没有"
- 用户问的项目代码相关概念，可能在教程文档中有解释
- 需要引用用户自己写的教程作为回答依据

不要在以下情况使用：
- 用户明确要求查互联网资料
- 用户问的是与学习笔记无关的通用问题（如天气、新闻）
- 用户要求修改代码而非理解概念

## How to Use

### 1. 检索知识库

在项目根目录 `/Users/enkidu/PyCharmMiscProject` 下运行命令：

```bash
# 基本检索（默认返回 3 条）
poetry run python -m app.tools.kb_search "查询关键词"

# 指定返回数量
poetry run python -m app.tools.kb_search "查询关键词" --limit 5

# 只搜 Python/AI 领域
poetry run python -m app.tools.kb_search "FastAPI 路由" --tag python_ai

# 只搜 NestJS 领域
poetry run python -m app.tools.kb_search "NestJS 控制器" --tag nestjs

# 只搜 React 领域
poetry run python -m app.tools.kb_search "React Hook" --tag react

# JSON 格式输出（方便程序处理）
poetry run python -m app.tools.kb_search "查询关键词" --json
```

### 2. 更新知识库

**当用户说"同步知识库"、"更新库"、"我改了笔记要同步"时,用增量同步(推荐):**

```bash
# 增量同步:只重灌变更的文件,删除其旧版本 chunks(3-5 秒/文件)
poetry run python -m app.tools.sync_notes

# 清理已删除文件的残留 chunks(笔记被删掉后用)
poetry run python -m app.tools.sync_notes --prune

# 强制全量重建(清空 + 重灌 + 重建索引,2-5 分钟,慎用)
poetry run python -m app.tools.sync_notes --full

# 同步指定目录(覆盖默认三目录)
poetry run python -m app.tools.sync_notes --path "/Users/enkidu/某目录" --tag my_notes
```

**增量同步原理:** 基于 `chroma_db/file_index.json` 索引记录每个文件的 mtime 和 chunk_ids。
- 新文件:灌入 + 记录索引
- mtime 变了:删除该文件旧 chunks → 灌入新的 → 更新索引
- mtime 没变:跳过
- 文件被删除:默认不处理,需 `--prune` 清理

**AI 使用流程:**
1. 用户说"同步"时,直接跑 `sync_notes`(不传参数,用默认三目录)
2. 同步完成后,把 `[summary]` 行的统计结果告诉用户(新增 X / 更新 Y / 跳过 Z)
3. 如果用户说"我删了某篇笔记",用 `--prune` 清理残留
4. 只有在索引损坏或大量数据异常时才用 `--full`

**旧的全量灌库命令(仍可用,但不推荐日常使用):**

```bash
# 全量灌入(不维护索引,无法增量)
poetry run python -m app.tools.ingest_notes
poetry run python -m app.tools.ingest_notes --reset
```

### 3. 临时灌入用户指定目录（开放能力）

**当用户说"把 xxx 目录灌进知识库"、"再加一个目录"、"也把我电脑上 /xxx 的笔记收进来"时，用 --path 临时指定。** 传了 `--path` 就覆盖默认三个目录，只灌用户指定的路径。

```bash
# 单个目录(标签默认 custom)
poetry run python -m app.tools.ingest_notes --path "/Users/enkidu/某目录"

# 单个目录 + 自定义标签
poetry run python -m app.tools.ingest_notes --path "/Users/enkidu/某目录" --tag my_notes

# 多个目录(按顺序配 --tag)
poetry run python -m app.tools.ingest_notes \
  --path "/Users/enkidu/目录A" --tag topic_a \
  --path "/Users/enkidu/目录B" --tag topic_b

# 先预览不写入(看文件数和切片数对不对)
poetry run python -m app.tools.ingest_notes --path "/Users/enkidu/某目录" --dry-run

# 清空整个库 + 灌用户目录(慎用 --reset,会清掉之前所有数据)
poetry run python -m app.tools.ingest_notes --reset --path "/Users/enkidu/某目录" --tag my_notes
```

**安全边界（自动生效）：** 系统敏感目录会被自动拒绝并打印 `[reject] 跳过敏感目录`，无需 AI 判断。黑名单包括：
- 系统目录：`/System` `/usr` `/bin` `/sbin` `/etc` `/var` `/private/etc` `/private/var` `/dev` `/proc` `/sys`
- macOS 库：`/Library` `/Users/enkidu/Library`
- 废纸篓：`/Users/enkidu/.Trash`

**AI 使用流程：**
1. 用户提供路径后，先用 `--dry-run` 预览，把文件数告诉用户确认范围
2. 用户确认后再去掉 `--dry-run` 正式灌入
3. 灌入完成后，告知用户新的 tag 是什么，方便后续 `kb_search --tag xxx` 检索
4. 如果路径被 `[reject]`，告诉用户该目录是系统敏感目录，请换一个

### 4. 检索结果说明

每条结果包含：

| 字段 | 说明 |
|------|------|
| title | 文件名（不含扩展名） |
| source | 文件完整路径 |
| tag | 领域标签：python_ai、nestjs、react 或用户自定义 |
| chunk_index | 在原文中的切片序号 |
| content | 实际内容片段 |

## Knowledge Base Info

- **ChromaDB 路径**: `./chroma_db/`
- **Collection**: `personal_notes`
- **Embedding 模型**: BAAI/bge-small-zh-v1.5（512 维）
- **切片策略**: RecursiveCharacterTextSplitter，chunk_size=500，overlap=80
- **默认数据来源（三个 tag）**:
  - `python_ai`: `/Users/enkidu/PyCharmMiscProject/md/` 下的所有 .md 文件
  - `nestjs`: `/Users/enkidu/project/study/01-语言/JavaScript/NestJS/后端课程/` 下的 .md 文件（排除 demo 项目目录）
  - `react`: `/Users/enkidu/project/study/01-语言/JavaScript/React/课程/` 下的 .md 文件（排除 demo 项目目录）
- **排除目录**: `node_modules` `.git` `dist` `build` `blog-demo` `prisma-demo` `prisma-my` `my-project` `my-project_new` `test_class` `frontend` `backend_notes` `start-point` `标准答案` `qa-backend` `qa-frontend-react` `qa-frontend-vue` `qa-fontend-vue` `generated`，以及 `backend-intro-notes-lesson4-*-demo` 前缀目录

## Response Guidelines

1. 检索后，基于返回的内容片段回答用户问题
2. 如果检索结果与问题相关，引用来源文件名
3. 如果检索结果不相关，告知用户"知识库中没有找到相关内容"
4. 不要编造笔记中没有的内容
5. 可以基于检索到的多个片段综合回答
6. 用户要求灌新目录时，按"3. 临时灌入用户指定目录"的 AI 使用流程操作，先 dry-run 预览再正式灌入
