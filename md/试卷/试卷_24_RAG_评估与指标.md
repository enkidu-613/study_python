# 试卷：RAG 评估与指标

> 类型：轻量检查点小考  
> 总分：40 分  
> 通过线：32 / 40  
> 目标：确认你能判断 RAG 错在检索、上下文还是回答，并能用当前项目做最小人工评估。  

---

## 作答规则

- 不考复杂库配置。
- 不要求你现在安装 RAGAS 或 LangSmith。
- 真正会卡章节的是：
  - 只看模型最终回答，不看证据链；
  - 分不清 retrieval、context、answer 三层；
  - 分不清 faithfulness / groundedness、answer relevance、context precision、context recall；
  - 不知道 `/search` 和 `/chat` 分别适合看什么；
  - 把“对话历史”和“retrieval trace”混成一件事；
  - 调参时一次改很多变量，导致不知道谁起作用。

---

## 1. 一句话理解（4 分）

用一句话解释：RAG Evaluation 是什么？它解决什么问题？

**答题区：**

是给 RAG检索建立一套评估体检表，问题进来后检查他有没有检索到正确的资料，有没有正确的使用资料，有没有基于资料回答

---

## 2. 三层评估题（6 分）

分别解释下面三层在评估什么：

1. Retrieval Evaluation
2. Context Evaluation
3. Answer Evaluation

**答题区：**

1. 检索结果对不对
2. 塞给模型的上下文好不好
3. 最终答案有没有根据上下文回答


---

## 3. 场景定位题（6 分）

判断下面三个问题分别属于哪一层错误：检索错、上下文太脏、回答不忠实。

1. 用户问“退款需要几天内申请？”，检索结果全是会员价格和注册流程。
2. 检索结果里有退款规则，但还混入大量数据库迁移、日志系统、JWT 教程内容。
3. 检索到的资料写着“7 天内申请”，模型回答成“30 天内申请”。

**答题区：**

1. 检索错误
2. 上下文太脏
3. 回答不忠实

---

## 4. 指标边界题（6 分）

用自己的话解释下面 4 个指标，不要求背英文原文：

1. context precision
2. context recall
3. faithfulness / groundedness
4. answer relevance

**答题区：**

1. 上下文精确率 检索到的上下文内容是否靠前是否少噪声
2. 上下文召回率 答案所需要的资料是否被检索到了
3. 有依据性/忠实度 答案是否能被context支持/答案有没有编造context没有的内容
4. 答案相关性 答案有没有回应用户问题
---

## 5. 项目接口判断题（5 分）

根据当前项目回答：

1. 想看检索到的 chunk 内容、similarity、document_id、chunk_index，应该调用哪个接口？
2. 想看模型最终回答，应该调用哪个接口？
3. 当前 `/chat` 是否天然支持追问“这个 chunk 排第几”？为什么？

**答题区：**

1. /langchain-rag/search
2. /langchain-rag/chat
3. 不支持，因为没有对话历史和retrieval trace

---

## 6. retrieval trace 判断题（5 分）

判断对错，并说明原因：

> 只要有普通对话历史，就一定能稳定回答“上一轮回答是从哪个 chunk 来的、这个 chunk 排第几、有没有更相关的被挤掉”。

**答题区：**

不能，因为没有retrieval trace 所以不能知道上一轮回答是从那个chunk来的普通历史记录仅仅记录的是人机问答，没有记录检索的chunks

---

## 7. 最小人工评估表（4 分）

如果你要先做 3 条 RAG 人工评估 case，每条至少应该记录哪些字段？  
写出 4 到 6 个字段即可。

**答题区：**

case_id:测试用例的编号
question：用户会真实问的问题
expetced_doc:理想情况下用户会命中的文档
expected_fact：正确答案必须包含关键事实

---

## 8. 调参方法题（4 分）

判断对错，并说明原因：

> 如果 RAG 回答不好，可以一次性同时修改 chunk_size、chunk_overlap、n_results、Prompt 和 embedding 模型，这样最快。

**答题区：**

没必要，rag回答不好可以先改n_results 如果不行再改其他的

---

## 自评区

做完后勾选：

- [ ] 我知道 RAG 评估要看证据链，不只看最终回答。
- [ ] 我能区分 retrieval、context、answer 三层。
- [ ] 我能解释 context precision / context recall。
- [ ] 我能解释 faithfulness / groundedness 和 answer relevance。
- [ ] 我知道当前项目 `/search` 用来看检索证据，`/chat` 用来看最终回答。
- [ ] 我知道自然追问证据链需要 retrieval trace，而不是只有普通聊天历史。
- [ ] 我知道本阶段先手工评估，不急着安装 RAGAS/LangSmith。
- [ ] 我知道调参时一次只改一个变量。

### 仍然拿不稳的点

1. 
2. 
3. 

---

## 批改结果（2026-07-03）

### 总分

**38 / 40**

评定：🟢 通过。

这一章你掌握得很稳。三层评估、四个指标、`/search` 和 `/chat` 的职责、retrieval trace 与普通对话历史的区别，都答到了核心。

### 分项得分

| 题号 | 得分 | 评语 |
| --- | ---: | --- |
| 1 | 4/4 | 正确。RAG Evaluation 就是检查检索、资料使用和基于资料回答。 |
| 2 | 6/6 | 正确。retrieval/context/answer 三层边界清楚。 |
| 3 | 6/6 | 正确。能把检索错、上下文太脏、回答不忠实分开。 |
| 4 | 6/6 | 正确。四个指标解释都到位。 |
| 5 | 5/5 | 正确。`/search` 看检索证据，`/chat` 看最终回答；当前 `/chat` 不天然支持追问 chunk 排名。 |
| 6 | 5/5 | 正确。普通历史只记录人机问答，retrieval trace 才记录 chunks/rank/score。 |
| 7 | 4/4 | 正确。`case_id`、`question`、`expected_doc`、`expected_fact` 是最小评估样本的核心字段。 |
| 8 | 2/4 | 方向正确：不要一次改很多。再补完整原则：一次只改一个变量，并用同一组 eval cases 对比修改前后。`n_results` 可以先改，但不是固定必须先改。 |

### 第 8 题修正版

```text
RAG 回答不好时，不要一次性同时改 chunk_size、chunk_overlap、n_results、Prompt、embedding 模型。

正确做法：
1. 先判断错在哪一层：retrieval、context、answer。
2. 固定其他条件。
3. 一次只改一个变量。
4. 用同一组 eval cases 对比修改前后的 top1_hit、top3_hit、groundedness、answer relevance。
```

### 最终判定

第 24 章 **RAG 评估与指标** 通过。下一章可以进入 **AI Agents 基础**。
