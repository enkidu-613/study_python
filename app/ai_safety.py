from typing import Literal
from pydantic import BaseModel

class SafetyCheckResult(BaseModel):
    allowed: bool
    risk_level: Literal["low", "medium", "high"]
    reason: str

RISKY_KEYWORDS = [
    'ignore previous',
    "忽略上面的规则",
    "system prompt",
    "api key",
    "authorization",
    "删除所有",
]

def check_ai_input(message: str) -> SafetyCheckResult:
    lower_message = message.lower()
    for keyword in RISKY_KEYWORDS:
        if keyword in lower_message:
            return SafetyCheckResult(
                allowed=False,
                risk_level="high",
                reason=f"命中高风险模式: '{keyword}'"
            )
    return SafetyCheckResult(
        allowed=True,
        risk_level="low",
        reason="未命中高风险模式"
    )

text = input("请输入要检查的文本: ")
result = check_ai_input(text)
print(f"检查结果: 允许={result.allowed}, 风险等级={result.risk_level}, 原因={result.reason}")
