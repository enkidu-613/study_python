# Refresh Current AI Course References Implementation Plan

> **For agentic workers:** Use the relevant course QA and source-verification skills while implementing this plan. Steps use checkbox syntax for tracking.

**Goal:** Update only the course notes whose version guidance is now stale, without changing the project's pinned dependencies.

**Architecture:** Keep the course's provider-neutral learning path intact. Make MCP SDK v2 the current Chapter 49 path while preserving v1 as a migration note, and add concise version-boundary notes for LangChain and FastAPI.

**Tech Stack:** Markdown course notes, Poetry lockfile as read-only version evidence, official MCP/LangChain/FastAPI documentation.

**Spec:** User approved the prior audit recommendations in chat on 2026-10-09.

## Global Constraints

- Do not alter `pyproject.toml` or `poetry.lock` in this task.
- Preserve existing user-authored, untracked course documents and unrelated working-tree changes.
- Base API/version claims on current official documentation and identify version-sensitive behavior.
- Keep the explanation accessible to a learner who has not yet studied MCP.

## Review Focus

- MCP v2 API examples match the current official import path and class names.
- MCP v1 remains clearly identified as a legacy, still-maintained line rather than mixed into v2 code.
- FastAPI OpenTelemetry behavior is not implied to exist in the project's pinned version.
- LangChain documentation version text matches the lockfile, without forcing a dependency upgrade.

### Task 1: Refresh MCP chapter

**Files:** Modify `md/49_MCP_Server与Agent工具权限.md`.

- [x] Replace the primary example with MCP Python SDK v2 `MCPServer` usage and current installation guidance.
- [x] Explain the current protocol revision at a beginner-appropriate level; keep v1 import/install as a clearly separate legacy note.
- [x] Review links and learning goals for consistency with the new example.

### Task 2: Correct version boundaries

**Files:** Modify `md/28_LangChain_Agent工具调用.md`, `md/40_LLM可观测性_本地日志.md`, and `md/41_LangSmith_追踪实践.md`.

- [x] Update Chapter 28's LangChain version statement to match `poetry.lock`; mention newer MCP integration only as optional and version-sensitive.
- [x] Add a compact note that native FastAPI OpenTelemetry support is newer than the pinned project version and requires version-specific configuration.

### Task 3: Verify the edits

**Files:** Review the four modified course documents and the plan.

- [x] Check Markdown structure, links, code import paths, and that no locked dependency files changed.
- [x] Report which commands/examples were verified from official docs versus not executed locally.
