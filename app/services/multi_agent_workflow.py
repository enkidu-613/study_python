import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages.human import HumanMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from pydantic import SecretStr

from app.tools.knowledge_base import search_knowledge_base

load_dotenv()

api_key = os.getenv("MODELSCOPE_API_KEY")
if not api_key:
    raise RuntimeError("MODELSCOPE_API_KEY 未配置")

llm = ChatDeepSeek(
    api_base=os.getenv("MODEL_API_URL","https://tokenhub.tencentmaas.com/v1"),
    model=os.getenv("MODEL_NAME", "deepseek-v4-flash"),
    api_key=SecretStr(api_key),
    streaming=False,
)

# Subagent：负责查询项目知识库并返回证据。
# 它不直接面对用户，而是由 ask_research_agent Tool 调用。
research_agent = create_agent(
    model=llm,
    tools=[search_knowledge_base],
    system_prompt="你只负责检索知识项目并返回依据。",
)
# Tool 包装器：Supervisor 的模型可以为它生成 tool call。
# 它接收用户问题，调用 research_agent，并把检索证据返回给 Supervisor。
@tool
def ask_research_agent(question: str) -> str:
    """需要项目知识库证据时调用此函数"""
    result = research_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return result["messages"][-1].content
# Supervisor：主 Agent。
# 它在一次 invoke 中协调模型和工具循环，
# 接收 Subagent 返回的证据，并生成最终回答。
supervisor = create_agent(
    model=llm,
    tools=[ask_research_agent],
    system_prompt="""你负责理解用户问题；
        必要时调用研究助手，并给出最终回答，如果助手没有检测到相关知识库数据则禁止回答""",
)
result = supervisor.invoke(
    {"messages": [HumanMessage(content="秦始皇的丞相和中车府令是谁？")]}
)

print(result["messages"][-1].content)
