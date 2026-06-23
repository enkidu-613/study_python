from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI"])

MODEL_API_URL = os.getenv('MODEL_API_URL', 'https://api-inference.modelscope.cn/v1')
MODEL_NAME = os.getenv('MODEL_NAME', 'deepseek-ai/DeepSeek-V3.2')

client = OpenAI(
    base_url=MODEL_API_URL,
    api_key=os.getenv('MODELSCOPE_API_KEY'),
)

class ChatRequest(BaseModel):
    message: str

async def generate_stream(message: str):
    extra_body = {"enable_thinking": True}
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': message}],
        stream=True,
        extra_body=extra_body
    )
    
    done_thinking = False
    
    for chunk in response:
        if chunk.choices:
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
                continue
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

@router.post("/chat")
async def chat(req: ChatRequest):
    return StreamingResponse(
        generate_stream(req.message),
        media_type="text/event-stream"
    )
