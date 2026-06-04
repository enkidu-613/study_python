---
name: learning-plan-manager
description: 管理学习计划进度和历史文件索引。当用户要求更新学习进度、追踪阶段完成、添加学习计划或查询当前学习状态时调用。
---
# 学习计划与历史文件索引管理器

## 功能概述

管理用户的学习计划进度和历史文件索引，实现：
1. 学习计划的添加、更新、删除
2. 学习阶段完成后的自动进度更新
3. 历史文件索引的自动维护
4. 学习计划状态和历史记录的查询

## 数据文件位置

```
.reasonix/memory/
├── learning_plan.json           # 学习计划主数据
├── learning_history_index.json  # 历史文件索引
├── conversations/               # 日期对话文件
│   └── YYYY-MM-DD.md
├── learning_notes.md
├── project_overview.md
├── code_patterns.md
├── learning_rag_week1.md
└── roadmap查缺补漏计划.md

.reasonix/skills/learning-plan-manager/
└── learning_plan_manager.py     # Python 辅助脚本
```

另外：
- 错题本位置：`md/错题本.md`
- 学习文档：`md/` 目录下的 `00_*` ~ `15_*` 系列

## learning_plan.json 结构

```json
{
  "version": "1.0",
  "updated_at": "ISO时间戳",
  "stages": [
    {
      "id": "stage-id",
      "name": "阶段名称",
      "description": "描述",
      "status": "pending|in_progress|completed",
      "created_at": "YYYY-MM-DD",
      "completed_at": null,
      "documents": ["md/xxx.md"],
      "dependencies": ["依赖stage id"],
      "roadmap_tags": ["标签"]
    }
  ],
  "current_stage_id": "当前阶段id"
}
```

## learning_history_index.json 结构

```json
{
  "version": "1.0",
  "updated_at": "ISO时间戳",
  "entries": [
    {
      "id": "dialog-N",
      "date": "YYYY-MM-DD",
      "title": "标题",
      "file_path": ".reasonix/memory/conversations/YYYY-MM-DD.md",
      "stage_id": "关联阶段",
      "entry_type": "dialog|document|milestone",
      "topics": ["标签"],
      "summary": "摘要"
    }
  ]
}
```

## 操作

### 查询学习进度
1. 读取 `.reasonix/memory/learning_plan.json`
2. 统计 total / completed / in_progress / pending
3. 按顺序列出各阶段状态（✅ 🟡 ⏳）
4. 显示当前阶段

### 标记阶段完成
1. 读取 learning_plan.json，找到 stage
2. 检查 dependencies 是否都已完成
3. 设置 status="completed", completed_at=今天
4. 若有下一阶段且其依赖都满足，自动推进
5. 写回文件，更新时间戳
6. 可选：运行 `.reasonix/skills/learning-plan-manager/learning_plan_manager.py complete-stage <stage_id>`

### 添加历史索引
1. 读取 learning_history_index.json
2. 在 entries 数组最前面插入新条目
3. 写回文件

### 对话归档（每天结束时）
1. 提取关键信息（主题、方案、知识点）
2. 追加到 `.reasonix/memory/conversations/YYYY-MM-DD.md`
3. 更新 learning_history_index.json
4. 格式：
```markdown
## 对话 N: [简短主题]
**时间**: YYYY-MM-DD
**用户任务**: [概括]
### 主要内容
- [要点]
```

## Python 辅助脚本

`.reasonix/skills/learning-plan-manager/learning_plan_manager.py` 提供命令行接口：
- `query-plan [stage_id]` — 查询进度
- `query-history [--stage id] [--topic t]` — 查询历史
- `complete-stage <id>` — 标记完成
- `add-stage <id> <name> <desc> [--dep ...] [--doc ...]` — 添加阶段
- `add-history <title> <path> <stage_id> [--topic ...] [--summary ...]` — 添加记录

## 注意事项
- 所有修改操作后更新 updated_at 时间戳
- stage_id 必须在 learning_plan.json 中存在
- 对话归档时 file_path 前缀用 `.reasonix/memory/` 而非 `.trae/memory/`
