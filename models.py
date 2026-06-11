from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database import engine
from datetime import datetime
from sqlalchemy.sql import func

Base = declarative_base()


class DBTodo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_done = Column(Boolean, default=False)


class User(Base):
    """👤 用户（认证系统）"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)  # bcrypt 哈希值
    role = Column(String(20), default="USER")
    created_at = Column(DateTime, default=datetime.now)


class RevokedToken(Base):
    """🚫 Token 黑名单（挂失的 Token）"""
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True)
    token_hash = Column(String(64), unique=True, index=True)  # SHA256 哈希值，不存完整 Token
    revoked_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)  # Token 自然过期时间，方便定时清理


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
