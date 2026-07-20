import os

from dotenv import load_dotenv
from langchain_core.messages.human import HumanMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langgraph.pregel.debug import RunnableConfig
from pydantic import SecretStr
from app.tools.knowledge_base import search_knowledge_base

load_dotenv()
tools = [search_knowledge_base]
api_key = os.getenv("MODELSCOPE_API_KEY")
if not api_key:
    raise RuntimeError("MODELSCOPE_API_KEY 未配置")

llm = ChatDeepSeek(
    model=os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2"),
    api_base=os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1"),
    api_key=SecretStr(api_key),
    temperature=0.7,
    streaming=False,
)

model_with_tools = llm.bind_tools(tools)


def call_model(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools)

builder = StateGraph(MessagesState)

builder.add_node("model", call_model)
builder.add_node("tools", tool_node)

builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")

graph = builder.compile(checkpointer=InMemorySaver())

config:RunnableConfig = {
    "configurable":{
        "thread_id":"dome-thread-1"
    }
}

result = graph.invoke(
    {
        "messages":[
            HumanMessage(content="为我从资料库里查找关于秦始皇巡游的记载")
        ]
    },
    config=config
)

print(result)
