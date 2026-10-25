"""第 40 章：本地、无敏感内容的 AI 调用观测辅助函数。"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter


logger = logging.getLogger(__name__)


@contextmanager
def observe_operation(
    operation: str,
    *,
    model: str | None = None,
    input_chars: int | None = None,
) -> Iterator[None]:
    """记录一次操作的开始、结束、失败和耗时，不记录完整用户内容。"""
    started_at = perf_counter()
    logger.info(
        "ai_event=started operation=%s model=%s input_chars=%s",
        operation,
        model or "unknown",
        input_chars if input_chars is not None else "unknown",
    )
    try:
        yield
    except Exception:
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        logger.exception(
            "ai_event=failed operation=%s elapsed_ms=%s",
            operation,
            elapsed_ms,
        )
        raise
    else:
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        logger.info(
            "ai_event=completed operation=%s elapsed_ms=%s",
            operation,
            elapsed_ms,
        )
