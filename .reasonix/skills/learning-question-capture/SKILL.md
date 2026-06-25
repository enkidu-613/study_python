---
name: learning-question-capture
description: Use when the user asks a learning question, says they do not understand, asks why/how a concept works, compares concepts across languages or frameworks, or requests that Q&A be recorded for later reinforcement. Captures compact learning questions and answers, then syncs them across .codex, .trae, and .reasonix.
---

# Learning Question Capture

Record the user's chapter-level confusion as a compact reinforcement item after answering it. This skill is for durable learning memory, not full transcript archiving.

## Trigger

Use this skill when the user:

- asks a conceptual learning question;
- says "不懂", "没懂", "为什么", "区别是什么", "作用是什么";
- compares a new concept with something they already know;
- asks to preserve Q&A for later review;
- exposes a misunderstanding that should become a future review item.

Do not record trivial shell commands, Git operations, pure status updates, installation chores, or casual non-learning chat unless the user explicitly asks.

## Strict Exclusions

Do not record these into `learning_questions`, even if they are phrased as a question:

- skill architecture, skill merging, or skill boundary discussions;
- history archiving strategy, sync policy, or memory-file organization;
- Git, push, commit, branch, or repository management questions;
- plugin/tool installation, agent configuration, or workspace policy decisions;
- project-management decisions that are not a technical concept the user needs to review.

If such a discussion should be preserved, put it in normal history archiving instead of the learning question bank.

## Source Of Truth

Write first to:

- `.trae/memory/learning_questions/YYYY-MM.md`

Then mirror the same content to:

- `.reasonix/memory/learning_questions/YYYY-MM.md`
- `.codex/memory/learning_questions/YYYY-MM.md`

The three files must contain the same entry text. `.trae` remains the learning source of truth.

## Workflow

1. Answer the user's question first in the normal teaching style.
2. Decide whether the question is worth future reinforcement.
3. Determine chapter/topic from the current conversation or nearby docs. If unsure, use `chapter: 未归属`.
4. Append one compact entry to the monthly question file.
5. Mirror the exact entry to `.reasonix` and `.codex`.
6. Verify the entry can be found in all three agent folders.

## Entry Format

Use this Markdown shape:

```markdown
### YYYY-MM-DD HH:mm - <topic> - <short title>

- id: lq-YYYYMMDD-HHMM-<short-slug>
- chapter: <chapter path or 未归属>
- question: <the user's question in one sentence>
- answer_summary: <the answer compressed into 2-4 sentences>
- exact_rule: <one copyable rule the user should remember>
- reinforce_prompt: <one short future recall question>
- status: active
```

Keep entries short. Do not paste the full conversation unless the user asks for full archival.

## Quality Rules

- Prefer "what confused the user" over "what was discussed".
- Only record items that can become a future recall question, mistake review, or chapter exam patch.
- Store the corrected mental model, not just a definition.
- If the user mixed two concepts, name both and record the boundary.
- If the topic belongs to a chapter, include the chapter file path.
- Use `status: active` until the user later proves mastery in review or exam.
- Do not create a second learning workspace.
- Do not auto-commit after recording.

## Example

```markdown
### 2026-06-26 15:40 - Prompt Engineering - Few-Shot 不是训练

- id: lq-20260626-1540-few-shot-not-training
- chapter: md/21_Prompt_Engineering进阶.md
- question: Few-Shot 为什么不是训练，模型为什么还能记住示例？
- answer_summary: Few-Shot 示例只是本次 Prompt 的上下文，不会修改模型参数。模型不是永久记住示例，而是当次请求里读到了示例并模仿。
- exact_rule: Few-Shot = 本次 Prompt 里的临时例题；Fine-Tuning = 用训练数据改变模型参数。
- reinforce_prompt: 用一句话区分 Few-Shot 和 Fine-Tuning。
- status: active
```
