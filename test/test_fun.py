def normalize_title(title: str) -> str:
    return title.strip()

def test_normalize_title():
    assert normalize_title("  这是一个标题  ") == "这是一个标题"