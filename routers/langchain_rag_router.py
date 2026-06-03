"""
LangChain RAG 路由：用框架重构手搓 RAG
======================================

本文件是"LangChain 集成"阶段的学习成果，与 rag_router.py（手搓版）并行存在，
方便对比"手搓"和"框架"的差异。

【第一课：LangChain 核心概念地图】

LangChain 不是替代你的代码，而是把你的代码打包成"乐高积木"。

核心概念（6个）：

1. Document（文档）
   类比：图书馆的索引卡片
   技术：{page_content: "文字内容", metadata: {来源, 页码}}

2. Embedding Model（嵌入模型）
   类比：翻译官，把中文翻译成"语义坐标"
   技术：把 "苹果" → [0.1, -0.3, 0.8, ...]（4096维向量）

3. VectorStore（向量数据库）
   类比：按坐标找人的导航系统
   技术：ChromaDB、Milvus、Pinecone

4. Retriever（检索器）
   类比：图书管理员
   技术：你描述需求，他去 VectorStore 找最相关的 Document

5. LLM（大语言模型）
   类比：作家
   技术：根据你给的资料写出回答

6. Chain / LCEL（链 / 表达式语言）
   类比：工厂流水线
   技术：用 "|" 管道符把上面5个串起来，一步搞定

【新旧语法对比】
旧版（RetrievalQA）：
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

新版（LCEL）：
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    # 用 "|" 像拼水管一样把步骤串起来

【与手搓版的核心差异】
| 步骤       | 手搓版 (rag_router.py)       | LangChain 版 (本文件)          |
|-----------|-----------------------------|-------------------------------|
| 文本切片    | 自己写 split_text()          | 用 TextSplitter（可选）          |
| Embedding | 自己调 client.embeddings     | 用 OpenAIEmbeddings 封装        |
| 向量存储    | 直接调 chroma_client.add()   | 用 Chroma 类封装                |
| 语义检索    | 自己调 collection.query()    | 用 retriever.invoke()           |
| 拼 Prompt | 自己拼 f-string              | 用 ChatPromptTemplate           |
| 调 LLM    | 自己调 client.chat.completions| 用 ChatOpenAI 封装              |
| 流式输出    | 自己写 SSE 格式               | 用 astream() + EventSourceResponse |
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncIterator
import json
import os

from dotenv import load_dotenv

# ========== LangChain 核心组件 ==========
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 复用现有的 ChromaDB 客户端
import chromadb

# ========== 初始化 ==========
load_dotenv()

# ModelScope API 配置
MODELSCOPE_BASE_URL = "https://api-inference.modelscope.cn/v1"
MODELSCOPE_API_KEY = os.getenv("MODELSCOPE_API_KEY")
LLM_MODEL = "deepseek-ai/DeepSeek-V3.2"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"

# ---------- 1. Embedding 模型 ----------
# 把文字变成向量的"翻译官"
embedding_model = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_base=MODELSCOPE_BASE_URL,
    openai_api_key=MODELSCOPE_API_KEY,
    # Qwen Embedding 输出 4096 维向量，确保与现有 Chroma Collection 兼容
)

# ---------- 2. LLM（大语言模型） ----------
# 负责根据资料写回答的"作家"
llm = ChatOpenAI(
    model=LLM_MODEL,
    openai_api_base=MODELSCOPE_BASE_URL,
    openai_api_key=MODELSCOPE_API_KEY,
    temperature=0.7,
    streaming=True,  # 开启流式输出
)

# ---------- 3. VectorStore（向量数据库） ----------
# 连接到现有的 ChromaDB（与手搓版共用同一个数据库文件）
chroma_client = chromadb.PersistentClient(path="./chroma_db")

vectorstore = Chroma(
    client=chroma_client,
    collection_name="documents",
    embedding_function=embedding_model,
)

# ---------- 4. Retriever（检索器） ----------
# 从 VectorStore 搜相关文档的"图书管理员"
retriever = vectorstore.as_retriever(
    search_type="similarity",      # 相似度检索
    search_kwargs={"k": 3},        # 返回前3个最相关的片段
)


# ========== 辅助函数 ==========
def format_docs(docs) -> str:
    """把检索到的 Document 列表拼成字符串，塞进 Prompt"""
    # docs 是 List[Document]，每个 Document 有 page_content 和 metadata
    formatted = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "未知来源")
        title = doc.metadata.get("title", "未命名")
        formatted.append(f"[{i}] 来源：《{title}》\n{doc.page_content}")
    return "\n\n".join(formatted)


# ========== LCEL 链定义 ==========
# 这是 LangChain 的精髓：用 "|" 管道符拼流水线

# 1. 定义 Prompt 模板（替代手搓版的 f-string）
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个基于知识库的问答助手。请严格根据下面提供的资料片段回答用户问题。

【资料片段】
{context}

【回答要求】
1. 只基于上面的资料回答，不要编造资料中没有的信息。
2. 如果资料中完全没有提到用户问题的答案，必须回答："根据现有资料无法回答该问题。"
3. 禁止猜测、禁止推理、禁止用模型自身知识补充。"""),
    ("human", "{question}"),
])

# 2. 组装 Chain（流水线）
#    RunnablePassthrough() 让用户的 question 原样通过
#    retriever | format_docs 把检索结果格式化后传给 context
rag_chain = (
    {
        "context": retriever | format_docs,      # 检索 → 格式化
        "question": RunnablePassthrough(),        # 用户问题直接通过
    }
    | RAG_PROMPT                                  # 拼成完整 Prompt
    | llm                                         # 送给 LLM 生成回答
    | StrOutputParser()                           # 把 AIMessage 转成纯字符串
)

# ========== FastAPI 路由 ==========
router = APIRouter(prefix="/langchain-rag", tags=["LangChain RAG"])


class ChatRequest(BaseModel):
    query: str
    n_results: int = 3  # 兼容手搓版参数，但实际在 retriever 里配置


@router.post("/chat", summary="LangChain RAG 问答（流式）")
async def langchain_chat(req: ChatRequest):
    """
    用 LangChain LCEL 链处理 RAG 问答，返回 SSE 流式输出。

    与手搓版 /rag/chat 的区别：
    - 手搓版：自己调 Embedding → Chroma → 拼 Prompt → OpenAI → SSE
    - 本接口：chain.astream() 一步搞定上面所有步骤
    """
    async def generate() -> AsyncIterator[str]:
        """异步生成器：调用 LCEL 链并包装为 SSE"""
        try:
            # astream() 是 LangChain 的异步流式方法
            # 它会自动：检索 → 拼 Prompt → 调 LLM → 逐字返回
            async for chunk in rag_chain.astream(req.query):
                data = {"type": "content", "content": chunk}
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

            # 结束标记
            done_data = {"type": "done"}
            yield f"data: {json.dumps(done_data, ensure_ascii=False)}\n\n"

        except Exception as e:
            error_data = {"type": "error", "content": f"LangChain 链执行出错: {str(e)}"}
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


@router.get("/health", summary="LangChain RAG 健康检查")
def health_check():
    """检查 LangChain 各组件是否正常加载"""
    try:
        # 简单测试：统计 VectorStore 里的文档数量
        count = vectorstore._collection.count()
        return {
            "status": "ok",
            "vectorstore_docs": count,
            "llm_model": LLM_MODEL,
            "embedding_model": EMBEDDING_MODEL,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
