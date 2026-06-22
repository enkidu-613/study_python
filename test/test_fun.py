def normalize_title(title: str) -> str:
    return title.strip()

def test_normalize_title_strips_spaces():
    # 三段式测试
    # 1.准备输入
    # 2.执行函数
    # 3.检查结果
    """
    对应代码 
    title = "  这是一个标题  "
    result = normalize_title(title)
    assert result == "这是一个标题"
    """
    assert normalize_title("  这是一个标题  ") == "这是一个标题"


