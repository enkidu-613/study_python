"""第 37 至 39 章：不访问模型的最小评估运行入口。"""

from app.evals.contracts import EvaluationCase, evaluate_case


def main() -> None:
    case = EvaluationCase(
        case_id="refund-001",
        user_input="退款需要几天内申请？",
        expected_document="退款规则",
        expected_fact="7 天内申请",
        required_tool="search_knowledge_base",
    )
    result = evaluate_case(
        case,
        retrieved_document_titles=["退款规则", "账户帮助"],
        answer_text="根据退款规则，需要在 7 天内申请。",
        called_tool_names=["search_knowledge_base"],
    )
    print(result.model_dump())
    print(f"passed={result.passed}")


if __name__ == "__main__":
    main()
