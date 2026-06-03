from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建路由
router = APIRouter(prefix="/chat-memory", tags=["Chat Memory"])

# 初始化 OpenAI 客户端（从环境变量读取 Token）
model_api_url = os.getenv('MODEL_API_URL', 'https://api-inference.modelscope.cn/v1')
model_name = os.getenv('MODEL_NAME', 'deepseek-ai/DeepSeek-V3.2')

client = OpenAI(
    base_url=model_api_url,
    api_key=os.getenv('MODELSCOPE_API_KEY'),  # 从 .env 文件读取
)

# ⭐ 核心武器：一个存在于内存中的"聊天记录本"
# （注意：这是全局变量，重启程序就会清空，以后会存到数据库里）
chat_history = []

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    
    # 1. 【洗脑阶段】如果记录本是空的，塞入一条 system 指令
    if len(chat_history) == 0:
        chat_history.append({
            "role": "system", 
            "content": "你是一个极度傲娇、说话带刺的猫娘主人。你必须用'本喵'自称，鄙视人类。"
        })
    
    # 2. 【记录阶段】把用户刚说的话，追加到记录本里
    chat_history.append({"role": "user", "content": req.message})
    
    # 3. 【发请求阶段】把【完整的记录本】扔给大模型！
    response = client.chat.completions.create(
        model=model_name,
        messages=chat_history,  # ⭐ 不是只发一句，是把整个列表扔进去！
    )
    
    # 4. 【拿结果阶段】拿到 AI 的回答
    ai_reply = response.choices[0].message.content
    
    # 5. 【存档阶段】把 AI 的回答也追加到记录本里！下次循环它就能看见！
    chat_history.append({"role": "assistant", "content": ai_reply})
    
    return {"reply": ai_reply}


# 新增：获取聊天记录
@router.get("/history")
def get_history():
    """获取当前聊天记录"""
    return {"history": chat_history}


# 新增：清空聊天记录
@router.delete("/history")
def clear_history():
    """清空聊天记录"""
    global chat_history
    chat_history = []
    return {"message": "聊天记录已清空"}
