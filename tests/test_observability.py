import logging

import pytest

from app.observability import observe_operation


def test_observe_operation_logs_only_metadata(caplog):
    with caplog.at_level(logging.INFO):
        with observe_operation("rag.retrieve", model="demo-model", input_chars=12):
            pass

    assert "ai_event=started operation=rag.retrieve" in caplog.text
    assert "ai_event=completed operation=rag.retrieve" in caplog.text


def test_observe_operation_reraises_failure(caplog):
    with caplog.at_level(logging.ERROR), pytest.raises(ValueError, match="boom"):
        with observe_operation("agent.answer"):
            raise ValueError("boom")

    assert "ai_event=failed operation=agent.answer" in caplog.text
