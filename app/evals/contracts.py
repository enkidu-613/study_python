"""用确定性规则检查 RAG 与 Agent 的关键行为。"""

from __future__ import annotations

from pydantic import BaseModel


class EvaluationCase(BaseModel):
    """一条可重复执行的 AI 应用测试用例。"""

    case_id: str
    user_input: str
    expected_fact: str
    expected_document: str | None = None
    required_tool: str | None = None


class EvaluationResult(BaseModel):
    """确定性检查的结果，不调用任何模型。"""

    case_id: str
    retrieval_passed: bool
    answer_passed: bool
    tool_usage_passed: bool

    @property
    def passed(self) -> bool:
        return (
            self.retrieval_passed
            and self.answer_passed
            and self.tool_usage_passed
        )


def evaluate_case(
    case: EvaluationCase,
    *,
    retrieved_document_titles: list[str],
    answer_text: str,
    called_tool_names: list[str] | None = None,
) -> EvaluationResult:
    """检查检索命中、答案事实和必须调用的工具是否符合预期。"""
    retrieved_titles = {title.strip() for title in retrieved_document_titles}
    called_tools = set(called_tool_names or [])

    retrieval_passed = (
        case.expected_document is None
        or case.expected_document in retrieved_titles
    )
    answer_passed = case.expected_fact in answer_text
    tool_usage_passed = (
        case.required_tool is None or case.required_tool in called_tools
    )

    return EvaluationResult(
        case_id=case.case_id,
        retrieval_passed=retrieval_passed,
        answer_passed=answer_passed,
        tool_usage_passed=tool_usage_passed,
    )
