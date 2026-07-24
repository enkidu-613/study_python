"""第 31 章：可独立运行的 Supervisor + Subagent 最小示例。"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from pydantic import SecretStr

from app.tools.knowledge_base import search_knowledge_base


load_dotenv()


def build_llm() -> ChatDeepSeek:
    """按项目现有 .env 配置创建聊天模型。"""
    api_key = os.getenv("MODELSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("MODELSCOPE_API_KEY 未配置")

    return ChatDeepSeek(
        model=os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2"),
        api_base=os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1"),
        api_key=SecretStr(api_key),
        temperature=0,
        streaming=False,
    )


def build_supervisor():
    """创建本章所需的 research_agent、Tool 包装和 supervisor。"""
    llm = build_llm()

    research_agent = create_agent(
        model=llm,
        tools=[search_knowledge_base],
        system_prompt=(
            "你是项目知识库检索员。每次收到问题都必须先调用 "
            "search_knowledge_base，再只根据工具返回的资料给出简短证据。"
        ),
    )

    @tool
    def ask_research_agent(question: str) -> str:
        """查询项目知识库并返回检索员给出的证据。"""
        subagent_result = research_agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        evidence = subagent_result["messages"][-1].content
        print("\n[research_agent 返回的证据]\n", evidence)
        return str(evidence)

    return create_agent(
        model=llm,
        tools=[ask_research_agent],
        system_prompt=(
            "你是本章的 supervisor 演示。每次收到问题都必须调用 "
            "ask_research_agent 一次，再基于它返回的证据给出最终回答。"
        ),
    )


def main() -> None:
    supervisor = build_supervisor()
    result = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "项目中的向量存储在哪里初始化？",
                }
            ]
        }
    )
    print("\n[supervisor 最终回答]\n", result["messages"][-1].content)


if __name__ == "__main__":
    main()
