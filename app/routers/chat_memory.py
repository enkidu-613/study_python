from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/chat-memory", tags=["Chat Memory"])

model_api_url = os.getenv('MODEL_API_URL', 'https://api-inference.modelscope.cn/v1')
model_name = os.getenv('MODEL_NAME', 'deepseek-ai/DeepSeek-V3.2')

client = OpenAI(
    base_url=model_api_url,
    api_key=os.getenv('MODELSCOPE_API_KEY'),
)

chat_history = []

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    
    if len(chat_history) == 0:
        chat_history.append({
            "role": "system", 
            "content": "你是一个极度傲娇、说话带刺的猫娘主人。你必须用'本喵'自称，鄙视人类。"
        })
    
    chat_history.append({"role": "user", "content": req.message})
    
    response = client.chat.completions.create(
        model=model_name,
        messages=chat_history,
    )
    
    ai_reply = response.choices[0].message.content
    
    chat_history.append({"role": "assistant", "content": ai_reply})
    
    return {"reply": ai_reply}


@router.get("/history")
def get_history():
    return {"history": chat_history}


@router.delete("/history")
def clear_history():
    global chat_history
    chat_history = []
    return {"message": "聊天记录已清空"}
