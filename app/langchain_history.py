from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

history = InMemoryChatMessageHistory()

history.add_message(HumanMessage(content="你好，能帮我写一篇关于人工智能的文章吗？"))

history.add_message(AIMessage(content="当然可以！人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。AI技术包括机器学习、自然语言处理、计算机视觉等。它在医疗、金融、交通等各个领域都有广泛应用。未来，随着技术的不断发展，人工智能有望进一步改变我们的生活方式和工作方式。"))

print(history.messages)