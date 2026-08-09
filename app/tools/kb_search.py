"""个人知识库检索 CLI 工具。

用法:
    poetry run python -m app.tools.kb_search "FastAPI 路由怎么写"
    poetry run python -m app.tools.kb_search "NestJS 控制器" --limit 5
    poetry run python -m app.tools.kb_search "NestJS 守卫" --tag nestjs
    poetry run python -m app.tools.kb_search "React Hook" --tag react
    poetry run python -m app.tools.kb_search "RAG 检索" --tag python_ai
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma

from app.embedding import get_langchain_embeddings

load_dotenv()

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "personal_notes"


def get_vector_store() -> Chroma:
    """获取个人知识库的向量存储实例。"""
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    return Chroma(
        client=chroma_client,
        collection_name=COLLECTION_NAME,
        embedding_function=get_langchain_embeddings(),
    )


def search(query: str, limit: int = 3, tag: str | None = None) -> list[dict]:
    """检索知识库，返回结果列表。

    Args:
        query: 搜索关键词
        limit: 返回结果数量（1-10）
        tag: 可选，按标签过滤。默认 tag: python_ai / nestjs / react;
            也支持 ingest_notes --tag 自定义的任意标签。
    """
    safe_limit = max(1, min(limit, 10))

    store = get_vector_store()

    # 构建 filter
    where_filter = None
    if tag:
        where_filter = {"tag": tag}

    docs = store.similarity_search(
        query,
        k=safe_limit,
        filter=where_filter,
    )

    results = []
    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata
        results.append({
            "index": i,
            "title": metadata.get("title", "未知"),
            "source": metadata.get("source", "未知"),
            "tag": metadata.get("tag", "未知"),
            "chunk_index": metadata.get("chunk_index", 0),
            "content": doc.page_content,
        })
    return results


def format_text(results: list[dict]) -> str:
    """格式化为纯文本输出。"""
    if not results:
        return "没有找到相关内容。"

    lines = []
    for r in results:
        lines.append(f"--- [{r['index']}] {r['title']} (tag={r['tag']}) ---")
        lines.append(f"来源: {r['source']}")
        lines.append(f"内容:\n{r['content']}")
        lines.append("")
    return "\n".join(lines)


def format_json(results: list[dict]) -> str:
    """格式化为 JSON 输出。"""
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="个人知识库检索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=3, help="返回结果数量 (默认 3)")
    parser.add_argument("--tag", default=None, help="按标签过滤(如 python_ai / nestjs / react 或自定义 tag)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    results = search(args.query, limit=args.limit, tag=args.tag)

    if args.json:
        print(format_json(results))
    else:
        print(format_text(results))
