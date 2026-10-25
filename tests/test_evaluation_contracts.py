from app.evals.contracts import EvaluationCase, evaluate_case


def test_rag_case_passes_when_expected_document_and_fact_exist():
    case = EvaluationCase(
        case_id="refund-001",
        user_input="退款需要几天内申请？",
        expected_document="退款规则",
        expected_fact="7 天内申请",
    )

    result = evaluate_case(
        case,
        retrieved_document_titles=["退款规则"],
        answer_text="请在 7 天内申请退款。",
    )

    assert result.retrieval_passed is True
    assert result.answer_passed is True
    assert result.passed is True


def test_agent_case_fails_when_required_tool_was_not_called():
    case = EvaluationCase(
        case_id="agent-001",
        user_input="查询知识库里的退款规则",
        expected_fact="7 天内申请",
        required_tool="search_knowledge_base",
    )

    result = evaluate_case(
        case,
        retrieved_document_titles=[],
        answer_text="退款需要在 7 天内申请。",
        called_tool_names=[],
    )

    assert result.answer_passed is True
    assert result.tool_usage_passed is False
    assert result.passed is False
