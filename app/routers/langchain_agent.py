from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.pregel.debug import RunnableConfig
from app.tools.knowledge_base import search_knowledge_base
from dotenv import load_dotenv
from pydantic import SecretStr

import os

load_dotenv()

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

agent = create_agent(
    model=llm,
    tools=[search_knowledge_base],
    system_prompt=(
        "你是一个严谨的知识库助手。"
        "如果问题需要项目知识库证据，先调用 search_knowledge_base 工具获取相关文档切片，并在回答中引用这些文档。"
        "回答时说明依据来自工具返回内容；如果没有证据，就明确说明没有检索到。"
    ),
    checkpointer = InMemorySaver(),  # 使用内存检查点
)

config:RunnableConfig ={
    "configurable": {
        "thread_id": "user-1-thread-1",
    }
}

first_result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "为我查找关于向量数据库关于秦始皇的描述，以及他是什么时候死的",
            }
        ]
    },
    config=config
)

second_result = agent.invoke(
    {
        "messages":[
            {
                "role": "user",
                "content": "上面的对话说了什么？",
            }
        ]
    },
    config=config
)

first_answer = first_result["messages"][-1].content
second_answer = second_result["messages"][-1].content

print("Agent Answer First:", first_answer)
print("Agent Answer Second:", second_answer)

for message in first_result["messages"]:
    print(type(message).__name__,message)
