from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 创建 AI 路由
router = APIRouter(prefix="/ai", tags=["AI"])

# 初始化 OpenAI 客户端
client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key=os.getenv('MODELSCOPE_API_KEY'),
)# 使用OpenAI的规范，去连接自定义的模型，返回一个client对象

# 请求模型
class ChatRequest(BaseModel):
    message: str

# 生成器函数：流式响应
async def generate_stream(message: str):
    #这是一个扩展字参数的字典，标准的OpenAI API中没有这个参数，但是DeepSeek-V3.2模型支持这个参数
    extra_body = {"enable_thinking": True} # 这个参数触发了模型的思维链（CoT）能力
    
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-V3.2',# 请求模型名称
        messages=[{'role': 'user', 'content': message}], # 角色是用户，内容是用户的问题
        stream=True, #开启流式响应
        extra_body=extra_body #传递扩展字典
    )
    
    done_thinking = False
    
    for chunk in response:
        if chunk.choices:
            #当不为空的时候，走以下赋值和判断逻辑
            thinking = chunk.choices[0].delta.reasoning_content
            answer = chunk.choices[0].delta.content

            if thinking and thinking != '':
                data = {"type": "thinking", "content": thinking}
            elif answer and answer != '':
                if not done_thinking:
                    data = {"type": "divider", "content": "\n\n === Final Answer ===\n"}
                    done_thinking = True
                else:
                    data = {"type": "answer", "content": answer}
            else:
                #当为空的时候 跳过
                continue
            # json.dumps(data, ensure_ascii=False) 将字典转换为 JSON 字符串，确保中文字符不被转义
            # 给字符串添加 data：前缀 并加上两个换行符 '\n'
            # 这叫 Server-Sent Events (SSE)，是一种用于实时推送数据的协议
            # 它允许服务器向客户端发送数据，而无需客户端主动请求
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

# 路由端点
@router.post("/chat")
async def chat(req: ChatRequest): # 创建一个异步函数 用于创建聊天请求
    # 以前直接return一个字典
    # 现在把你的生成器函数扔进StreamingResponse里
    # StreamingResponse 是FastApi提供的一个特殊响应类，专门用于传输流式数据
    return StreamingResponse(
        generate_stream(req.message), # 把传送带接上
        media_type="text/event-stream"# 告诉浏览器，这是一个SSE协议的流式响应，让浏览器保持链接
    )
