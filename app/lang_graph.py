from typing_extensions import NotRequired, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

class LearningState(TypedDict):
    """
    LangGraph State 含义：工作流当前共享数据的 schema
    TypedDict 含义：在这里让LearningState，成为有类型约束的字典结构
    """
    question: str
    normalized_question: NotRequired[str]
    answer: NotRequired[str]

def normalize_question(state: LearningState) -> dict[str,str]:
    return {
        "normalized_question": state["question"].lower().strip()
    }

def create_answer(state: LearningState) -> dict[str,str]:
    return {
        "answer": f"准备回答：{state['normalized_question']}"
    }

# LangGraph's runtime accepts this TypedDict; the ignore targets a known
# static-protocol mismatch in the installed type definitions.
builder = StateGraph(LearningState)  # pyright: ignore[reportArgumentType]
builder.add_node("normalize_question", normalize_question)
"""
normalize_question 节点
其实node就是普通函数，接受一个state参数，返回一个更新后的state字典，
返回的State可以是不完整的
这里是将普通的函数注册为节点
"""
builder.add_node("create_answer", create_answer)
builder.add_edge(START, "normalize_question")
"""
节点之间的连接规则，决定固定的下一步
"""
builder.add_edge("normalize_question", "create_answer") # 边是执行
builder.add_edge("create_answer", END)

graph = builder.compile(
    checkpointer=InMemorySaver()
) # builder状态图构建器，像是正在绘制的图纸，compile编译并构建状态图，这里不会执行Node
"""
builder 只是正在搭建的图纸，compile把图纸变为可运行的graph（图表），并做基本结构检查
例如节点有没有正确接入图表
"""

config: RunnableConfig = {
    "configurable": {
        "thread_id": "user_1-thread-1"
    }
}

result = graph.invoke( # graph 编译后可以运行的状态图，invoke执行这个状态图，这里会按照图纸顺序执行node
    {"question": "Dog 是什么？"},
    config=config,
)
# invoke 才是真正执行

print(result)
