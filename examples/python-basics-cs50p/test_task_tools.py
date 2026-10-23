# Teaching material: enkidu-613; CS50P topic reference: David J. Malan and
# the CS50 team, Harvard University. CC BY-NC-SA 4.0.
# https://cs50.harvard.edu/python/ | https://creativecommons.org/licenses/by-nc-sa/4.0/
import pytest

from task_tools import is_task_code, normalize_title, parse_minutes


def test_normalize_title_removes_outer_spaces():
    assert normalize_title("  学习 Python  ") == "学习 Python"


def test_normalize_title_rejects_blank():
    with pytest.raises(ValueError):
        normalize_title("   ")


def test_parse_minutes_accepts_positive_integer():
    assert parse_minutes("20") == 20


def test_parse_minutes_rejects_invalid_text():
    with pytest.raises(ValueError):
        parse_minutes("abc")


def test_parse_minutes_rejects_zero():
    with pytest.raises(ValueError):
        parse_minutes("0")


def test_parse_minutes_rejects_negative_integer():
    with pytest.raises(ValueError):
        parse_minutes("-1")


def test_task_code_accepts_expected_format():
    assert is_task_code("TASK-001")


def test_task_code_rejects_short_number():
    assert not is_task_code("TASK-01")


def test_task_code_rejects_extra_characters():
    assert not is_task_code("TASK-001-extra")


def test_task_code_rejects_trailing_newline():
    assert not is_task_code("TASK-001\n")
