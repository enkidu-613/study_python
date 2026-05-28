from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database import engine
from datetime import datetime

Base = declarative_base()

class DBTodo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_done = Column(Boolean, default=False)


class Document(Base):
    """📚 完整文档（藏书仓库里的整本书）"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    source = Column(String(500))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    """✂️ 文档切片（索引卡片）"""
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding_id = Column(String(100), unique=True)

    document = relationship("Document", back_populates="chunks")


Base.metadata.create_all(bind=engine)
