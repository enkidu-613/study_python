# Teaching material: enkidu-613; CS50P topic reference: David J. Malan and
# the CS50 team, Harvard University. CC BY-NC-SA 4.0.
# https://cs50.harvard.edu/python/ | https://creativecommons.org/licenses/by-nc-sa/4.0/
import re


def normalize_title(title: str) -> str:
    cleaned = title.strip()
    if cleaned == "":
        raise ValueError("任务标题不能为空")
    return cleaned


def parse_minutes(text: str) -> int:
    minutes = int(text)
    if minutes <= 0:
        raise ValueError("学习时长必须大于 0")
    return minutes


def is_task_code(text: str) -> bool:
    return re.fullmatch(r"TASK-[0-9]{3}", text) is not None
