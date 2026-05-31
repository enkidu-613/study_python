# 13. RAG 闭环：从检索到回答

> 目标：把"能检索到片段"和"能调大模型"两个独立能力串成一条链，实现真正的知识库问答。

---

## 本章地图

```
上一章：FastAPI + Chroma 最小原型（双存储 API 化）
        ↓
本章：  手搓最小 RAG 闭环
        ├── 为什么需要闭环？
        ├── 上下文 Prompt 拼接
        ├── 引用溯源设计
        ├── 复用检索逻辑（内部函数）
        └── 流式调用 LLM
        ↓
下一章：LangChain 框架集成（用框架替代手搓）
```

---

## 1. 为什么要做这一步？

### 上一章的问题

`rag_router.py` 有两个接口，但它们是**割裂的**：

- `POST /rag/documents` → 存文档 ✅
- `POST /rag/search` → 返回检索片段 ✅
- **但没有接口能把检索结果喂给 LLM，让 LLM 基于资料回答**

### 用户想要的是什么？

用户不会直接看一堆检索片段自己总结。用户想要的是：

```
用户问："Python 怎么做 Web 开发？"

系统答："根据《Python编程语言介绍》第0段，Python 广泛应用于 Web 开发领域，
        常用的框架有 Django 和 Flask [来源：《Python编程语言介绍》第0段]。"
```

这就是 **RAG 闭环**：检索 → 拼 Prompt → 调 LLM → 回答。

---

## 2. 核心概念

### 概念 1：上下文 Prompt 拼接

**问题**：LLM 不知道你知识库里有什么，你必须把检索到的片段塞进对话里。

**做法**：把检索结果格式化后放进 `messages` 的 `system` 角色中：

```python
messages = [
    {"role": "system", "content": "你是一个助手。基于以下资料回答：\n[1] ...\n[2] ..."},
    {"role": "user", "content": "用户的问题"}
]
```

**为什么放 system 里？**

因为 `system` 角色的权重最高，LLM 会把它当作"必须遵守的指令"。如果放 `user` 里，LLM 可能把资料当成普通对话内容，不够重视。

### 概念 2：引用溯源

**问题**：LLM 回答得很像编的，用户不知道它到底有没有依据。

**做法**：在 system prompt 里明确要求 LLM 标注来源：

```
如果引用了某个片段，请在回答末尾标注来源，格式如：[来源：《标题》第N段]
```

**原理**：LLM 看到 `[1] 来源：《xxx》` 这种编号，会自然地在回答末尾复用这个格式。

### 概念 3：内部函数复用

**问题**：`search` 路由和 `rag_chat` 路由都需要做检索，代码会重复。

**做法**：把检索逻辑抽成 `_semantic_search()` 内部函数：

```
search 路由 ──→ _semantic_search()
rag_chat 路由 ──→ _semantic_search()
```

**好处**：改检索逻辑只需改一个地方，两个接口自动同步。

### 概念 4：流式返回

**问题**：LLM 思考过程可能很慢，用户盯着空白页面等很久。

**做法**：复用 `ai_router.py` 的 SSE 流式返回，让用户看到 LLM 在"逐字思考"。

---

## 3. 代码变更总览

在 `routers/rag_router.py` 中新增 4 个部分：

| 新增内容 | 作用 | 对应知识点 |
|:---|:---|:---|
| `_semantic_search()` | 可复用的检索逻辑 | 概念 3：内部函数复用 |
| `build_system_prompt()` | 把检索结果拼成 system prompt | 概念 1：上下文 Prompt 拼接 |
| `generate_rag_stream()` | 异步流式调用 LLM | 概念 4：流式返回 |
| `rag_chat` 路由 | 对外暴露 POST /rag/chat | 全流程闭环 |

同时修改 `search` 路由，让它调用 `_semantic_search()`，自身只负责 HTTP 层。

---

## 4. 逐段详解

### 4.1 `_semantic_search()` —— 内部检索函数

```python
def _semantic_search(query_text: str, n_results: int, db: Session) -> List[SearchResult]:
    # 1. 查询转向量
    query_vec = get_embedding(query_text)

    # 2. ChromaDB 检索
    chroma_results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    # 3. 回查 SQLite，组装结果
    results = []
    for i in range(n_results):
        ...
    return results
```

**与原来 `search()` 的区别**：

| | 原来的 `search()` | `_semantic_search()` |
|:---|:---|:---|
| 参数 | `query: SearchIn` | `query_text: str, n_results: int, db: Session` |
| 调用方 | HTTP 请求 | 内部函数/路由 |
| 返回 | `List[SearchResult]` | `List[SearchResult]` |

**为什么参数变了？**

内部函数不需要关心 HTTP 请求格式（`SearchIn` Pydantic 模型），直接接收字符串和数字更灵活。

### 4.2 `build_system_prompt()` —— Prompt 模板

```python
def build_system_prompt(results: List[SearchResult]) -> str:
    # 空结果处理
    if not results:
        return "没有检索到与用户问题相关的资料..."

    # 格式化每个片段
    context_blocks = []
    for i, r in enumerate(results, start=1):
        block = f"[{i}] 来源：《{r.title}》第{r.chunk_index}段（相关度：{r.similarity:.2f}）\n{r.chunk_content}"
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    # 拼接完整 prompt
    prompt = f"""你是一个基于知识库的问答助手...

【资料片段】
{context}

【回答要求】
1. 只基于上面的资料回答...
2. 如果资料不足...
3. 如果引用了某个片段，请标注来源...
4. 保持简洁清晰。"""

    return prompt
```

**三个关键设计**：

1. **空结果兜底**：检索不到时给 LLM 一个明确的"拒绝回答"指令，防止 LLM 瞎编。

2. **编号制式化**：`[1]`、`[2]` 让 LLM 能明确区分不同片段，也方便后续要求它标注来源。

3. **相关度提示**：`（相关度：0.82）`给 LLM 一个参考，帮助它判断哪个片段更可靠（虽然 LLM 不一定真的会用）。

### 4.3 `generate_rag_stream()` —— 流式生成器

```python
async def generate_rag_stream(query: str, results: List[SearchResult]):
    system_prompt = build_system_prompt(results)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-V3.2',
        messages=messages,
        stream=True,
        extra_body={"enable_thinking": True}
    )

    for chunk in response:
        ...
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
```

**与 `ai_router.py` 的 `generate_stream()` 的唯一区别**：

```python
# ai_router.py
messages = [{'role': 'user', 'content': message}]   # ← 没有 system prompt

# rag_router.py
messages = [
    {"role": "system", "content": system_prompt},   # ← 动态拼接了检索结果
    {"role": "user", "content": query}
]
```

**思考过程 vs 正式回答**：

因为 `extra_body={"enable_thinking": True}`，DeepSeek-V3.2 会先输出思考过程（`reasoning_content`），再输出正式回答（`content`）。代码中用 `type: "thinking"` 和 `type: "answer"` 区分，中间用 `type: "divider"` 做分隔线。

### 4.4 `rag_chat` 路由 —— 对外接口

```python
@router.post("/chat", summary="RAG 知识库问答")
async def rag_chat(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. 检索
    results = _semantic_search(req.query, req.n_results, db)

    # 2. 流式返回 LLM 回答
    return StreamingResponse(
        generate_rag_stream(req.query, results),
        media_type="text/event-stream"
    )
```

**为什么 `async`？**

因为 `generate_rag_stream` 是异步生成器（用了 `async def` + `yield`），路由函数也要是 `async` 才能匹配。

**三步合一**：

```
① _semantic_search()     → 检索
② build_system_prompt()   → 拼 Prompt
③ generate_rag_stream()   → 调 LLM 流式返回
```

---

## 5. Prompt 模板实际效果

假设用户问 `"Python 怎么做 Web 开发？"`，检索到 2 个片段，实际传给 LLM 的 system prompt 是这样的：

```
你是一个基于知识库的问答助手。请严格根据下面提供的资料片段回答用户问题。

【资料片段】
[1] 来源：《Python编程语言介绍》第0段（相关度：0.82）
Python 广泛应用于 Web 开发、数据分析、人工智能等领域。

[2] 来源：《Django框架入门》第1段（相关度：0.76）
Django 是 Python 最流行的 Web 框架，提供了完整的 MVC 架构...

【回答要求】
1. 只基于上面的资料回答，不要编造资料中没有的信息。
2. 如果资料不足以回答问题，请明确说明"根据现有资料无法回答"。
3. 如果引用了某个片段，请在回答末尾标注来源，格式如：[来源：《标题》第N段]
4. 保持简洁清晰。
```

LLM 看到 `[1]`、`[2]` 和回答要求第 3 条，就会在回答末尾自动追加 `[来源：《xxx》第N段]`。

---

## 6. 数据流图

```
用户 POST /rag/chat
{
  "query": "Python 怎么做 Web 开发？",
  "n_results": 3
}
        ↓
┌─────────────────┐
│ rag_chat 路由    │
│ ① 调 _semantic_search()
└────────┬────────┘
         ↓
┌─────────────────┐
│ Embedding 转向量 │
│ ChromaDB 检索    │
│ SQLite 回查      │
│ 返回 SearchResult 列表
└────────┬────────┘
         ↓ [List[SearchResult]]
┌─────────────────┐
│ build_system_prompt()
│ 把片段拼进 system prompt
└────────┬────────┘
         ↓ [str: system_prompt]
┌─────────────────┐
│ generate_rag_stream()
│ 调 LLM，stream=True
│ yield SSE 数据包
└────────┬────────┘
         ↓ [SSE stream]
StreamingResponse → 用户看到逐字生成的回答
```

---

## 7. 接口对比

| 接口 | URL | 输入 | 输出 | 是否调 LLM |
|:---|:---|:---|:---|:---|
| 存入文档 | `POST /rag/documents` | `{title, content, source}` | 存入成功信息 | ❌ |
| 语义检索 | `POST /rag/search` | `{query, n_results}` | 检索片段列表 | ❌ |
| **RAG 问答** ⭐ | **`POST /rag/chat`** | **`{query, n_results}`** | **AI 回答（带引用标注）** | ✅ |

---

## 8. 测试方法

### 第 1 步：确认知识库有数据

如果之前没存过文档，先用 `/rag/documents` 存一篇，或者运行 `dual_storage_demo.py`（数据会写到同一个 `./chroma_db` 持久化目录）。

### 第 2 步：启动服务

```bash
cd /Users/enkidu/PyCharmMiscProject
poetry run python main.py
```

### 第 3 步：curl 测试

```bash
curl -X POST http://127.0.0.1:8000/rag/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Python 怎么做 Web 开发？", "n_results": 3}'
```

**期望输出**：流式返回，先看到思考过程，再看到正式回答，末尾带 `[来源：《xxx》第N段]`。

### 第 4 步：浏览器测试

打开 `http://127.0.0.1:8000/docs`，找到 `/rag/chat`，点"Try it out"直接测试。

---

## 9. 常见问题

### Q1：LLM 不标注来源怎么办？

**原因**：Prompt 里的要求不够强，或者 LLM 模型比较小不太听话。

**解决**：在 `build_system_prompt` 的回答要求里加一句：
```
3. 【强制】每段回答末尾必须标注来源，格式：[来源：《标题》第N段]。不标注来源的回答不合格。
```

### Q2：检索结果太长，LLM 报上下文超限？

**原因**：3 个片段 × 80 字 + Prompt 模板 + 用户问题，可能超过模型上下文上限。

**解决**：降低 `n_results`（从 3 改到 2），或者缩小 `chunk_size`（从 80 改到 50）。下一章会学更精确的 token 数管理。

### Q3：空结果时 LLM 还是瞎编？

**原因**：Prompt 里写的是"请礼貌地告诉用户"，LLM 可能理解为"你可以编造一个礼貌的说法"。

**解决**：Prompt 写得更强硬：
```
没有检索到与用户问题相关的资料。你的唯一回复必须是："根据现有资料无法回答该问题。"
```

---

## 10. 下一步预告

本章是**手搓** RAG 闭环——自己写检索、自己拼 Prompt、自己调 LLM。

下一章进入 **LangChain 框架**，你会学到：
- LangChain 已经封装好了 `RetrievalQA` 链，一行代码就能实现本章的所有功能
- 但手搓一遍再看框架，才能理解框架在帮你做什么、省略了什么
- 以及框架的局限：什么时候该用手搓，什么时候该用框架
