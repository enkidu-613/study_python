# Study State Memory

Last migrated from `.trae` on 2026-06-13.

## Current Stage

- Current stage id: `websocket-realtime`
- Current topic: WebSocket realtime communication
- Current document: `md/18_WebSocket实时通信.md`
- Status: in progress
- Previous stage: `jwt-auth` completed on 2026-06-12

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

## Latest History Summary

Latest `.trae/memory/learning_history_index.json` entries say:

- `dialog-56` on 2026-06-12 started WebSocket learning and created `md/18_WebSocket实时通信.md`.
- JWT补考 scored 6.25/7 (89%): nearly passed, with one remaining weak point.
- `dialog-55` and `dialog-54` covered SHA-256 token hashes, blacklists, `jwt.decode`, `alg:none`, role guards, and JWT statelessness.

## Known Weak Points

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

## Teaching Preferences

- ADHD-friendly but precise: analogy first only when useful, then exact mechanism.
- The user benefits from short sections, tables, runnable templates, and explicit "copy this pattern" guidance.
- Do not optimize for memorization. Optimize for: idea, use case, reason, and template location.

## Important Project Files

- Learning plan: `.trae/memory/learning_plan.json`
- History index: `.trae/memory/learning_history_index.json`
- Mistake book: `md/错题本.md`
- Current chapter: `md/18_WebSocket实时通信.md`
- JWT chapter: `md/17_JWT用户认证.md`
- JWT exams: `md/试卷/试卷_JWT认证.md`, `md/试卷/试卷_JWT认证_补考.md`

## Next Likely Study Steps

1. Run the FastAPI WebSocket minimum template: `accept -> receive_text -> send_text`.
2. Compare WebSocket with SSE in the project’s AI streaming routes.
3. Add JWT-style authentication to a WebSocket endpoint using query token or first-message auth.
4. Build an interruptible AI chat flow with one reader task and one generator task.
