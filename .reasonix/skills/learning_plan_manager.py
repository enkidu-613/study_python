#!/usr/bin/env python3
"""
学习计划与历史文件索引管理器
提供查询、更新、触发等操作接口
用法: python learning_plan_manager.py <command> [args...]
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

PLAN_PATH = Path(".reasonix/memory/learning_plan.json")
HISTORY_PATH = Path(".reasonix/memory/learning_history_index.json")


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


def query_plan(stage_id: Optional[str] = None) -> None:
    plan = load_json(PLAN_PATH)
    stages = plan["stages"]
    if stage_id:
        stage = next((s for s in stages if s["id"] == stage_id), None)
        if not stage:
            print(f"❌ 未找到阶段: {stage_id}")
            return
        print(f"\n📋 {stage['name']} [{stage['status']}]")
        print(f"   描述: {stage['description']}")
        print(f"   完成: {stage['completed_at'] or '未完成'}")
        return
    total = len(stages)
    completed = sum(1 for s in stages if s["status"] == "completed")
    in_progress = sum(1 for s in stages if s["status"] == "in_progress")
    print(f"\n📊 进度: {completed}/{total} 完成 ({completed/total*100:.1f}%) | 🔄 {in_progress} | 当前: {plan.get('current_stage_id', '无')}")
    for s in stages:
        icon = "✅" if s["status"] == "completed" else "🔄" if s["status"] == "in_progress" else "⏳"
        print(f"   {icon} [{s['id']}] {s['name']}")


def query_history(stage_id: Optional[str] = None, topic: Optional[str] = None) -> None:
    history = load_json(HISTORY_PATH)
    entries = history["entries"]
    if stage_id:
        entries = [e for e in entries if e["stage_id"] == stage_id]
    if topic:
        entries = [e for e in entries if topic in e["topics"]]
    print(f"\n📚 {len(entries)} 条记录")
    for e in entries[:20]:
        print(f"   [{e['date']}] {e['title']} ({e['stage_id']})")


def complete_stage(stage_id: str) -> None:
    plan = load_json(PLAN_PATH)
    stages = plan["stages"]
    stage = next((s for s in stages if s["id"] == stage_id), None)
    if not stage:
        print(f"❌ 未找到: {stage_id}")
        return
    if stage["status"] == "completed":
        print(f"⚠️ 已完成")
        return
    for dep_id in stage.get("dependencies", []):
        dep = next((s for s in stages if s["id"] == dep_id), None)
        if dep and dep["status"] != "completed":
            print(f"❌ 依赖未完成: {dep['name']}")
            return
    stage["status"] = "completed"
    stage["completed_at"] = datetime.now().strftime("%Y-%m-%d")
    for s in stages:
        if s["status"] == "pending":
            deps_ok = all(
                next((d for d in stages if d["id"] == did), None) and
                next((d for d in stages if d["id"] == did), None)["status"] == "completed"
                for did in s.get("dependencies", [])
            )
            if deps_ok:
                s["status"] = "in_progress"
                plan["current_stage_id"] = s["id"]
                print(f"🔄 推进: {s['name']}")
                break
    plan["updated_at"] = datetime.now().isoformat()
    save_json(PLAN_PATH, plan)
    print(f"✅ 完成: {stage['name']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: query-plan [id] | query-history [--stage id] [--topic t] | complete-stage <id>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "query-plan":
        query_plan(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "query-history":
        sid = topic = None
        for i, a in enumerate(sys.argv):
            if a == "--stage" and i+1 < len(sys.argv): sid = sys.argv[i+1]
            if a == "--topic" and i+1 < len(sys.argv): topic = sys.argv[i+1]
        query_history(sid, topic)
    elif cmd == "complete-stage":
        if len(sys.argv) < 3: print("❌ 需要 stage_id"); sys.exit(1)
        complete_stage(sys.argv[2])
    else:
        print(f"❌ 未知: {cmd}")
