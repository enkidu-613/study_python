from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from pydantic import SecretStr

import os

load_dotenv(dotenv_path=".env")

api_key = os.getenv("MODELSCOPE_API_KEY")
if not api_key:
    raise RuntimeError("MODELSCOPE_API_KEY 未配置")

store = {}

llm = ChatDeepSeek(
    model=os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2"),
    api_base=os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1"),
    api_key=SecretStr(api_key),
    temperature=0.7,
    streaming=False,
)

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的助手，能够回答用户的问题。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

first_answer = chain_with_history.invoke(
    {"question": "我叫 Enkidu。"},
    config={"configurable": {"session_id": "user-1"}},
)

second_answer = chain_with_history.invoke(
    {"question": "我叫什么？"},
    config={"configurable": {"session_id": "user-1"}},
)

print(first_answer)
print(second_answer)
