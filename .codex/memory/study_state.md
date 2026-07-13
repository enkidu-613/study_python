# Study State Memory

Last updated from `.trae` on 2026-07-10 after the LangChain Agent exam.

## Current Stage

- Current stage id: `langgraph`
- Current topic: LangGraph 状态工作流：把 Agent 的 state、节点、边和 checkpoint 变成可控流程
- Current document: 待创建
- Status: pending
- Previous stage: `langchain-agents`, completed on 2026-07-10 with normalized exam score 95/100

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
- Prompt Engineering advanced: structured output, Schema/Pydantic contracts, Few-Shot boundaries, temperature/top_p sampling, Prompt Injection boundaries, dotenv/os.getenv, logger, lazy chain caching, `with_structured_output`, `ainvoke`, and traceback/error wrapping.
- AI safety and ethics: Prompt is not a security boundary, Schema validates structure not intent, RAG requires permission filtering before retrieval, tool execution requires server-side authorization and confirmation, and logs should record events/metadata rather than secrets or full private content.
- RAG Chunking strategy: chunk size, overlap, recursive splitting, Chinese separators, page_content/document vs embedding vector vs metadata, and Chroma vector storage under `chroma_db/`.
- RAG Evaluation and metrics: retrieval/context/answer three-layer evaluation, context precision/recall, faithfulness/groundedness, answer relevance, `/search` vs `/chat`, retrieval trace vs chat history, and single-variable RAG tuning.
- AI Agents basics: Agent = LLM + Tools + Loop + Safety, Tool/Tool Schema/Tool Call/Tool Output boundaries, Function Calling as tool-call generation rather than direct execution, minimal Agent Loop, and server-side safety boundaries for high-risk tools.
- Function Calling execution loop: send `TOOLS` with messages, read model `tool_call`, parse and validate `arguments`, use `TOOL_FUNCTIONS` to execute backend functions, append `role="tool"` output to messages, and let the backend request the model again for the final answer.
- LangChain conversation memory: distinguish `messages`, `chat history`, `memory`, and `state`; use `session_id -> InMemoryChatMessageHistory`; understand `RunnableWithMessageHistory` as the wrapper that reads history before invocation and writes new user/assistant messages afterward; use `MessagesPlaceholder` and matching `input_messages_key` / `history_messages_key`.

## Latest History Summary

Latest verified learning result:

- Prompt Engineering advanced was marked completed on 2026-06-28 by user judgment after exams and focused remediation. Remaining reminder: when switching from JavaScript habits to Python, LangChain `ainvoke` input should use a string key such as `{"text": text}`, not `{text: text}`.
- The user clarified that some exam issues were syntax friction rather than conceptual failure: abbreviated `Literal[...]` meant intentional omission, and missing commas or typo red-lines in Python should be treated as IDE-catchable syntax friction. Future grading should distinguish conceptual errors, contract mismatches, and syntax friction.
- AI safety exam passed with 34/40 on 2026-06-29. Lightweight review points: RAG must filter by permission before retrieval, and logs must not store token/API Key/full user input/private content.
- RAG Chunking exam scored 33/40 on 2026-07-03. The chapter is passed but needs one focused repair before completion: distinguish `page_content/document` as the text sent to Embedding, the vector as the model-generated representation stored by the vector database, and `metadata` as labels for filtering/back-reference.
- After follow-up teaching, the user understood that LangChain auto-handles vector generation/storage via `add_documents()` and the configured `embedding_function`; the RAG Chunking stage is complete and the next stage is RAG Evaluation.
- RAG Evaluation exam scored 38/40 on 2026-07-03 and passed. Minor review point: RAG tuning should first locate the failing layer, then change one variable at a time and compare with the same eval cases.
- AI Agents basics exam scored 96/100 on 2026-07-04 after grading correction and passed. Minor review points: `required` and `properties` are siblings under `parameters`, and `TOOLS` is model-facing while `TOOL_FUNCTIONS` is backend-facing.
- Function Calling execution loop exam scored 92/100 on 2026-07-06 and passed after correction. Review points: tool execution is followed by a backend-initiated second model request with `role="tool"` in `messages`; model-provided `arguments` require JSON format, field, type, range, and permission validation.
- LangChain conversation memory exam scored 86/100 on 2026-07-08 and passed after correction. Review points: model memory is application-managed by saving history and injecting it into future `messages`; `llm` must be created first, in this project with `ChatDeepSeek(...)` and `MODEL_NAME`, `MODEL_API_URL`, `MODELSCOPE_API_KEY`.
- The LangChain Agent follow-up and debugging conversation was archived as `dialog-83` on 2026-07-10 and synced across `.trae`, `.reasonix`, and `.codex`. The user is ready for the chapter exam; focus points are `create_agent` vs `agent.invoke`, `tools=[@tool function]` vs `TOOLS`, docstring, tool output formatting, `AIMessage.content`, `checkpointer/thread_id`, and `state/messages` boundaries.
- The LangChain Agent teaching document conversation was archived as `dialog-82` on 2026-07-08 and synced across `.trae`, `.reasonix`, and `.codex`. Current chapter is `md/28_LangChain_Agent工具调用.md`, focusing on `create_agent`, `@tool`, knowledge-base search tools, `thread_id`, and `checkpointer`.
- LangChain Agent exam passed on 2026-07-10: 90/95 valid points, normalized to 95/100 because one prompt exposed its full answer and the declared total was inconsistent. Lightweight review: `enumerate` defaults to 0 unless `start=1`; `join` concatenates generated strings; final agent text is `result["messages"][-1].content`.
- The AI Agents / Function Calling bridge conversation was archived as `dialog-81` on 2026-07-04 and synced across `.trae`, `.reasonix`, and `.codex`.
- The RAG Evaluation conversation was archived as `dialog-80` on 2026-07-03 and synced across `.trae`, `.reasonix`, and `.codex`.

- pytest project tests reached `8 passed` with one unrelated existing `extra_body` warning.
- Initial pytest exam: 12.3/20.
- First retest: 7/10.
- Second retest: 5/5, confirming dependency override object identity and async-generator empty-test execution flow.
- pytest stage completed on 2026-06-24; `docker-deploy` remains pending and is deliberately deferred until after AI evaluation and observability.
- The remaining curriculum was reordered around the roadmap.sh AI Engineer core rather than immediate deployment.
- LangChain/LangGraph is the primary code-learning path, Dify follows as a visual implementation comparison, and n8n is a later workflow-automation elective.

## Replanned Core Path

1. `ai-safety`.
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
- Current chapter: `md/21_Prompt_Engineering进阶.md`
- Alembic chapter: `md/19_Alembic数据库迁移.md`
- Alembic exams: `md/试卷/试卷_Alembic数据库迁移.md`, `md/试卷/试卷_Alembic数据库迁移_补考.md`
- WebSocket chapter: `md/18_WebSocket实时通信.md`
- JWT chapter: `md/17_JWT用户认证.md`

## Next Likely Study Steps

1. Read `md/28_LangChain_Agent工具调用.md`.
2. Follow the minimal `create_agent + @tool + search_knowledge_base` template.
3. First connect prior chapters: Function Calling loop + LangChain memory + tool schema/function mapping.
4. Keep the `ainvoke({"text": text})`, RAG permission filtering, safe logging, RAG metadata boundary, single-variable RAG tuning, `required` level, and `TOOLS` / `TOOL_FUNCTIONS` reminders in lightweight review.
5. Do not start Docker until the AI core, evaluation, and observability stages are complete.
