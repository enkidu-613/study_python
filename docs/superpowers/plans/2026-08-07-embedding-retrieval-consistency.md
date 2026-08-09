# Embedding Retrieval Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local BGE embeddings consistent across hardware while separating query and document encoding according to the model's retrieval contract.

**Architecture:** Keep `app/embedding.py` as the single model-loading boundary. Route query and document text through separate public functions, share one normalized encoder, and preserve the configured model when falling back from an accelerator to CPU.

**Tech Stack:** Python 3.12, PyTorch, sentence-transformers, LangChain Core, ChromaDB, pytest

## Global Constraints

- Use `BAAI/bge-small-zh-v1.5` as the hardware-independent default model.
- Apply the Chinese BGE retrieval instruction only to query text.
- Normalize both query and document embeddings.
- Existing Chroma indexes must be rebuilt after this behavior change.
- Do not modify unrelated dirty files.

---

### Task 1: Lock the embedding contract with tests

**Files:**
- Create: `tests/test_embedding.py`
- Test: `tests/test_embedding.py`

**Interfaces:**
- Produces: expected behavior for `get_query_embedding`, `get_document_embedding`, `get_document_embeddings`, `_get_batch_size`, and CPU fallback.

- [x] Write failing tests using a fake `SentenceTransformer` so tests never download model weights.
- [x] Run `poetry run pytest tests/test_embedding.py -q` and verify failures describe the missing query/document contract.

### Task 2: Implement the consistent embedding boundary

**Files:**
- Modify: `app/embedding.py`
- Modify: `.env.example`
- Test: `tests/test_embedding.py`

**Interfaces:**
- Produces: `get_query_embedding(text: str) -> list[float]`, `get_document_embedding(text: str) -> list[float]`, and `get_document_embeddings(texts: list[str]) -> list[list[float]]`.
- Preserves: `get_embedding` and `get_embeddings` as document-side compatibility aliases.

- [x] Fix the default model so hardware only controls device and batch size.
- [x] Add shared normalized encoding and query-only instruction preparation.
- [x] Validate text and batch-size configuration.
- [x] Make accelerator failure retry the same model on CPU.
- [x] Return concise actual configuration from `model_info()`.
- [x] Run `poetry run pytest tests/test_embedding.py -q` and verify all tests pass.

### Task 3: Connect the correct APIs to RAG

**Files:**
- Modify: `app/routers/rag.py`
- Test: `tests/test_embedding.py`

**Interfaces:**
- Consumes: document and query embedding functions from Task 2.
- Produces: document chunks encoded without query instruction and searches encoded with it.

- [x] Replace ambiguous `get_embedding` calls with the correct query/document functions.
- [x] Run focused tests and a Python import check.

### Task 4: Rewrite chapter 32 gate three

**Files:**
- Modify: `md/32_HuggingFace生态.md`

**Interfaces:**
- Documents: the two real call chains, shared model cache, normalization, query instruction boundary, same-model CPU fallback, and index rebuild requirement.

- [x] Replace the current third gate with an action-first walkthrough matching the final code.
- [x] Explain every newly introduced function and configuration beside its first example.
- [x] Run heading/link marker checks and `git diff --check`.
