# Study State Memory

Last updated from `.trae` on 2026-06-24 after the AI Engineer roadmap review.

## Current Stage

- Current stage id: `prompt-advanced`
- Current topic: advanced prompt engineering, structured output, output constraints, sampling parameters, and prompt-injection boundaries
- Current document: not written yet; the next tutorial will follow `md/20_pytest单元测试.md`
- Status: pending
- Previous stage: `pytest`, completed on 2026-06-24

## Completed Core Path

The learner has completed:

- Python basics, intermediate Python, advanced Python features.
- FastAPI basics, CRUD, SQLAlchemy ORM, dependency injection, APIRouter layering.
- Prompt engineering, chat memory, SSE streaming.
- RAG foundations: embeddings, cosine similarity, ChromaDB, dual SQLite + Chroma storage.
- FastAPI + Chroma prototype, hand-built RAG loop, context window management.
- LangChain basics: LCEL, Document, Embedding, VectorStore, Retriever, LLM, ChatDeepSeek reasoning stream.
- Async programming foundations: coroutine/task/future, gather/create_task/as_completed, Semaphore, event loop wakeup mechanics.
- JWT authentication: bcrypt, token signing/verification, Depends guards, role guards, logout blacklist, Swagger/CORS/global exception handling.
- WebSocket realtime communication: protocol upgrade, FastAPI WebSocket routes, Query token auth, room broadcast, SSE comparison, and interruptible AI stream control.
- Alembic database migrations: Poetry command usage, `target_metadata = Base.metadata`, migration vs backup, `alembic_version`, `stamp head`, empty migration causes, clean initial migration, upgrade/downgrade flow.
- pytest unit testing: Arrange/Act/Assert, TestClient, isolated test database, fixtures, dependency overrides, auth flow, WebSocket testing, SSE mock testing, and false-positive empty-test diagnosis.

## Latest History Summary

Latest verified learning result:

- pytest project tests reached `8 passed` with one unrelated existing `extra_body` warning.
- Initial pytest exam: 12.3/20.
- First retest: 7/10.
- Second retest: 5/5, confirming dependency override object identity and async-generator empty-test execution flow.
- pytest stage completed on 2026-06-24; `docker-deploy` remains pending and is deliberately deferred until after AI evaluation and observability.
- The remaining curriculum was reordered around the roadmap.sh AI Engineer core rather than immediate deployment.
- LangChain/LangGraph is the primary code-learning path, Dify follows as a visual implementation comparison, and n8n is a later workflow-automation elective.

## Replanned Core Path

1. `prompt-advanced` and `ai-safety`.
2. `rag-chunking` and `rag-evaluation`.
3. `ai-agents` using direct SDK/manual mechanics.
4. `langchain-memory`, `langchain-agents`, and `langgraph`.
5. `dify`, then advanced/multi-agent workflows.
6. `hugging-face` and `multimodal-ai`.
7. `llm-evaluation` and `llm-observability`.
8. `docker-deploy`, `frontend-basics`, and `frontend-backend`.

Later electives: vector database comparison, MCP, n8n, LlamaIndex, and fine-tuning.

## Known Weak Points

Alembic:

- Avoid calling migration a backup. A migration is a schema change script; a backup is a full database state copy including real data.
- Empty database is not enough for `upgrade head` to create tables; migration history must include `create_table`.
- Complete database moves should use database backup tools first; Alembic manages schema upgrades and small data corrections during migrations.

JWT:

- `algorithms=["HS256"]` is an algorithm allowlist. The missing keyword is algorithm confusion attack, including the `"none"` algorithm attack.
- bcrypt hash structure: `$2b$` version, cost factor, 22-character salt, 31-character hash value.

Async:

- `create_task` without awaiting can run but hide exceptions as "Task exception was never retrieved".
- `gather(return_exceptions=True)` returns exceptions as values; check with `isinstance(result, Exception)`.
- Future is a one-shot result placeholder; Task is a Future that actively runs a coroutine.
- `run_in_executor` is the bridge for synchronous blocking calls inside async code.

RAG:

- `enumerate(start=1)` creates source numbers like `[1]` for LLM/user citation.
- `yield` streams chunks; `return` waits and returns once.

WebSocket:

- Watch Python-vs-JavaScript syntax slips: Python uses `!=`, not `!==`.
- True room grouping uses `dict[str, list[WebSocket]]`.

## Teaching Preferences

- ADHD-friendly but precise: analogy first only when useful, then exact mechanism.
- The user benefits from short sections, tables, runnable templates, and explicit "copy this pattern" guidance.
- Do not optimize for memorization. Optimize for: idea, use case, reason, and template location.
- For commands, exact spelling does not need to be memorized when the user says they can check docs; concept and safe workflow matter more.

## Important Project Files

- Learning plan: `.trae/memory/learning_plan.json`
- History index: `.trae/memory/learning_history_index.json`
- Mistake book: `md/错题本.md`
- Current chapter: `md/20_pytest单元测试.md`
- Alembic chapter: `md/19_Alembic数据库迁移.md`
- Alembic exams: `md/试卷/试卷_Alembic数据库迁移.md`, `md/试卷/试卷_Alembic数据库迁移_补考.md`
- WebSocket chapter: `md/18_WebSocket实时通信.md`
- JWT chapter: `md/17_JWT用户认证.md`

## Next Likely Study Steps

1. Keep pytest patterns available for future regression tests instead of expanding this chapter further.
2. Write and study the next chapter for `prompt-advanced`.
3. Do not start Docker until the AI core, evaluation, and observability stages are complete.
