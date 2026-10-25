from app.main import should_preload_embedding


def test_embedding_preload_is_enabled_by_default(monkeypatch):
    monkeypatch.delenv("SKIP_EMBEDDING_PRELOAD", raising=False)

    assert should_preload_embedding() is True


def test_embedding_preload_can_be_skipped_for_ci(monkeypatch):
    monkeypatch.setenv("SKIP_EMBEDDING_PRELOAD", "1")

    assert should_preload_embedding() is False
