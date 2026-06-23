from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量读取配置
MODEL_API_URL = os.getenv('MODEL_API_URL', 'https://api-inference.modelscope.cn/v1')
MODEL_NAME = os.getenv('MODEL_NAME', 'deepseek-ai/DeepSeek-V3.2')

# 从环境变量读取 API Key
client = OpenAI(
    base_url=MODEL_API_URL,
    api_key=os.getenv('MODELSCOPE_API_KEY'),
)

# set extra_body for thinking control
extra_body = {
    # enable thinking, set to False to disable
    "enable_thinking": True
}

response = client.chat.completions.create(
    model=MODEL_NAME, # ModelScope Model-Id, required
    messages=[
        {
          'role': 'user',
          'content': '9.9和9.11谁大'
        }
    ],
    stream=True,
    extra_body=extra_body
)
done_thinking = False
for chunk in response:
    if chunk.choices:
        thinking_chunk = chunk.choices[0].delta.reasoning_content
        answer_chunk = chunk.choices[0].delta.content
        if thinking_chunk != '':
            print(thinking_chunk, end='', flush=True)
        elif answer_chunk != '':
            if not done_thinking:
                print('\n\n === Final Answer ===\n')
                done_thinking = True
            print(answer_chunk, end='', flush=True)
