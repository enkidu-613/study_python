"""增量同步学习笔记到 ChromaDB。

基于文件 mtime + chunk_ids 索引,只重灌变更文件,删除其旧版本 chunks。
索引文件: chroma_db/file_index.json

用法:
    poetry run python -m app.tools.sync_notes          # 增量同步默认三目录
    poetry run python -m app.tools.sync_notes --full    # 强制全量重建
    poetry run python -m app.tools.sync_notes --path /xxx --tag foo
    poetry run python -m app.tools.sync_notes --prune   # 清理已删除文件的残留 chunks

同步规则:
    - 新文件:       灌入,记录 mtime + chunk_ids
    - mtime 变了:   删除该文件旧 chunks → 灌入新的 → 更新索引
    - mtime 没变:   跳过
    - 文件被删除:   默认不处理(--prune 才清理,见下)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import chromadb
from langchain_chroma import Chroma

from app.embedding import get_langchain_embeddings
from app.tools.ingest_notes import (
    CHROMA_PATH,
    COLLECTION_NAME,
    NOTE_DIRS,
    _collect_files,
    _is_sensitive,
    _load_and_split,
    _make_id,
)

INDEX_FILE = Path(CHROMA_PATH) / "file_index.json"


def _load_index() -> dict:
    """读取文件索引;不存在则返回空 dict。"""
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return {}


def _save_index(index: dict) -> None:
    """保存文件索引到 chroma_db/file_index.json。"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _get_vector_store() -> Chroma:
    """获取 ChromaDB 向量存储实例。"""
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    return Chroma(
        client=chroma_client,
        collection_name=COLLECTION_NAME,
        embedding_function=get_langchain_embeddings(),
    )


def sync(dirs: list[dict[str, str]] | None = None) -> None:
    """增量同步:对比 mtime,只重灌变更文件,删除其旧 chunks。

    - dirs=None 时用默认 NOTE_DIRS;传入则覆盖默认。
    - 新文件:        灌入 + 记录索引
    - mtime 变了:    删旧 chunks → 灌新 → 更新索引
    - mtime 没变:    跳过
    - 文件被删除:    默认不处理(用 --prune 或 sync(prune=True) 清理)
    """
    target_dirs = dirs if dirs is not None else NOTE_DIRS

    # 安全检查
    safe_dirs: list[dict[str, str]] = []
    for d in target_dirs:
        if _is_sensitive(d["path"]):
            print(f"[reject] 跳过敏感目录: {d['path']}")
            continue
        safe_dirs.append(d)

    if not safe_dirs:
        print("[abort] 没有可同步的安全目录")
        return

    index = _load_index()
    vector_store = _get_vector_store()

    added = 0
    updated = 0
    skipped = 0
    added_chunks = 0
    deleted_chunks = 0

    for note_dir in safe_dirs:
        dir_path = note_dir["path"]
        tag = note_dir["tag"]
        label = note_dir.get("label", tag)

        files = _collect_files(dir_path)
        print(f"[scan] {label}: 找到 {len(files)} 个文件")

        for file_path in files:
            key = str(file_path)
            mtime = file_path.stat().st_mtime

            docs = _load_and_split(file_path, tag)
            if not docs:
                continue

            new_chunk_ids = [_make_id(key, i) for i in range(len(docs))]
            old_record = index.get(key)

            if old_record is None:
                # 新文件
                vector_store.add_documents(docs, ids=new_chunk_ids)
                index[key] = {"mtime": mtime, "chunk_ids": new_chunk_ids, "tag": tag}
                added += 1
                added_chunks += len(docs)
            elif old_record["mtime"] == mtime:
                # 未变化
                skipped += 1
            else:
                # 修改:先删旧 chunks,再灌入新的
                try:
                    vector_store.delete(ids=old_record["chunk_ids"])
                    deleted_chunks += len(old_record["chunk_ids"])
                except Exception as exc:
                    print(f"[warn] 删除旧 chunks 失败 {key}: {exc}")
                vector_store.add_documents(docs, ids=new_chunk_ids)
                index[key] = {"mtime": mtime, "chunk_ids": new_chunk_ids, "tag": tag}
                updated += 1
                added_chunks += len(docs)

    _save_index(index)

    print(f"\n[summary] 新增 {added} / 更新 {updated} / 跳过 {skipped} 文件")
    print(f"[summary] 灌入 {added_chunks} 切片 / 删除 {deleted_chunks} 旧切片")
    print(f"[summary] 索引: {INDEX_FILE}")


def prune(dirs: list[dict[str, str]] | None = None) -> None:
    """清理已删除文件的残留 chunks 和索引项。

    扫描索引里记录的所有文件,如果文件已不存在于文件系统,
    则删除其在 ChromaDB 里的 chunks,并从索引中移除。
    """
    target_dirs = dirs if dirs is not None else NOTE_DIRS
    index = _load_index()

    if not index:
        print("[prune] 索引为空,无需清理")
        return

    # 收集所有目标目录下实际存在的文件
    existing_files: set[str] = set()
    for note_dir in target_dirs:
        if _is_sensitive(note_dir["path"]):
            continue
        for f in _collect_files(note_dir["path"]):
            existing_files.add(str(f))

    vector_store = _get_vector_store()
    removed_files = 0
    removed_chunks = 0

    for key, record in list(index.items()):
        if key not in existing_files:
            # 文件已被删除,清理 chunks + 索引
            try:
                vector_store.delete(ids=record["chunk_ids"])
                removed_chunks += len(record["chunk_ids"])
            except Exception as exc:
                print(f"[warn] 删除 chunks 失败 {key}: {exc}")
            del index[key]
            removed_files += 1

    _save_index(index)
    print(f"[prune] 清理 {removed_files} 个已删除文件 / {removed_chunks} 个 chunks")


def full_resync(dirs: list[dict[str, str]] | None = None) -> None:
    """全量重建:清空 collection + 清空索引 + 重新灌入所有文件 + 重建索引。

    等同于 ingest_notes --reset,但额外重建 file_index.json。
    """
    # 1. 清空索引文件
    if INDEX_FILE.exists():
        INDEX_FILE.unlink()
        print(f"[reset] 已删除索引: {INDEX_FILE}")

    # 2. 调用 ingest 的 reset 逻辑(清 collection + 重新灌入)
    from app.tools.ingest_notes import ingest
    ingest(reset=True, dirs=dirs)

    # 3. 重建索引(只算 mtime + chunk_ids,不写入 ChromaDB)
    target_dirs = dirs if dirs is not None else NOTE_DIRS
    index: dict = {}
    for note_dir in target_dirs:
        if _is_sensitive(note_dir["path"]):
            continue
        files = _collect_files(note_dir["path"])
        tag = note_dir["tag"]
        for file_path in files:
            key = str(file_path)
            docs = _load_and_split(file_path, tag)
            if not docs:
                continue
            chunk_ids = [_make_id(key, i) for i in range(len(docs))]
            index[key] = {
                "mtime": file_path.stat().st_mtime,
                "chunk_ids": chunk_ids,
                "tag": tag,
            }
    _save_index(index)
    print(f"[index] 重建完成,共 {len(index)} 个文件")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="增量同步学习笔记到 ChromaDB",
        epilog="默认只同步变更的文件;--full 全量重建;--prune 清理已删除文件残留。",
    )
    parser.add_argument("--full", action="store_true", help="强制全量重建(清空 + 重灌 + 重建索引)")
    parser.add_argument("--prune", action="store_true", help="清理已删除文件的残留 chunks")
    parser.add_argument("--path", action="append", default=None, help="指定目录(可多次),覆盖默认")
    parser.add_argument("--tag", action="append", default=None, help="与 --path 配对的标签(可多次)")
    args = parser.parse_args()

    # 组装 dirs
    cli_dirs: list[dict[str, str]] | None = None
    if args.path:
        cli_dirs = []
        tags = args.tag or []
        for i, p in enumerate(args.path):
            tag = tags[i] if i < len(tags) else "custom"
            cli_dirs.append({"path": p, "tag": tag, "label": f"{tag}@{p}"})

    if args.full:
        full_resync(dirs=cli_dirs)
    elif args.prune:
        prune(dirs=cli_dirs)
    else:
        sync(dirs=cli_dirs)
