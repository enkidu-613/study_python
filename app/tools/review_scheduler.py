"""复习调度器 CLI 工具(基于 FSRS 间隔重复算法)。

用法:
    poetry run python -m app.tools.review_scheduler add --topic "范数" --source "md/ai学习应用数学/01_向量与余弦相似度.md"
    poetry run python -m app.tools.review_scheduler due
    poetry run python -m app.tools.review_scheduler due --json
    poetry run python -m app.tools.review_scheduler rate --topic "范数" --rating again
    poetry run python -m app.tools.review_scheduler rate --topic "范数" --rating easy --note "能给AI讲清楚"
    poetry run python -m app.tools.review_scheduler list
    poetry run python -m app.tools.review_scheduler stats
    poetry run python -m app.tools.review_scheduler migrate

评分档位(与 FSRS/Anki 一致):
    again  = 忘了/答错        (间隔重置到最短)
    hard   = 勉强想起/重讲才懂 (间隔略增)
    good   = 正常想起         (间隔正常增长)
    easy   = 轻松想起/能讲给别人 (间隔大幅增长)

文件说明:
    .agents/memory/fsrs_queue.json    ← 本工具的 FSRS 队列(新)
    .agents/memory/review_queue.json  ← 旧阶梯版错题队列(quizzer 契约,
                                       schema 被 tests/test_learning_skill_contract.py 锁定,勿改)
    migrate 命令会把旧队列错题导入 FSRS 队列,旧文件保持原样
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from fsrs import Card, Rating, Scheduler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
# FSRS 队列(新):存 D/S 记忆状态
QUEUE_PATH = PROJECT_ROOT / ".agents" / "memory" / "fsrs_queue.json"
# 旧阶梯版错题队列(quizzer 契约文件,只读迁移,不修改)
LEGACY_QUEUE_PATH = PROJECT_ROOT / ".agents" / "memory" / "review_queue.json"

RATING_MAP = {
    "again": Rating.Again,
    "hard": Rating.Hard,
    "good": Rating.Good,
    "easy": Rating.Easy,
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_queue() -> dict:
    if not QUEUE_PATH.exists():
        return {"version": 1, "cards": {}}
    with open(QUEUE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_queue(queue: dict) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def cmd_add(args: argparse.Namespace) -> None:
    queue = load_queue()
    cards = queue.setdefault("cards", {})
    if args.topic in cards:
        print(f"[skip] 主题已存在: {args.topic}(用 rate 更新,不要重复 add)")
        return
    scheduler = Scheduler()
    card = Card()
    # 新卡默认先按 good 处理一次,让它进入调度循环拿到首个到期日
    card, _log = scheduler.review_card(card, Rating.Good, now_utc())
    cards[args.topic] = {
        "card": card.to_dict(),
        "source": args.source or "",
        "tags": args.tag or [],
        "created": now_utc().isoformat(),
        "history": [{"time": now_utc().isoformat(), "rating": "good", "note": "initial"}],
    }
    save_queue(queue)
    due_local = card.due.astimezone().strftime("%Y-%m-%d %H:%M")
    print(f"[add] 主题入队: {args.topic}")
    print(f"      首次到期: {due_local}")


def cmd_migrate(_: argparse.Namespace) -> None:
    """把旧阶梯版错题队列(review_queue.json)导入 FSRS 队列,旧文件不动。"""
    if not LEGACY_QUEUE_PATH.exists():
        print("[skip] 旧队列不存在,无需迁移")
        return
    with open(LEGACY_QUEUE_PATH, encoding="utf-8") as f:
        legacy = json.load(f)
    queue = load_queue()
    cards = queue.setdefault("cards", {})
    added, skipped = 0, 0
    for item in legacy.get("items", []):
        topic = item.get("topic") or item.get("id", "")
        if not topic or topic in cards:
            skipped += 1
            continue
        card = Card()  # 全新卡,未复习过,立即可复习
        cards[topic] = {
            "card": card.to_dict(),
            "source": item.get("source", ""),
            "tags": [item["stage_id"]] if item.get("stage_id") else [],
            "created": now_utc().isoformat(),
            "history": [],
            # 旧错题的题目和答案,复习出题时直接用
            "review_material": {
                "prompt": item.get("prompt", ""),
                "answer": item.get("answer", ""),
                "legacy_id": item.get("id", ""),
            },
        }
        added += 1
    save_queue(queue)
    print(f"[migrate] 旧队列导入完成: 新增 {added} 条,跳过 {skipped} 条(已存在)")
    print(f"          旧文件未修改: {LEGACY_QUEUE_PATH.name}")


def cmd_due(args: argparse.Namespace) -> None:
    queue = load_queue()
    cards = queue.setdefault("cards", {})
    if not cards:
        print("[empty] 队列为空,先用 add 添加主题")
        return
    now = now_utc()
    due_items = []
    for topic, item in cards.items():
        card = Card.from_dict(item["card"])
        if card.due <= now:
            due_items.append((topic, card, item))
    # 按到期时间排序,最该复习的排前面
    due_items.sort(key=lambda x: x[1].due)
    if not due_items:
        nearest = min(
            (Card.from_dict(i["card"]).due for i in cards.values()),
        )
        days_left = (nearest - now).total_seconds() / 86400
        print(f"[clear] 今日无到期项。最近的到期在 {days_left:.1f} 天后")
        return
    if args.json:
        payload = [
            {
                "topic": topic,
                "source": item.get("source", ""),
                "tags": item.get("tags", []),
                "stability": round(card.stability, 2) if card.stability else None,
                "difficulty": round(card.difficulty, 2) if card.difficulty else None,
                "is_new": card.stability is None,
                "has_material": bool(item.get("review_material", {}).get("prompt")),
                "overdue_days": round((now - card.due).total_seconds() / 86400, 1),
            }
            for topic, card, item in due_items
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"[due] 今日到期 {len(due_items)} 项(按逾期时间排序):")
        for topic, card, item in due_items:
            overdue = (now - card.due).total_seconds() / 86400
            src = item.get("source", "")
            src_short = src.split("/")[-1] if src else "无来源"
            stability = f"{card.stability:.1f}" if card.stability else "新卡"
            has_material = " | 有复习题" if item.get("review_material", {}).get("prompt") else ""
            print(f"  - {topic}(逾期 {overdue:.1f} 天 | 稳定性 {stability} | 来源: {src_short}{has_material})")


def cmd_rate(args: argparse.Namespace) -> None:
    queue = load_queue()
    cards = queue.setdefault("cards", {})
    if args.topic not in cards:
        print(f"[error] 主题不存在: {args.topic}(先 add)")
        sys.exit(1)
    if args.rating not in RATING_MAP:
        print(f"[error] 无效评分: {args.rating}(可选 again/hard/good/easy)")
        sys.exit(1)
    item = cards[args.topic]
    card = Card.from_dict(item["card"])
    scheduler = Scheduler()
    card, _log = scheduler.review_card(card, RATING_MAP[args.rating], now_utc())
    item["card"] = card.to_dict()
    item["history"].append(
        {"time": now_utc().isoformat(), "rating": args.rating, "note": args.note or ""}
    )
    save_queue(queue)
    due_local = card.due.astimezone().strftime("%Y-%m-%d %H:%M")
    print(f"[rate] {args.topic} ← {args.rating}")
    print(f"       稳定性 {card.stability:.2f} | 难度 {card.difficulty:.2f} | 状态 {card.state.name}")
    print(f"       下次到期: {due_local}")


def cmd_list(args: argparse.Namespace) -> None:
    queue = load_queue()
    cards = queue.setdefault("cards", {})
    if not cards:
        print("[empty] 队列为空")
        return
    now = now_utc()
    if args.json:
        payload = {}
        for topic, item in cards.items():
            card = Card.from_dict(item["card"])
            payload[topic] = {
                "due": card.due.isoformat(),
                "stability": round(card.stability, 2) if card.stability else None,
                "difficulty": round(card.difficulty, 2) if card.difficulty else None,
                "reviews": len(item["history"]),
                "source": item.get("source", ""),
            }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    rows = []
    for topic, item in cards.items():
        card = Card.from_dict(item["card"])
        status = "已到期" if card.due <= now else f"{(card.due - now).total_seconds() / 86400:.1f} 天后"
        rows.append((card.due, topic, status, card, len(item["history"])))
    rows.sort(key=lambda x: x[0])
    print(f"[list] 队列共 {len(rows)} 项(按到期时间排序):")
    for _due, topic, status, card, reviews in rows:
        stability = f"{card.stability:.1f}" if card.stability else "新卡"
        difficulty = f"{card.difficulty:.1f}" if card.difficulty else "-"
        print(
            f"  - {topic:<28} {status:<10} "
            f"稳定 {stability:<6} 难度 {difficulty} 复习 {reviews} 次"
        )


def cmd_stats(_: argparse.Namespace) -> None:
    queue = load_queue()
    cards = queue.setdefault("cards", {})
    if not cards:
        print("[empty] 队列为空")
        return
    now = now_utc()
    due_count = sum(1 for i in cards.values() if Card.from_dict(i["card"]).due <= now)
    total_reviews = sum(len(i["history"]) for i in cards.values())
    ratings: dict[str, int] = {}
    for i in cards.values():
        for h in i["history"]:
            if h["rating"] != "initial":
                ratings[h["rating"]] = ratings.get(h["rating"], 0) + 1
    print(f"[stats] 主题数 {len(cards)} | 今日到期 {due_count} | 总复习次数 {total_reviews}")
    if ratings:
        dist = " ".join(f"{k}×{v}" for k, v in sorted(ratings.items()))
        print(f"       评分分布: {dist}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FSRS 复习调度器")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="新主题入队")
    p_add.add_argument("--topic", required=True, help="主题名(建议与对话 topics 粒度一致)")
    p_add.add_argument("--source", default="", help="来源文档路径(用于复习时检索原文)")
    p_add.add_argument("--tag", nargs="*", default=[], help="可选标签")
    p_add.set_defaults(func=cmd_add)

    p_due = sub.add_parser("due", help="查询今日到期主题")
    p_due.add_argument("--json", action="store_true", help="JSON 输出")
    p_due.set_defaults(func=cmd_due)

    p_rate = sub.add_parser("rate", help="记录一次复习评分")
    p_rate.add_argument("--topic", required=True)
    p_rate.add_argument("--rating", required=True, choices=list(RATING_MAP), help="again/hard/good/easy")
    p_rate.add_argument("--note", default="", help="备注(可选)")
    p_rate.set_defaults(func=cmd_rate)

    p_list = sub.add_parser("list", help="列出全部主题")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_stats = sub.add_parser("stats", help="队列统计")
    p_stats.set_defaults(func=cmd_stats)

    p_mig = sub.add_parser("migrate", help="把旧阶梯版错题队列导入 FSRS 队列(旧文件不动)")
    p_mig.set_defaults(func=cmd_migrate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
