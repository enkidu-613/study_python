from langchain_core.tools import tool

from app.embedding import get_langchain_embeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document as LCDocument
from dotenv import load_dotenv
import chromadb

load_dotenv()

chroma_client = chromadb.PersistentClient(path="./chroma_db")


_vector_store = None

def get_vector_store():
    """
    获取知识库向量存储实例。
    """
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
            client=chroma_client,
            collection_name="documents",
            embedding_function=get_langchain_embeddings()  # 使用默认的嵌入函数
        )
    return _vector_store

@tool
def search_knowledge_base(query: str, limit: int = 3) -> str:
    """
    在知识库中搜索相关文档切片，并返回结果列表。
    """
    safe_limit = max(1, min(limit, 5))  # 限制返回的文档数量在1到5之间
    docs = get_vector_store().similarity_search(query, k=safe_limit)

    if not docs:
        return "没有找到相关的文档。"
    
    formatted_docs = []
    
    for index,doc in enumerate(docs, start=1):
        metadata = doc.metadata
        title = metadata.get("title", "未知标题")
        source = metadata.get("source", "未知来源")
        chunk_index = metadata.get("chunk_index", "未知索引")
        content = doc.page_content[:800]  # 截取前800个字符
        text = f"[{index}] 来源：《{title}》({source},chunk={chunk_index})\n{content}"
        formatted_docs.append(text)
    
    return "\n\n".join(formatted_docs)