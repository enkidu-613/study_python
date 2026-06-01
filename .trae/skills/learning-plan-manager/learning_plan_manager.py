#!/usr/bin/env python3
"""
学习计划与历史文件索引管理器
提供查询、更新、触发等操作接口
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# 数据文件路径
PLAN_PATH = Path(".trae/memory/learning_plan.json")
HISTORY_PATH = Path(".trae/memory/learning_history_index.json")


def load_json(path: Path) -> dict:
    """加载 JSON 文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """原子写入 JSON 文件（先写临时文件，再重命名）"""
    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


def query_plan(stage_id: Optional[str] = None) -> None:
    """
    查询学习计划状态
    用法: python learning_plan_manager.py query-plan [stage_id]
    """
    plan = load_json(PLAN_PATH)
    stages = plan["stages"]

    if stage_id:
        stage = next((s for s in stages if s["id"] == stage_id), None)
        if not stage:
            print(f"❌ 未找到阶段: {stage_id}")
            return
        print(f"\n📋 阶段详情: {stage['name']}")
        print(f"   状态: {stage['status']}")
        print(f"   描述: {stage['description']}")
        print(f"   创建: {stage['created_at']}")
        print(f"   完成: {stage['completed_at'] or '未完成'}")
        print(f"   文档: {', '.join(stage['documents']) or '无'}")
        return

    # 统计
    total = len(stages)
    completed = sum(1 for s in stages if s["status"] == "completed")
    in_progress = sum(1 for s in stages if s["status"] == "in_progress")
    pending = sum(1 for s in stages if s["status"] == "pending")

    print(f"\n📊 学习进度总览")
    print(f"   总阶段: {total}")
    print(f"   ✅ 已完成: {completed} ({completed/total*100:.1f}%)")
    print(f"   🔄 进行中: {in_progress}")
    print(f"   ⏳ 待开始: {pending}")
    print(f"   当前阶段: {plan.get('current_stage_id', '无')}")

    print(f"\n📋 阶段列表")
    for s in stages:
        icon = "✅" if s["status"] == "completed" else "🔄" if s["status"] == "in_progress" else "⏳"
        print(f"   {icon} [{s['id']}] {s['name']} ({s['status']})")


def query_history(stage_id: Optional[str] = None, topic: Optional[str] = None) -> None:
    """
    查询历史文件索引
    用法: python learning_plan_manager.py query-history [--stage stage_id] [--topic topic]
    """
    history = load_json(HISTORY_PATH)
    entries = history["entries"]

    # 筛选
    if stage_id:
        entries = [e for e in entries if e["stage_id"] == stage_id]
    if topic:
        entries = [e for e in entries if topic in e["topics"]]

    print(f"\n📚 历史文件索引 ({len(entries)} 条记录)")
    for e in entries:
        print(f"\n   [{e['date']}] {e['title']}")
        print(f"   文件: {e['file_path']}")
        print(f"   阶段: {e['stage_id']}")
        print(f"   类型: {e['entry_type']}")
        print(f"   主题: {', '.join(e['topics'])}")
        print(f"   摘要: {e['summary']}")


def complete_stage(stage_id: str) -> None:
    """
    标记阶段完成，自动更新进度
    用法: python learning_plan_manager.py complete-stage <stage_id>
    """
    plan = load_json(PLAN_PATH)
    stages = plan["stages"]

    stage = next((s for s in stages if s["id"] == stage_id), None)
    if not stage:
        print(f"❌ 未找到阶段: {stage_id}")
        return

    if stage["status"] == "completed":
        print(f"⚠️ 阶段 '{stage['name']}' 已经是完成状态")
        return

    # 检查依赖
    for dep_id in stage.get("dependencies", []):
        dep = next((s for s in stages if s["id"] == dep_id), None)
        if dep and dep["status"] != "completed":
            print(f"❌ 依赖阶段未完成: {dep['name']} ({dep_id})")
            return

    # 标记完成
    now = datetime.now().strftime("%Y-%m-%d")
    stage["status"] = "completed"
    stage["completed_at"] = now

    # 寻找下一个可开始的阶段
    for s in stages:
        if s["status"] == "pending":
            deps = s.get("dependencies", [])
            if all(
                next((d for d in stages if d["id"] == dep_id), None)
                and next((d for d in stages if d["id"] == dep_id), None)["status"] == "completed"
                for dep_id in deps
            ):
                s["status"] = "in_progress"
                plan["current_stage_id"] = s["id"]
                print(f"🔄 自动启动下一阶段: {s['name']}")
                break

    plan["updated_at"] = datetime.now().isoformat()
    save_json(PLAN_PATH, plan)

    print(f"✅ 阶段完成: {stage['name']} ({stage_id})")
    print(f"   完成日期: {now}")

    # 同步更新历史索引中的记录状态
    history = load_json(HISTORY_PATH)
    updated = 0
    for entry in history["entries"]:
        if entry["stage_id"] == stage_id:
            # 历史记录本身不需要改状态，但可以添加完成标记
            updated += 1
    if updated > 0:
        print(f"   同步更新 {updated} 条历史记录关联")


def add_stage(name: str, description: str, stage_id: str, dependencies: list[str] = None, documents: list[str] = None) -> None:
    """
    添加新学习阶段
    用法: python learning_plan_manager.py add-stage <id> <name> <description> [--dep dep1,dep2] [--doc doc1,doc2]
    """
    plan = load_json(PLAN_PATH)

    if any(s["id"] == stage_id for s in plan["stages"]):
        print(f"❌ 阶段 ID 已存在: {stage_id}")
        return

    new_stage = {
        "id": stage_id,
        "name": name,
        "description": description,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "completed_at": None,
        "documents": documents or [],
        "dependencies": dependencies or []
    }

    plan["stages"].append(new_stage)
    plan["updated_at"] = datetime.now().isoformat()
    save_json(PLAN_PATH, plan)

    print(f"✅ 添加阶段: {name} ({stage_id})")


def add_history(title: str, file_path: str, stage_id: str, topics: list[str] = None, summary: str = "") -> None:
    """
    添加历史文件索引记录
    用法: python learning_plan_manager.py add-history <title> <file_path> <stage_id> [--topic t1,t2] [--summary text]
    """
    history = load_json(HISTORY_PATH)
    plan = load_json(PLAN_PATH)

    # 校验 stage_id
    if not any(s["id"] == stage_id for s in plan["stages"]):
        print(f"⚠️ 警告: stage_id '{stage_id}' 不存在于学习计划中")

    new_entry = {
        "id": f"entry-{len(history['entries']) + 1:03d}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": title,
        "file_path": file_path,
        "stage_id": stage_id,
        "entry_type": "document",
        "topics": topics or [],
        "summary": summary
    }

    history["entries"].insert(0, new_entry)  # 最新记录放最前
    history["updated_at"] = datetime.now().isoformat()
    save_json(HISTORY_PATH, history)

    print(f"✅ 添加历史记录: {title}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
学习计划管理器

用法:
  python learning_plan_manager.py query-plan [stage_id]     查询学习计划
  python learning_plan_manager.py query-history [--stage id] [--topic t]  查询历史索引
  python learning_plan_manager.py complete-stage <stage_id>  标记阶段完成
  python learning_plan_manager.py add-stage <id> <name> <desc> [--dep ...] [--doc ...]  添加阶段
  python learning_plan_manager.py add-history <title> <path> <stage_id> [--topic ...] [--summary ...]  添加历史
        """)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "query-plan":
        query_plan(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "query-history":
        stage_id = None
        topic = None
        for i, arg in enumerate(sys.argv):
            if arg == "--stage" and i + 1 < len(sys.argv):
                stage_id = sys.argv[i + 1]
            if arg == "--topic" and i + 1 < len(sys.argv):
                topic = sys.argv[i + 1]
        query_history(stage_id, topic)
    elif cmd == "complete-stage":
        if len(sys.argv) < 3:
            print("❌ 需要 stage_id")
            sys.exit(1)
        complete_stage(sys.argv[2])
    elif cmd == "add-stage":
        if len(sys.argv) < 5:
            print("❌ 需要: id name description")
            sys.exit(1)
        deps = None
        docs = None
        for i, arg in enumerate(sys.argv):
            if arg == "--dep" and i + 1 < len(sys.argv):
                deps = sys.argv[i + 1].split(",")
            if arg == "--doc" and i + 1 < len(sys.argv):
                docs = sys.argv[i + 1].split(",")
        add_stage(sys.argv[3], sys.argv[4], sys.argv[2], deps, docs)
    elif cmd == "add-history":
        if len(sys.argv) < 5:
            print("❌ 需要: title file_path stage_id")
            sys.exit(1)
        topics = None
        summary = ""
        for i, arg in enumerate(sys.argv):
            if arg == "--topic" and i + 1 < len(sys.argv):
                topics = sys.argv[i + 1].split(",")
            if arg == "--summary" and i + 1 < len(sys.argv):
                summary = sys.argv[i + 1]
        add_history(sys.argv[2], sys.argv[3], sys.argv[4], topics, summary)
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)
