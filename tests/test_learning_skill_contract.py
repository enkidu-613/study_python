import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATHS = [
    PROJECT_ROOT / ".codex/skills/comfortable-fast-learning-coach/SKILL.md",
    PROJECT_ROOT / ".trae/skills/comfortable-fast-learning-coach/SKILL.md",
    PROJECT_ROOT / ".reasonix/skills/comfortable-fast-learning-coach/SKILL.md",
    PROJECT_ROOT / ".reasonix/skills/comfortable-fast-learning-coach.md",
]
SESSION_PATHS = [
    PROJECT_ROOT / ".trae/memory/learning_session.json",
    PROJECT_ROOT / ".reasonix/memory/learning_session.json",
]
LEARNING_PLAN_PATH = PROJECT_ROOT / ".trae/memory/learning_plan.json"
REVIEW_QUEUE_PATHS = [
    PROJECT_ROOT / ".trae/memory/review_queue.json",
    PROJECT_ROOT / ".reasonix/memory/review_queue.json",
]


def test_learning_coach_skill_is_identical_for_all_agents():
    contents = [path.read_text(encoding="utf-8") for path in SKILL_PATHS]

    assert len(set(contents)) == 1


def test_learning_coach_contains_active_learning_contracts():
    content = SKILL_PATHS[0].read_text(encoding="utf-8")

    required_markers = [
        "三遍主动练习",
        "精力与时间门控",
        "间隔复习",
        "暂停与恢复",
        "难度自适应",
        "最多 3 个复习项",
        "独立重写",
    ]

    for marker in required_markers:
        assert marker in content


def test_learning_coach_keeps_existing_project_as_source_of_truth():
    content = SKILL_PATHS[0].read_text(encoding="utf-8")

    assert ".trae/memory/learning_plan.json" in content
    assert "不要创建第二套 `.study-config.json`" in content
    assert "不要因为学习状态变化而每轮对话自动提交 Git" in content


def test_learning_session_state_is_synced_and_resumable():
    sessions = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in SESSION_PATHS
    ]

    assert sessions[0] == sessions[1]
    learning_plan = json.loads(LEARNING_PLAN_PATH.read_text(encoding="utf-8"))
    planned_stage_ids = {stage["id"] for stage in learning_plan["stages"]}

    assert sessions[0]["stage_id"] in planned_stage_ids
    assert sessions[0]["phase"] in {
        "idle",
        "teaching",
        "practicing",
        "reviewing",
        "paused",
    }
    assert sessions[0]["pending_action"]
    assert "context" in sessions[0]
    assert "energy" in sessions[0]
    assert "time_budget_minutes" in sessions[0]


def test_review_queue_is_synced_and_has_stable_schema():
    queues = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in REVIEW_QUEUE_PATHS
    ]

    assert queues[0] == queues[1]
    assert queues[0]["version"] == "1.0"
    assert isinstance(queues[0]["items"], list)
