"""把学习笔记灌入 ChromaDB 的 personal_notes collection。

用法:
    poetry run python -m app.tools.ingest_notes          # 灌入默认目录
    poetry run python -m app.tools.ingest_notes --reset   # 清空后重新灌入
    poetry run python -m app.tools.ingest_notes --path /xxx --tag foo   # 灌入指定目录
    poetry run python -m app.tools.ingest_notes --path /a --tag t1 --path /b --tag t2
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.embedding import get_langchain_embeddings

load_dotenv()

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "personal_notes"

# 灌入目录配置
NOTE_DIRS: list[dict[str, str]] = [
    {
        "path": "/Users/enkidu/PyCharmMiscProject/md",
        "tag": "python_ai",
        "label": "Python/FastAPI/AI",
    },
    {
        "path": "/Users/enkidu/project/study/01-语言/JavaScript/NestJS/后端课程",
        "tag": "nestjs",
        "label": "NestJS 课程笔记",
    },
    {
        "path": "/Users/enkidu/project/study/01-语言/JavaScript/React/课程",
        "tag": "react",
        "label": "React 课程笔记",
    },
]

# 只收录这些扩展名
VALID_EXTENSIONS = {".md", ".markdown"}

# 排除的目录名(精确匹配):demo 项目代码、构建产物、依赖目录
# 这些目录里的 .md 多为 README/配置说明,不是课程讲义笔记
EXCLUDE_DIR_NAMES: set[str] = {
    "node_modules", ".git", "dist", "build",
    # NestJS demo 项目
    "blog-demo", "prisma-demo", "prisma-my",
    "my-project", "my-project_new", "test_class",
    "frontend", "backend_notes", "start-point",
    # React demo 项目
    # 注意:不能用 "enkidu",它也是用户名,会误伤所有 /Users/enkidu/ 路径
    "标准答案",
    # demo 项目内子目录
    "qa-backend", "qa-frontend-react", "qa-frontend-vue", "qa-fontend-vue",
    "generated",
}

# 排除的目录名前缀:backend-intro-notes-lesson4-*-demo 这类
EXCLUDE_DIR_PREFIXES: tuple[str, ...] = ("backend-intro-notes-lesson4-",)

# 系统敏感目录前缀黑名单:AI/用户传任意路径时,命中这些就拒绝灌入
# 防止误操作系统目录、系统配置、应用数据
SENSITIVE_PATH_PREFIXES: tuple[str, ...] = (
    "/System", "/usr", "/bin", "/sbin", "/etc", "/var", "/private/etc", "/private/var",
    "/dev", "/proc", "/sys",
    "/Library",  # macOS 系统库
    "/Users/enkidu/Library",  # 用户应用数据(含 Keychain、Preferences 等)
    "/Users/enkidu/.Trash",   # 废纸篓
)

# 切片参数
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80


def _is_sensitive(path: str) -> bool:
    """路径是否落在系统敏感目录内。用 resolve() 解析软链和 .. 后再判断前缀。"""
    resolved = str(Path(path).expanduser().resolve())
    return any(resolved == p or resolved.startswith(p + "/") for p in SENSITIVE_PATH_PREFIXES)


def _is_excluded(path: Path) -> bool:
    """路径中任意一段命中排除名或前缀,就跳过整个文件。"""
    for part in path.parts:
        if part in EXCLUDE_DIR_NAMES:
            return True
        if any(part.startswith(prefix) for prefix in EXCLUDE_DIR_PREFIXES):
            return True
    return False


def _collect_files(root: str) -> list[Path]:
    """递归收集目录下所有 .md 文件,跳过 demo 项目目录。"""
    root_path = Path(root)
    if not root_path.exists():
        return []
    return sorted(
        p for p in root_path.rglob("*")
        if p.is_file()
        and p.suffix.lower() in VALID_EXTENSIONS
        and not _is_excluded(p)
    )


def _make_id(file_path: str, chunk_index: int) -> str:
    """用文件路径 + chunk 索引生成稳定 ID，重复灌入时覆盖而不是追加。"""
    h = hashlib.md5(file_path.encode()).hexdigest()[:10]
    return f"note_{h}_{chunk_index}"


def _load_and_split(file_path: Path, source_tag: str) -> list[LCDocument]:
    """读取单个文件，切片后返回 LCDocument 列表。"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = file_path.read_text(encoding="gbk")

    if not content.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", "。", "！", "？", "；", " "],
    )
    chunks = splitter.split_text(content)

    docs = []
    for i, chunk_text in enumerate(chunks):
        docs.append(LCDocument(
            page_content=chunk_text,
            metadata={
                "source": str(file_path),
                "tag": source_tag,
                "chunk_index": i,
                "title": file_path.stem,
            },
        ))
    return docs


def ingest(
    reset: bool = False,
    dry_run: bool = False,
    dirs: list[dict[str, str]] | None = None,
) -> None:
    """扫描所有目录，切片后灌入 ChromaDB。

    - dirs=None 时用默认 NOTE_DIRS;传入则覆盖默认,只灌用户指定的目录。
      每项形如 {"path": "...", "tag": "...", "label": "..."}(label 可缺省)。
    - dry_run=True 时只扫描和切片统计,不写入 ChromaDB,用来预览将要灌入的文件。
    - 任何 path 落在系统敏感目录内都会被拒绝并跳过。
    """
    target_dirs = dirs if dirs is not None else NOTE_DIRS

    # 安全检查:逐个路径审核,敏感目录直接拒绝
    safe_dirs: list[dict[str, str]] = []
    for d in target_dirs:
        p = d["path"]
        if _is_sensitive(p):
            print(f"[reject] 跳过敏感目录: {p}")
            continue
        safe_dirs.append(d)

    if not safe_dirs:
        print("[abort] 没有可灌入的安全目录")
        return

    vector_store = None
    if not dry_run:
        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

        if reset:
            try:
                chroma_client.delete_collection(COLLECTION_NAME)
                print(f"[reset] 已删除 collection: {COLLECTION_NAME}")
            except Exception:
                pass

        vector_store = Chroma(
            client=chroma_client,
            collection_name=COLLECTION_NAME,
            embedding_function=get_langchain_embeddings(),
        )

    total_files = 0
    total_chunks = 0

    for note_dir in safe_dirs:
        dir_path = note_dir["path"]
        tag = note_dir["tag"]
        label = note_dir.get("label", f"{tag}@{dir_path}")

        files = _collect_files(dir_path)
        if not files:
            print(f"[skip] {label}: 目录不存在或没有 .md 文件 ({dir_path})")
            continue

        print(f"[scan] {label}: 找到 {len(files)} 个文件")

        for file_path in files:
            docs = _load_and_split(file_path, tag)
            if not docs:
                continue

            if not dry_run:
                ids = [_make_id(str(file_path), i) for i in range(len(docs))]
                vector_store.add_documents(docs, ids=ids)
            total_files += 1
            total_chunks += len(docs)

        print(f"[done] {label}: {'预览完成(未写入)' if dry_run else '灌入完成'}")

    mode = "[dry-run] " if dry_run else ""
    print(f"\n{mode}[summary] 共 {total_files} 个文件, {total_chunks} 个切片")
    if not dry_run:
        print(f"[summary] collection: {COLLECTION_NAME}")
        print(f"[summary] 路径: {CHROMA_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="灌入学习笔记到 ChromaDB",
        epilog="不传 --path 时灌入默认 NOTE_DIRS;传 --path 则只灌指定目录(可多次配对 --tag)。",
    )
    parser.add_argument("--reset", action="store_true", help="清空 collection 后重新灌入")
    parser.add_argument("--dry-run", action="store_true", help="只扫描和统计,不写入 ChromaDB")
    parser.add_argument(
        "--path", action="append", default=None,
        help="指定要灌入的目录(可多次)。传了就覆盖默认目录。",
    )
    parser.add_argument(
        "--tag", action="append", default=None,
        help="与 --path 配对的标签(可多次)。缺省按 'custom' 处理。",
    )
    args = parser.parse_args()

    # 组装 dirs:仅当用户传了 --path 才覆盖默认
    cli_dirs: list[dict[str, str]] | None = None
    if args.path:
        cli_dirs = []
        tags = args.tag or []
        for i, p in enumerate(args.path):
            tag = tags[i] if i < len(tags) else "custom"
            cli_dirs.append({"path": p, "tag": tag, "label": f"{tag}@{p}"})

    ingest(reset=args.reset, dry_run=args.dry_run, dirs=cli_dirs)
