"""
LangChain RAG 路由：纯 LangChain 原生实现
==========================================

完整替代 rag_router.py（手搓版）的所有接口，尽可能使用 LangChain 原生功能。
不可替代的部分（Token 估算、SQLite 存储）保留推荐实现。

【代码结构：从下往上读】
第1层：工具函数       → estimate_tokens()、format_docs()、truncate_context()
第2层：数据层函数     → 操作 SQLite 和 ChromaDB 的原子函数
第3层：业务层函数     → 组合多个数据层函数完成完整业务
第4层：表现层函数     → SSE 流式输出、LCEL 链构建
第5层：路由接口       → 最薄的一层，只做参数校验和函数编排

【接口对照】
| 手搓版接口                    | 本文件 LangChain 实现           | 原生度 |
|------------------------------|-------------------------------|--------|
| POST /rag/documents          | POST /langchain-rag/documents | 🟡 80% |
| POST /rag/search             | POST /langchain-rag/search    | 🟢 95% |
| POST /rag/chat               | POST /langchain-rag/chat      | 🟡 70% |
| POST /rag/estimate-tokens    | POST /langchain-rag/estimate-tokens | 🔴 tiktoken |
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import AsyncIterator
import json
import os

from dotenv import load_dotenv

# ========== LangChain 核心组件 ==========
from langchain_community.embeddings import HuggingFaceBgeEmbeddings  # 本地 Embedding
from langchain_deepseek import ChatDeepSeek            # 替代 ChatOpenAI，原生支持 DeepSeek 推理链
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document as LCDocument

from langchain_core.messages import AIMessageChunk
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 复用 ChromaDB 客户端（与手搓版共享同一个数据库目录）
import chromadb

# ========== 保留组件（LangChain 无原生替代） ==========
import tiktoken                           # Token 估算

from database import get_db               # SQLite 依赖注入
from models import Document, DocumentChunk  # SQLAlchemy ORM

# ========== 初始化配置 ==========
load_dotenv()

MODELSCOPE_BASE_URL = os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1")
MODELSCOPE_API_KEY = os.getenv("MODELSCOPE_API_KEY")
LLM_MODEL = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL_NAME", "Qwen/Qwen3-Embedding-8B")

# 上下文窗口配置
MAX_CONTEXT_TOKENS = 2000
MAX_INPUT_TOKENS = 6000
MAX_OUTPUT_TOKENS = 2000

# ---------- 1. Embedding 模型（本地 HuggingFace BGE、MPS 加速） ----------

def _create_embedding_model():
    """
    创建并配置 Embedding 模型，自动选择最优设备。

    设备选择策略：
    1. 检测 MPS（Apple Silicon GPU）是否可用且兼容
    2. 如果可用 → 用 MPS 加速
    3. 如果不可用 / 加载失败 → 回退到 CPU
    """

    def _detect_mps() -> str:
        """检测 MPS 是否可用，返回 'mps' 或 'cpu'"""
        try:
            import torch
            if torch.backends.mps.is_available():
                # 冒烟测试：用极小张量确认 MPS 确实能跑
                try:
                    _ = torch.tensor([1.0], device="mps")
                    print("[Embedding] MPS 可用 ✅，使用 Metal GPU 加速")
                    return "mps"
                except Exception:
                    print("[Embedding] MPS 冒烟测试失败，回退 CPU ⚠️")
                    return "cpu"
            else:
                print("[Embedding] MPS 不可用，使用 CPU 🖥️")
                return "cpu"
        except ImportError:
            print("[Embedding] PyTorch 未安装，使用 CPU 🖥️")
            return "cpu"

    device = _detect_mps()

    try:
        model = HuggingFaceBgeEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True},
        )
        print(f"[Embedding] 模型加载完成，设备: {device}")
        return model
    except Exception as e:
        if device == "mps":
            print(f"[Embedding] MPS 初始化失败: {e}")
            print("[Embedding] 回退到 CPU")
            model = HuggingFaceBgeEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            print("[Embedding] 模型加载完成，设备: cpu")
            return model
        else:
            raise  # CPU 也失败了，直接抛异常


embedding_model = _create_embedding_model()

# ---------- 2. LLM（langchain-deepseek 原生支持推理链） ----------
llm = ChatDeepSeek(
    model=LLM_MODEL,
    api_base=MODELSCOPE_BASE_URL,
    api_key=MODELSCOPE_API_KEY,
    temperature=0.7,
    streaming=True,
    model_kwargs={"extra_body": {"thinking": {"type": "enabled"}}},
)

# ---------- 3. VectorStore（LangChain 原生封装） ----------
chroma_client = chromadb.PersistentClient(path="./chroma_db")

vectorstore = Chroma(
    client=chroma_client,
    collection_name="documents",
    embedding_function=embedding_model,
)

# ---------- 4. TextSplitter（LangChain 原生） ----------
# 替代手搓版的 split_text()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
)


# =====================================================================
# 第1层：工具函数（纯函数，不依赖数据库）
# =====================================================================

def estimate_tokens(text: str, model: str = "cl100k_base") -> int:
    """Token 估算（LangChain 无原生替代，保留 tiktoken）"""
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))


def format_docs(docs) -> str:
    """把检索结果格式化为 Prompt 上下文字符串"""
    formatted = []
    for i, doc in enumerate(docs, start=1):
        title = doc.metadata.get("title", "未命名")
        source = doc.metadata.get("source", "未知来源")
        formatted.append(f"[{i}] 来源：《{title}》（{source}）\n{doc.page_content}")
    return "\n\n".join(formatted)


def truncate_context(formatted_context: str, max_tokens: int = MAX_CONTEXT_TOKENS) -> str:
    """
    Token 感知的上下文截断。
    按块（每块是一个资料片段）累积，超过上限即停止。

    LangChain 说明：LCEL 没有内置的 "截断到 N token" 组件，
    且因 /chat 接口中 SQLite 回查阻断了管道，此函数以纯函数方式直接调用。
    """
    if not formatted_context:
        return "没有检索到相关文档。"

    blocks = formatted_context.split("\n\n")
    result_blocks = []
    current_tokens = 0

    for block in blocks:
        block_tokens = estimate_tokens(block)
        if current_tokens + block_tokens > max_tokens:
            break  # 超预算即停，results 已按相似度排序
        result_blocks.append(block)
        current_tokens += block_tokens

    return "\n\n".join(result_blocks) if result_blocks else "没有检索到相关文档。"


# =====================================================================
# 第2层：数据层函数（操作 SQLite + ChromaDB）
#         每个函数只做一件事，函数名以 _ 开头表示"内部使用"
# =====================================================================

# -------- SQLite 操作 --------

def _save_document_to_sqlite(doc, db: Session) -> Document:
    """
    把完整文档存入 SQLite。
    返回 ORM 对象（此时已获得 id）。
    """
    document = Document(title=doc.title, content=doc.content, source=doc.source)
    db.add(document)
    db.commit()
    db.refresh(document)  # 刷新后 document.id 才有值
    return document


def _save_chunks_to_sqlite(chunks_with_ids: list[dict], db: Session):
    """
    批量存入切片元数据到 SQLite。
    chunks_with_ids 的格式：[{document_id, chunk_index, content, embedding_id}, ...]
    """
    for c in chunks_with_ids:
        chunk = DocumentChunk(
            document_id=c["document_id"],
            chunk_index=c["chunk_index"],
            content=c["content"],
            embedding_id=c["embedding_id"],
        )
        db.add(chunk)
    db.commit()


def _find_document_or_404(doc_id: int, db: Session) -> Document:
    """按 ID 查找文档，找不到直接抛 404 异常"""
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail=f"文档 ID={doc_id} 不存在")
    return document


def _delete_document_from_sqlite(document: Document, db: Session):
    """从 SQLite 删除文档（cascade 会自动删除关联的 chunks）"""
    db.delete(document)
    db.commit()


def _enrich_metadata_from_sqlite(doc: LCDocument, db: Session):
    """
    用 SQLite 的准确数据覆盖 LangChain Document 的 metadata。
    因为 ChromaDB 存的 metadata 可能不是最新的。
    """
    doc_id = doc.metadata.get("document_id")
    if not doc_id:
        return

    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if db_doc:
        doc.metadata["title"] = db_doc.title
        doc.metadata["source"] = db_doc.source or "未知来源"


# -------- ChromaDB 操作 --------

def _build_chroma_data(
    chunk_texts: list[str],
    document_id: int,
    title: str,
    source: str,
) -> tuple[list[LCDocument], list[str]]:
    """
    为 ChromaDB 准备数据。
    返回 (lc_docs, chroma_ids) 两个列表，下标一一对应。

    参数：
    - chunk_texts: 文本切片结果
    - document_id: 文档在 SQLite 中的 ID
    - title: 文档标题
    - source: 文档来源
    
    返回：
    - lc_docs: LangChain Document 对象列表（给 ChromaDB 用）
    - chroma_ids: 向量 ID 列表（格式："doc{id}_chunk{idx}"）
    """
    lc_docs = []
    chroma_ids = []

    for i, chunk_text in enumerate(chunk_texts):
        lc_docs.append(LCDocument(
            page_content=chunk_text,
            metadata={
                "document_id": document_id,
                "chunk_index": i,
                "title": title,
                "source": source,
            }
        ))
        chroma_ids.append(f"doc{document_id}_chunk{i}")

    return lc_docs, chroma_ids


def _save_to_chromadb(lc_docs: list[LCDocument], chroma_ids: list[str]):
    """
    把切片存入 ChromaDB（自动完成 Embedding + 向量存储）。
    """
    try:
        vectorstore.add_documents(lc_docs, ids=chroma_ids)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ChromaDB 存储失败（ID 可能重复，请勿重复提交相同文档）: {str(e)}"
        )


def _search_vectorstore(query: str, k: int) -> list[tuple[LCDocument, float]]:
    """
    语义检索：从 ChromaDB 中找到与 query 最相似的 k 条切片。
    返回 [(Document, distance), ...]，distance 越小越相似（0=完全相同）。
    """
    return vectorstore.similarity_search_with_score(query, k=k)


def _delete_from_chromadb(document: Document):
    """
    从 ChromaDB 删除某个文档的所有切片向量。
    """
    embedding_ids = [chunk.embedding_id for chunk in document.chunks]
    if embedding_ids:
        try:
            vectorstore.delete(ids=embedding_ids)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"ChromaDB 删除失败: {str(e)}"
            )
    return embedding_ids  # 返回删了多少条


# =====================================================================
# 第3层：业务层函数（组合多个数据层函数）
# =====================================================================

def _prepare_chunks_for_storage(
    chunk_texts: list[str],
    document: Document,
    doc_in,
    db: Session,
):
    """
    切片数据的完整处理流程：
    1. 构建 ChromaDB 数据
    2. 存切片元数据到 SQLite
    3. 存向量到 ChromaDB

    参数 doc_in 是用户请求传入的 DocumentIn 对象。
    """
    # 1. 构建 ChromaDB 需要的数据
    lc_docs, chroma_ids = _build_chroma_data(
        chunk_texts=chunk_texts,
        document_id=document.id,
        title=doc_in.title,
        source=doc_in.source,
    )

    # 2. 构建 SQLite 数据
    sqlite_chunks = []
    for i, chunk_text in enumerate(chunk_texts):
        sqlite_chunks.append({
            "document_id": document.id,
            "chunk_index": i,
            "content": chunk_text,
            "embedding_id": chroma_ids[i],  # 复用同一个 ID，保持关联
        })

    # 3. 存 SQLite
    _save_chunks_to_sqlite(sqlite_chunks, db)

    # 4. 存 ChromaDB
    _save_to_chromadb(lc_docs, chroma_ids)


def _parse_search_results(
    results_with_scores: list[tuple[LCDocument, float]],
    db: Session,
) -> list[dict]:
    """
    把 ChromaDB 的检索结果解析为前端需要的格式。
    同时用 SQLite 数据增强（确保 title 等字段准确）。

    返回格式：[{title, chunk_content, similarity, document_id, chunk_index}, ...]
    """
    output = []
    for doc, distance in results_with_scores:
        metadata = doc.metadata
        doc_id = metadata.get("document_id")
        chunk_idx = metadata.get("chunk_index")
        similarity = round(1 - distance, 4)  # cosine distance → similarity

        # SQLite 回查：获取最新的 title、content
        if doc_id is not None and chunk_idx is not None:
            db_doc = db.query(Document).filter(Document.id == doc_id).first()
            db_chunk = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == doc_id,
                DocumentChunk.chunk_index == chunk_idx,
            ).first()

            title = db_doc.title if db_doc else metadata.get("title", "未知")
            chunk_content = db_chunk.content if db_chunk else doc.page_content
        else:
            title = metadata.get("title", "未知")
            chunk_content = doc.page_content

        output.append({
            "title": title,
            "chunk_content": chunk_content,
            "similarity": similarity,
            "document_id": doc_id or 0,
            "chunk_index": chunk_idx or 0,
        })

    return output


def _retrieve_context(
    query: str,
    k: int,
    db: Session,
) -> tuple[list[LCDocument], str]:
    """
    完整的检索 → 增强 → 格式化 → 截断流程。
    返回 (原始文档列表, 格式化后的上下文字符串)。
    """
    # 1. 语义检索
    docs = vectorstore.similarity_search(query, k=k)

    # 2. SQLite 增强 metadata
    for doc in docs:
        _enrich_metadata_from_sqlite(doc, db)

    # 3. 格式化 + Token 截断
    context = format_docs(docs)
    context = truncate_context(context)

    return docs, context


def _build_sources_text(docs: list) -> str:
    """
    从检索结果中提取来源信息，构建参考来源文本。
    """
    sources = []
    for i, doc in enumerate(docs, start=1):
        title = doc.metadata.get("title", "未命名")
        source = doc.metadata.get("source", "未知来源")
        sources.append(f"[{i}] 《{title}》（{source}）")

    if sources:
        return "\n\n【参考来源】\n" + "\n".join(sources)
    return ""


# =====================================================================
# 第4层：表现层函数（SSE 流式输出相关）
# =====================================================================

def _build_rag_chain():
    """
    构建 LCEL 链：RAG_PROMPT | llm
    注意：不挂 StrOutputParser，保留 AIMessageChunk，
    这样才能拿到推理链（reasoning_content）。
    """
    return RAG_PROMPT | llm


def _yield_sse(event_type: str, content: str):
    """
    SSE 格式化工具。
    生成器用 yield，普通函数用 return，所以这里返回字符串。
    用法：yield _yield_sse("thinking", "思考内容")
    """
    data = {"type": event_type, "content": content}
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def _check_token_budget(context: str, question: str) -> str | None:
    """
    检查 Token 是否超限。
    返回 None 表示正常，返回字符串表示错误信息。
    """
    total_input = estimate_tokens(context) + estimate_tokens(question)
    if total_input > MAX_INPUT_TOKENS:
        return "输入总 Token 数量超过最大限制，请减少检索结果数量或精简问题。"
    return None


async def _generate_stream(
    context: str,
    question: str,
    docs: list[LCDocument],
) -> AsyncIterator[str]:
    """
    RAG 流式响应的核心生成器。
    负责：LCEL 链执行 → 解析推理链 + 回答 → SSE 包装 → 追加来源。

    数据流向：
    chain.astream({context, question})
      → AIMessageChunk（含 reasoning_content + content）
        → yield thinking + answer 事件
    → 最后 yield sources + done 事件
    """
    chain = _build_rag_chain()
    done_thinking = False

    try:
        async for chunk in chain.astream(
            {"context": context, "question": question},
            config={"max_tokens": MAX_OUTPUT_TOKENS}
        ):
            if isinstance(chunk, AIMessageChunk):
                reasoning = chunk.additional_kwargs.get("reasoning_content", "")
                answer = chunk.content

                # 推理链先出
                if reasoning:
                    yield _yield_sse("thinking", reasoning)

                # 回答后出，第一次出回答时先插一个分隔线
                if answer:
                    if not done_thinking:
                        yield _yield_sse("divider", "\n\n === Final Answer ===\n")
                        done_thinking = True
                    yield _yield_sse("answer", answer)

        # 来源信息
        sources_text = _build_sources_text(docs)
        if sources_text:
            yield _yield_sse("sources", sources_text)

        yield _yield_sse("done", "")

    except Exception as e:
        yield _yield_sse("error", f"链执行出错: {str(e)}")


# ========== Prompt 模板（LangChain 原生） ==========
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个基于知识库的问答助手。下面是从知识库中检索到的与用户问题相关的资料片段。

【资料片段】
{context}

【回答要求】
1. 请提取以上资料中与用户问题相关的信息，整理归纳后回答用户。
2. 不要编造资料中没有的信息，不要用你自己的知识补充。
3. 只有当资料片段为空（显示为"没有检索到相关文档"）时，才回答"根据现有资料无法回答该问题。"。否则，资料中无论信息多少，都应基于它们给出回答。"""),
    ("human", "{question}"),
])


# ========== FastAPI 路由 ==========
router = APIRouter(prefix="/langchain-rag", tags=["LangChain RAG"])


# ========== Pydantic 模型（与手搓版一致） ==========

class DocumentIn(BaseModel):
    title: str
    content: str
    source: str = ""


class SearchIn(BaseModel):
    query: str
    n_results: int = 3


class SearchResult(BaseModel):
    title: str
    chunk_content: str
    similarity: float
    document_id: int
    chunk_index: int


class ApiResponse(BaseModel):
    """通用响应包装"""
    code: int = 200
    status: str = "success"
    content: dict | list | str | bool | int | float | None = None


class ChatRequest(BaseModel):
    query: str
    n_results: int = 3


class EstimateTokensRequest(BaseModel):
    text: str


# =====================================================================
# 第5层：路由接口（最薄的一层，只做编排）
# =====================================================================

# ==================== 接口 1：存入文档 ====================

@router.post("/documents", summary="存入文档（LangChain 切片 + 双存储）")
def add_document(doc: DocumentIn, db: Session = Depends(get_db)):
    """
    存入文档的完整流程：
    1. SQLite：存完整文档
    2. LangChain：切分文本
    3. SQLite：存切片元数据
    4. ChromaDB：存向量
    """
    # 1. 完整文档 → SQLite
    document = _save_document_to_sqlite(doc, db)

    # 2. 文本切片（LangChain 原生）
    chunk_texts = text_splitter.split_text(doc.content)

    # 3. 切片 → SQLite + ChromaDB
    _prepare_chunks_for_storage(chunk_texts, document, doc, db)

    return ApiResponse(
        code=200,
        status="success",
        content={
            "message": "文档存入成功",
            "document_id": document.id,
            "title": doc.title,
            "chunks_count": len(chunk_texts),
        }
    )


# ==================== 接口 2：语义检索 ====================

@router.post("/search", summary="语义检索（LangChain 原生）")
def search(query: SearchIn, db: Session = Depends(get_db)):
    """
    语义检索流程：
    1. ChromaDB 语义检索（拿到相似切片）
    2. SQLite 回查（获取最新 title、content）
    3. 包装为统一格式返回
    """
    # 1. ChromaDB 检索
    results = _search_vectorstore(query.query, k=query.n_results)

    if not results:
        return []  # 空结果返回空列表

    # 2. 解析 + SQLite 增强
    parsed = _parse_search_results(results, db)

    # 3. 包装为 SearchResult 对象
    output = [SearchResult(**r) for r in parsed]

    return ApiResponse(code=200, status="success", content=output)


# ==================== 接口 3：RAG 流式问答 ====================

@router.post("/chat", summary="RAG 流式问答（LangChain 检索 + 推理链保留）")
async def langchain_chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    RAG 流式问答流程：
    1. 检索 → 增强 → 截断（_retrieve_context）
    2. 检查 Token 预算
    3. 流式生成（_generate_stream）
    """
    # 1. 检索上下文
    docs, context = _retrieve_context(req.query, k=req.n_results, db=db)

    # 2. 检查 Token 预算
    error_msg = _check_token_budget(context, req.query)
    if error_msg:
        async def error_stream():
            yield _yield_sse("error", error_msg)
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    # 3. 流式生成
    return StreamingResponse(
        _generate_stream(context, req.query, docs),
        media_type="text/event-stream",
    )


# ==================== 接口 4：Token 估算 ====================

@router.post("/estimate-tokens", summary="估算 Token 数量（tiktoken，LangChain 无原生替代）")
def estimate_tokens_endpoint(req: EstimateTokensRequest):
    """
    LangChain 没有独立的 Token 估算组件，保留 tiktoken。
    """
    return ApiResponse(
        code=200,
        status="success",
        content={"token_count": estimate_tokens(req.text)}
    )


# ==================== 接口 5：删除文档 ====================

@router.delete("/documents/{doc_id}", summary="删除文档（ChromaDB + SQLite 双删除）")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """
    双删除流程：
    1. 查找文档（不存在则 404）
    2. 从 ChromaDB 删除向量
    3. 从 SQLite 删除记录
    """
    # 1. 查找
    document = _find_document_or_404(doc_id, db)
    title = document.title

    # 2. ChromaDB 删除
    deleted_ids = _delete_from_chromadb(document)

    # 3. SQLite 删除
    _delete_document_from_sqlite(document, db)

    return ApiResponse(
        code=200,
        status="success",
        content={
            "message": "文档删除成功",
            "document_id": doc_id,
            "title": title,
            "deleted_chunks": len(deleted_ids),
        }
    )


# ==================== 接口 6：健康检查 ====================

@router.get("/health", summary="LangChain RAG 健康检查")
def health_check():
    """检查 LangChain 各组件是否正常加载"""
    try:
        count = vectorstore._collection.count()
        return ApiResponse(
            code=200,
            status="ok",
            content={
                "vectorstore_docs": count,
                "llm_model": LLM_MODEL,
                "embedding_model": EMBEDDING_MODEL,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
