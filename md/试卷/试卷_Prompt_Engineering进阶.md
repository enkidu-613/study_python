# 试卷：Prompt Engineering 进阶

> 章节：`md/21_Prompt_Engineering进阶.md`  
> 状态：待作答  
> 规则：不查答案，允许查项目代码和本章讲义；写不准的地方直接标注“拿不稳”。  
> 目标：确认你能把 LLM 从聊天能力接入稳定的工程接口。

---

## 第一轮：核心概念题（40 分）

### 1. Prompt + Pydantic 双保险（8 分）

用自己的话解释：

- Prompt 在结构化输出里解决什么问题？
- Pydantic 在结构化输出里解决什么问题？
- 为什么只靠 Prompt 不够？

**答题区：**


---

### 2. Schema 类是什么（6 分）

解释“输出 Schema 类”是什么，并说明它和 Prisma schema 的共同思想与区别。

**答题区：**


---

### 3. Few-Shot 不是训练（6 分）

解释 Few-Shot 为什么不是训练模型。模型为什么还能参考示例输出？

**答题区：**


---

### 4. 任务提取器 vs 任务规划器（6 分）

下面这句话：

```text
明天下午提交周报，这是高优先级工作
```

分别写出“任务提取器”和“任务规划器”可能输出什么，并说明二者边界。

**答题区：**


---

### 5. temperature 与 top_p（8 分）

判断并解释：

```text
temperature 控制模型是否严格遵守 Prompt。
top_p 控制关键词提取准确度。
```

这句话对吗？如果不对，正确理解是什么？

**答题区：**


---

### 6. Prompt Injection 边界（6 分）

为什么 `<user_text>...</user_text>` 和 Human 消息只能降低风险，不能当成真正的安全沙箱？真正的权限边界应该放在哪里？

**答题区：**


---

## 第二轮：代码机制题（35 分）

### 7. `with_structured_output()` 做了什么（7 分）

根据本章代码，解释：

```python
llm.with_structured_output(TaskExtractionResult, method="json_mode")
```

背后大概做了哪几件事？

**答题区：**


---

### 8. `load_dotenv()` 与 `os.getenv()`（6 分）

解释下面三者之间的关系：

```text
.env
load_dotenv()
os.getenv()
```

特别说明：`os` 是如何拿到 `.env` 里的值的？

**答题区：**


---

### 9. `logger = logging.getLogger(__name__)`（5 分）

这行代码做了什么？为什么常用 `__name__`？

**答题区：**


---

### 10. `_task_extractor` 惰性单例（7 分）

解释下面代码的目的：

```python
_task_extractor = None

def get_task_extractor():
    global _task_extractor
    if _task_extractor is None:
        _task_extractor = build_task_extractor()
    return _task_extractor
```

如果每次请求都直接调用 `build_task_extractor()`，会有什么问题？

**答题区：**


---

### 11. `ainvoke()` 参数流（6 分）

解释：

```python
await chain.ainvoke({"text": text})
```

这行不是“只传参”，它实际执行了哪些步骤？

**答题区：**


---

### 12. `except Exception as exc` 与 `from exc`（4 分）

解释：

```python
except Exception as exc:
    logger.exception("Error extracting task from text: %s", exc)
    raise HTTPException(status_code=502, detail="结构化输出生成失败") from exc
```

`exc` 是什么？`from exc` 保留了什么信息？

**答题区：**


---

## 第三轮：实战设计题（25 分）

### 13. 设计 `classify-feedback` 的输出 Schema（8 分）

根据第七关需求，写出一个 Pydantic 输出 Schema：

- `category`: 只能是 `bug` / `feature` / `praise`
- `urgency`: 只能是 `low` / `medium` / `high`
- `summary`: 字符串，一句话摘要

只写 Schema 类即可。

**答题区：**

```python

```

---

### 14. 根据 Schema 反推 Prompt（9 分）

为 `classify-feedback` 写一个 `ChatPromptTemplate.from_messages(...)` 的 Prompt 骨架。

要求：

- 有 system 角色；
- 用 `<user_text>` 隔离用户输入；
- 明确 `category`、`urgency`、`summary` 的字段规则；
- 至少写一个 `human -> ai` Few-Shot 示例；
- 最后一条 human 使用真实输入占位符。

**答题区：**

```python

```

---

### 15. 错误调试路线（4 分）

如果你调用接口后看到 Python traceback，你应该先看哪里？再看哪里？为什么？

**答题区：**


---

### 16. HTTP 状态码判断（4 分）

下面三种错误分别更适合返回什么状态码？简述原因。

1. 请求体 `text` 是空字符串。
2. 模型服务不可用。
3. 模型返回了不符合 Schema 的 JSON。

**答题区：**


---

## 自评区

做完后自己标记：

- [ ] 我能说清本章的工作思想：让模型输出能被程序稳定消费。
- [ ] 我能区分 Prompt、Few-Shot、Schema、Pydantic 的职责。
- [ ] 我能解释 `chain.ainvoke(input)` 的完整执行链路。
- [ ] 我能独立仿写 `classify-feedback` 的 Schema + Prompt + Chain + Endpoint。
- [ ] 我知道哪些问题是 Prompt 能降低风险，哪些必须由服务端代码控制。

### 拿不稳的点

写下 1-3 个你做题时最不确定的地方：

1. 
2. 
3. 
