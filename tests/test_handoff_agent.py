import importlib
import sys
from typing import Any

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import BaseTool

import app.multi_agent as multi_agent


class AdaptiveFakeModel(BaseChatModel):
    """根据当前可见工具模拟 Handoff，不访问真实模型 API。"""

    visible_tool_names: list[str] = []
    bind_history: list[list[str]] = []
    next_tool_call_number: int = 1

    @property
    def _llm_type(self) -> str:
        return "adaptive-handoff-fake"

    def bind_tools(
        self,
        tools: Any,
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ) -> "AdaptiveFakeModel":
        del tool_choice, kwargs
        visible_tool_names = [
            tool.name if isinstance(tool, BaseTool) else str(tool["name"])
            for tool in tools
        ]
        self.bind_history.append(visible_tool_names.copy())
        return self.model_copy(
            update={"visible_tool_names": visible_tool_names}
        )

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        del stop, run_manager, kwargs
        latest_question = next(
            (
                str(message.content)
                for message in reversed(messages)
                if isinstance(message, HumanMessage)
            ),
            "",
        )

        if (
            "transfer_to_support" in self.visible_tool_names
            and ("登录" in latest_question or "401" in latest_question)
        ):
            message = self._tool_call("transfer_to_support", {})
        elif (
            "transfer_to_triage" in self.visible_tool_names
            and "天气" in latest_question
        ):
            message = self._tool_call("transfer_to_triage", {})
        elif "check_technical_issue" in self.visible_tool_names:
            message = self._tool_call(
                "check_technical_issue",
                {"question": latest_question},
            )
        else:
            latest_tool_result = next(
                (
                    str(message.content)
                    for message in reversed(messages)
                    if isinstance(message, ToolMessage)
                ),
                "没有工具结果",
            )
            message = AIMessage(content=f"最终回答：{latest_tool_result}")

        return ChatResult(generations=[ChatGeneration(message=message)])

    def _tool_call(self, name: str, args: dict[str, Any]) -> AIMessage:
        call_id = f"call-{self.next_tool_call_number}"
        self.next_tool_call_number += 1
        return AIMessage(
            content="",
            tool_calls=[
                {
                    "name": name,
                    "args": args,
                    "id": call_id,
                    "type": "tool_call",
                }
            ],
        )


def import_handoff_with_fake_model(
    monkeypatch: pytest.MonkeyPatch,
    fake_model: AdaptiveFakeModel,
):
    monkeypatch.setattr(multi_agent, "build_llm", lambda: fake_model)
    sys.modules.pop("app.services.handoff_agent", None)
    return importlib.import_module("app.services.handoff_agent")


def test_import_does_not_build_model(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called():
        raise AssertionError("导入模块时不应该创建或调用模型")

    monkeypatch.setattr(multi_agent, "build_llm", fail_if_called)
    sys.modules.pop("app.services.handoff_agent", None)

    importlib.import_module("app.services.handoff_agent")


def test_each_user_question_runs_technical_check_once(
    monkeypatch: pytest.MonkeyPatch,
):
    fake_model = AdaptiveFakeModel()
    module = import_handoff_with_fake_model(monkeypatch, fake_model)
    agent = module.build_handoff_agent(model=fake_model)
    config = module.build_thread_config("check-once")

    first_result = agent.invoke(
        {"messages": [{"role": "user", "content": "我的登录一直报错"}]},
        config=config,
    )
    second_result = agent.invoke(
        {"messages": [{"role": "user", "content": "错误码是401"}]},
        config=config,
    )

    technical_checks = [
        message
        for message in second_result["messages"]
        if isinstance(message, ToolMessage)
        and message.name == "check_technical_issue"
    ]

    assert len(technical_checks) == 2
    assert "401 通常表示认证失败" in technical_checks[-1].content
    assert first_result["active_agent"] == "support_agent"
    assert config["recursion_limit"] <= 20


def test_support_role_can_handoff_back_to_triage(
    monkeypatch: pytest.MonkeyPatch,
):
    fake_model = AdaptiveFakeModel()
    module = import_handoff_with_fake_model(monkeypatch, fake_model)
    agent = module.build_handoff_agent(model=fake_model)
    config = module.build_thread_config("return-to-triage")

    agent.invoke(
        {"messages": [{"role": "user", "content": "我的登录一直报错"}]},
        config=config,
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "今天天气怎么样"}]},
        config=config,
    )

    return_messages = [
        message
        for message in result["messages"]
        if isinstance(message, ToolMessage)
        and message.name == "transfer_to_triage"
    ]

    assert len(return_messages) == 1
    assert result["active_agent"] == "triage_agent"
