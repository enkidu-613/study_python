---
name: "learning-plan-manager"
description: "管理学习计划进度和历史文件索引。Invoke when user asks to update learning progress, track completed stages, add learning plans, or query current learning status and history records."
---

# 学习计划与历史文件索引管理器

## 功能概述

本 Skill 负责管理用户的学习计划进度和历史文件索引，实现：
1. 学习计划的添加、更新、删除
2. 学习阶段完成后的自动进度更新
3. 历史文件索引的自动维护
4. 学习计划状态和历史记录的查询

## 数据存储结构

### 文件位置

```
.trae/memory/
├── learning_plan.json           # 学习计划主数据
└── learning_history_index.json  # 历史文件索引
```

### learning_plan.json 结构

```json
{
  "version": "1.0",
  "updated_at": "2026-05-31T12:00:00",
  "stages": [
    {
      "id": "stage-identifier",
      "name": "阶段名称",
      "description": "阶段描述",
      "status": "pending|in_progress|completed",
      "created_at": "2026-05-31",
      "completed_at": null,
      "documents": ["md/xxx.md"],
      "dependencies": ["依赖的阶段id"]
    }
  ],
  "current_stage_id": "当前进行中的阶段id"
}
```

### learning_history_index.json 结构

```json
{
  "version": "1.0",
  "updated_at": "2026-05-31T12:00:00",
  "entries": [
    {
      "id": "entry-identifier",
      "date": "2026-05-31",
      "title": "对话或文档标题",
      "file_path": "文件路径",
      "stage_id": "关联的阶段id",
      "entry_type": "dialog|document|milestone",
      "topics": ["主题标签"],
      "summary": "内容摘要"
    }
  ]
}
```

## 操作接口

### 1. 添加学习计划阶段

当用户新增学习内容时：

1. 读取 `learning_plan.json`
2. 在 `stages` 数组末尾追加新阶段对象
3. 更新 `updated_at` 时间戳
4. 写回文件

### 2. 标记阶段完成（触发机制）

当用户确认完成一个学习阶段时：

1. 读取 `learning_plan.json`
2. 找到对应 `stage_id`，修改：
   - `status` → `"completed"`
   - `completed_at` → 当前日期
3. 检查 `dependencies` 中的依赖阶段是否都已完成
   - 若依赖全部完成，将下一个阶段 `status` 改为 `"in_progress"`
   - 更新 `current_stage_id`
4. 更新 `updated_at` 时间戳
5. 写回文件
6. **同步更新历史索引**：将该阶段关联的对话/文档标记为已完成

### 3. 添加历史文件索引

当产生新的学习记录（对话、文档）时：

1. 读取 `learning_history_index.json`
2. 在 `entries` 数组开头插入新记录（最新的在最前）
3. 填写 `stage_id` 关联到当前进行中的阶段
4. 更新 `updated_at` 时间戳
5. 写回文件

### 4. 查询学习计划状态

当用户询问学习进度时：

1. 读取 `learning_plan.json`
2. 统计：
   - 总阶段数
   - 已完成数
   - 进行中数
   - 待开始数
3. 按顺序列出各阶段状态
4. 显示当前所在阶段

### 5. 查询历史文件索引

当用户询问历史记录时：

1. 读取 `learning_history_index.json`
2. 可按条件筛选：
   - `stage_id`：某阶段的所有记录
   - `date`：某日期范围的记录
   - `topics`：包含某主题的记录
3. 返回匹配的记录列表

## 数据一致性保证

1. **原子写操作**：先写临时文件，再重命名覆盖原文件
2. **版本校验**：读取时检查 `version` 字段，不匹配时进行迁移
3. **时间戳同步**：任何修改都必须更新 `updated_at`
4. **关联校验**：`stage_id` 必须在 `learning_plan.json` 中存在

## 操作可追溯性

所有修改记录通过 Git 提交保存：
- 修改学习计划后执行 `git add .trae/memory/learning_plan.json`
- 修改历史索引后执行 `git add .trae/memory/learning_history_index.json`
- 提交信息格式：`update(learning): 阶段XXX完成 / 添加历史记录XXX`
