# Chapter 32 Hugging Face Learning Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revise Chapter 32 so the learner first writes and verifies a minimal Hugging Face embedding loader, then understands the AI-generated project wrapper without being expected to reproduce its advanced hardware code.

**Architecture:** Keep all teaching content in `md/32_HuggingFace生态.md`. Reorder the chapter around one local embedding path, use `app/embedding.py` as a code-reading target, then add ecosystem boundaries and three-pass practice.

**Tech Stack:** Markdown, Python 3.12, Poetry, sentence-transformers 5.5.1, transformers 5.9.0, huggingface-hub 1.15.0

## Global Constraints

- Modify only `md/32_HuggingFace生态.md`.
- Do not modify `app/embedding.py`, earlier chapters, exams, mistake records, or learning state.
- Treat AI-generated project code as existing project infrastructure, not proof of learner mastery.
- Require independent mastery only for the minimal model-loading and encoding path.
- Use the current project implementation and locked dependency versions as the executable baseline.

---

### Task 1: Rebuild the local embedding learning path

**Files:**
- Modify: `md/32_HuggingFace生态.md`

**Interfaces:**
- Consumes: `SentenceTransformer(model_id, device=...)`, `model.encode(text, convert_to_numpy=True)` and the current `app.embedding` call chain.
- Produces: A runnable minimal example, a real project code map, and explicit mastery boundaries.

- [ ] **Step 1: Replace the assumed-prior-knowledge opening**

State explicitly that `app/embedding.py` was AI-assisted project infrastructure. Explain that running `get_embedding()` proves the wrapper works, while independently writing the minimal loader proves learner mastery.

- [ ] **Step 2: Add first-use dependency orientation**

Document these exact roles and installed versions:

```text
sentence-transformers 5.5.1: direct project dependency; high-level sentence embedding API
transformers 5.9.0: current transitive dependency; pipeline and lower-level model APIs
huggingface-hub 1.15.0: current transitive dependency; Hub downloads, cache, tokens and InferenceClient
```

Explain that a package used as a stable project API should normally become a direct Poetry dependency.

- [ ] **Step 3: Add the minimal handwritten loader**

Use this runnable shape:

```python
from sentence_transformers import SentenceTransformer

model_id = "BAAI/bge-base-zh-v1.5"
model = SentenceTransformer(model_id, device="cpu")
embedding = model.encode(
    "退款需要几天内申请？",
    convert_to_numpy=True,
)

print(type(embedding).__name__)
print(embedding.shape)
print(embedding[:5])
```

Explain the runtime chain `model_id -> model object -> encode -> ndarray` and use CPU in the learning snippet for portability.

- [ ] **Step 4: Map the real project wrapper**

Teach this exact sequence:

```text
TIER_DISPATCH
  -> _detect_device()
  -> _get_model_name()
  -> _load_model()
  -> get_embedding_model()
  -> get_embedding() / get_embeddings()
```

Classify `SentenceTransformer(...)`, `encode(...)`, and a minimal wrapper as “must write”; model selection, caching, and batching as “must understand”; cross-platform detection, locking, and fallback as “recognize only”.

- [ ] **Step 5: Verify project links and claims**

Run:

```bash
rg -n "TIER_DISPATCH|def _detect_device|def _get_model_name|def _load_model|def get_embedding_model|def get_embedding" app/embedding.py
```

Expected: every function named in the chapter exists in `app/embedding.py`.

### Task 2: Add model consistency and ecosystem boundaries

**Files:**
- Modify: `md/32_HuggingFace生态.md`

**Interfaces:**
- Consumes: the local embedding path from Task 1.
- Produces: model-selection rules, cache/revision guidance, remote-inference boundaries, and active practice.

- [ ] **Step 1: Add vector compatibility rules**

Document these current dimensions:

```text
BAAI/bge-small-zh-v1.5 = 512
BAAI/bge-base-zh-v1.5 = 768
BAAI/bge-large-zh-v1.5 = 1024
```

State the exact rule: indexing and querying must use the same model ID, revision, dimension, and preprocessing; changing any of these requires evaluation and normally re-embedding the collection.

- [ ] **Step 2: Add BGE usage and cache guidance**

Explain the optional short-query retrieval instruction, `normalize_embeddings=True`, `HF_HOME`, `HF_HUB_CACHE`, `HF_TOKEN`, model revision pinning, and the fact that module-level `_model` is process-local.

- [ ] **Step 3: Keep ecosystem examples behind the main path**

Keep `pipeline()` as an optional task-pipeline recognition exercise. Keep `InferenceClient` as remote HTTP inference and distinguish chat completion from TEI-style feature extraction.

- [ ] **Step 4: Replace passive practice with three runnable passes**

Require:

```text
Read: trace input, call and output through the minimal loader.
Follow-write: fill model_id and encode arguments, then run and inspect shape.
Independent rewrite: implement get_embedding_demo(text) without viewing the answer and verify two inputs have equal dimensions but different values.
```

- [ ] **Step 5: Run documentation verification**

Run:

```bash
poetry run python -c "import sentence_transformers, transformers, huggingface_hub; print(sentence_transformers.__version__, transformers.__version__, huggingface_hub.__version__)"
poetry run python -c "from sentence_transformers import SentenceTransformer; print(SentenceTransformer.__name__)"
git diff --check -- md/32_HuggingFace生态.md
rg -n "AI.*生成|独立重写|模型 ID.*revision.*维度.*预处理|只需识别" md/32_HuggingFace生态.md
```

Expected: imports succeed with the documented versions, the class name prints, the Markdown diff has no whitespace errors, and all required teaching markers are present.
