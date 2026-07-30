from collections.abc import Callable
from typing import Any, cast

from langchain.agents import (
    AgentState,
    create_agent,
)
from langchain.agents.middleware import (
    ModelRequest,  # 本次模型调用的框架请求，包含 State、Prompt、tools 等配置。
    ModelResponse,  # handler 完成模型调用后返回给 middleware 的响应。
    wrap_model_call,  # 把函数注册成每次调用模型前都会经过的 middleware。
)
from langchain.messages import SystemMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools.base import BaseTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from typing_extensions import NotRequired

from app.multi_agent import build_llm


# 下面的编号表示一次 invoke() 的实际运行顺序，不是这份文件从上到下的定义顺序。
# Python 会先完成函数和 Agent 的定义；真正的数据流从文件底部的 invoke() 开始。


class HandoffState(AgentState):
    # AgentState 已经提供 messages；这里额外记录当前使用哪一套角色配置。
    active_agent: NotRequired[str]


@tool
def transfer_to_support(
    runtime: ToolRuntime[None, HandoffState],
) -> Command:
    """发现技术问题时，将当前会话转入支持角色模式"""
    # 7. 模型发出 transfer_to_support 的 tool call 后，框架执行本工具并注入 runtime。
    # ToolRuntime 的第一个类型参数表示没有自定义 context，第二个表示 State 是 HandoffState。
    if runtime.tool_call_id is None:
        raise RuntimeError("transfer_to_support 必须由 Agent 的工具调用触发")

    # Command 不是直接修改对象，而是要求框架同时更新 messages 和 active_agent。
    # tool_call_id 把这条 ToolMessage 与模型刚才发出的那次工具调用对应起来。
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content="已转交给支持角色。",
                    name="transfer_to_support",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "active_agent": "support_agent",
        }
    )


# 8. transfer_to_support 返回 Command 后，Agent 把更新合并进 State。
# Agent 发现工具调用已经完成但还没有最终回答，于是再次进入模型调用阶段。


@tool
def transfer_to_triage(
    runtime: ToolRuntime[None, HandoffState],
) -> Command:
    """当前问题不属于技术支持时，将会话交还给分诊角色。"""
    if runtime.tool_call_id is None:
        raise RuntimeError("transfer_to_triage 必须由 Agent 的工具调用触发")

    return Command(
        update={
            "messages": [
                ToolMessage(
                    content="已交还给分诊角色。",
                    name="transfer_to_triage",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "active_agent": "triage_agent",
        }
    )


@tool
def check_technical_issue(question: str) -> str:
    """根据问题中的明确信息返回基础技术检查结果。"""
    # 10. 支持角色调用本工具；框架把返回字符串包装成 ToolMessage 并追加到 messages。
    # 模型读取工具结果后再次运行；当它返回普通回答且不再发出 tool call 时，Agent loop 结束。
    normalized_question = question.lower()
    if "401" in normalized_question or "unauthorized" in normalized_question:
        return (
            "检查结果：HTTP 401 通常表示认证失败。"
            "请检查 Authorization 请求头、Token 是否过期，以及 Token 格式是否正确。"
        )
    if "登录" in question:
        return (
            "检查结果：这是登录链路问题。"
            "请先核对账号状态、请求地址、请求体字段和服务端认证日志。"
        )
    return "检查结果：现有信息不足，请补充错误码、请求地址和服务端错误日志。"


def current_question_has_check_result(state: HandoffState) -> bool:
    """判断最新一条用户消息之后是否已经产生技术检查结果。"""
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            return False
        if (
            isinstance(message, ToolMessage)
            and message.name == "check_technical_issue"
        ):
            return True
    return False


def select_prompt(state: HandoffState) -> str:
    """根据共享 State 选择下一次模型调用使用的角色 Prompt。"""
    if state.get("active_agent") == "support_agent":
        if current_question_has_check_result(state):
            return (
                "你是支持角色。当前问题已经完成技术检查，"
                "请直接根据最新工具结果给出简短回答，不要再次调用工具。"
            )
        return (
            "你是支持角色。技术问题先调用 check_technical_issue；"
            "如果当前问题与技术支持无关，调用 transfer_to_triage。"
            "回答必须以工具结果为依据。"
        )
    return "你是分诊角色。遇到技术问题必须调用transfer_to_support。"


@wrap_model_call
def apply_role_config(
    request: ModelRequest,  # 3.1 框架注入本轮即将发送给模型的请求。
    handler: Callable[[ModelRequest], ModelResponse],  # 3.2 框架注入继续调用模型的函数。
) -> ModelResponse:
    """每次模型调用前，按 active_agent 覆盖本次的 Prompt 与 tools。"""
    # Callable[[ModelRequest], ModelResponse] 表示：
    # handler 接收一个 ModelRequest，调用后返回一个 ModelResponse。
    state = cast(HandoffState, request.state)

    # 4. 第一次运行时没有 active_agent，选择分诊 Prompt。
    # 9. 第 8 步让 Agent 再次运行本 middleware，此时读到 support_agent，改选支持 Prompt。
    prompt = select_prompt(state)

    available_tools: list[BaseTool | dict[str, Any]]
    # 4.1 分诊阶段只暴露转交工具；支持阶段可以检查问题或交还分诊。
    # 最新用户问题已经检查过时不再暴露工具，防止模型重复调用形成 Agent loop。
    if state.get("active_agent") == "support_agent":
        if current_question_has_check_result(state):
            available_tools = []
        else:
            available_tools = [check_technical_issue, transfer_to_triage]
    else:
        available_tools = [transfer_to_support]

    # 5. 根据原 request 创建仅用于本次模型调用的新请求，不直接修改共享 State。
    updated_request = request.override(
        system_message=SystemMessage(content=prompt),
        tools=available_tools,
    )

    # 6. 把改好的请求交给 handler，框架才会继续请求模型。
    # 第一次模型调用会根据分诊 Prompt 发出 transfer_to_support 的 tool call。
    return handler(updated_request)


def build_handoff_agent(model: BaseChatModel | None = None):
    """创建 Handoff Agent；导入本模块时不连接模型服务。"""
    return create_agent(
        model=model or build_llm(),
        # 这里注册所有候选 Tool；apply_role_config 会按角色选择本次真正暴露给模型的子集。
        tools=[
            transfer_to_support,
            check_technical_issue,
            transfer_to_triage,
        ],
        state_schema=HandoffState,
        middleware=[apply_role_config],  # 3. Agent 每次准备调用模型前，框架先运行这个 middleware。
        checkpointer=InMemorySaver(),  # 2. 按 thread_id 查找旧快照；首次没有快照，就从输入 State 开始。
    )


def build_thread_config(thread_id: str) -> RunnableConfig:
    """创建带有限递归上限的会话配置。"""
    return {
        "configurable": {
            "thread_id": thread_id,
        },
        "recursion_limit": 12,
    }


def main() -> None:
    """运行两轮 Handoff 演示。"""
    handoff_agent = build_handoff_agent()
    thread_config = build_thread_config("handoff-demo-user-1")

    # 1. invoke 接收用户消息，并通过 config 中的 thread_id 把本次运行绑定到同一会话线程。
    handoff_agent.invoke(
        {"messages": [HumanMessage(content="我的登录一直报错")]},
        config=thread_config,
    )

    # 11. 第一次 Agent loop 结束后，checkpointer 保存最终 State，invoke 返回同一份最终 State。
    # 第二次使用相同 thread_id，会在第 2 步恢复 active_agent="support_agent"，再重复后续流程。
    second_result = handoff_agent.invoke(
        {"messages": [HumanMessage(content="错误码是401")]},
        config=thread_config,
    )

    print(second_result["messages"][-1].content)


if __name__ == "__main__":
    main()
