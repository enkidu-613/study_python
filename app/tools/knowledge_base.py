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


def search_knowledge_base(query: str, limit: int = 3) -> list[LCDocument]:
    """
    在知识库中搜索相关文档切片，并返回结果列表。
    """
    return get_vector_store().similarity_search(query, k=limit)