import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from openai import AsyncOpenAI

load_dotenv()

MODEL_API_URL = os.getenv("MODEL_API_URL", "https://api-inference.modelscope.cn/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2")
async_client = AsyncOpenAI(
    base_url=MODEL_API_URL,
    api_key=os.getenv("MODELSCOPE_API_KEY"),
)

router = APIRouter(prefix="/ws", tags=["WebSocket"])


async def stream_ai_reply(websocket: WebSocket, message: str):
    try:
        extra_body = {"enable_thinking": True}
        stream = await async_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": message}],
            stream=True,
            extra_body=extra_body,
        )

        done_thinking = False

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            thinking = getattr(delta, "reasoning_content", None)
            answer = getattr(delta, "content", None)

            if thinking:
                await websocket.send_json({"type": "thinking", "content": thinking})
            elif answer:
                if not done_thinking:
                    await websocket.send_json({
                        "type": "divider",
                        "content": "\n\n === Final Answer ===\n",
                    })
                    done_thinking = True
                await websocket.send_json({"type": "answer", "content": answer})

        await websocket.send_json({"type": "done"})
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        await websocket.send_json({
            "type": "error",
            "message": f"AI 生成失败: {type(exc).__name__}",
        })


@router.get("/message-docs", summary="WebSocket /ws/message 使用说明")
async def websocket_message_docs():
    return {
        "websocket_url": "ws://127.0.0.1:8000/ws/message",
        "protocol": "text",
        "close_message": "exit",
        "description": "Swagger/OpenAPI 不直接展示 WebSocket 路由；这个 HTTP 接口用于在 /docs 中说明 WebSocket 的连接方式。",
        "browser_example": 'const ws = new WebSocket("ws://127.0.0.1:8000/ws/message"); ws.onmessage = (event) => console.log(event.data); ws.onopen = () => ws.send("你好");',
    }


@router.websocket("/message")
async def websocket_message(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            if message == "exit":
                await websocket.send_text("谢谢使用")
                await websocket.close()
                break
            await websocket.send_text(f"你说的是{message}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")


@router.websocket("/message-auth")
async def websocket_message_auth(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()

    if token != "123456":
        await websocket.send_json({
            "type": "error",
            "message": "token 错误",
        })
        await websocket.close(code=4001)
        return

    while True:
        message = await websocket.receive_text()
        if message == "exit":
            await websocket.send_text("谢谢使用")
            await websocket.close()
            break
        await websocket.send_text(f"你说的是{message}")


@router.websocket("/ai-interrupt")
async def websocket_ai_interrupt(websocket: WebSocket):
    await websocket.accept()
    current_task: asyncio.Task | None = None

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "exit":
                if current_task and not current_task.done():
                    current_task.cancel()
                await websocket.send_json({"type": "bye"})
                await websocket.close()
                break

            if message_type == "stop":
                if current_task and not current_task.done():
                    current_task.cancel()
                    try:
                        await current_task
                    except asyncio.CancelledError:
                        pass
                    await websocket.send_json({"type": "stopped"})
                else:
                    await websocket.send_json({
                        "type": "info",
                        "message": "当前没有正在生成的任务",
                    })
                current_task = None
                continue

            if message_type != "chat":
                await websocket.send_json({
                    "type": "error",
                    "message": "消息 type 只能是 chat、stop 或 exit",
                })
                continue

            message = data.get("message")
            if not isinstance(message, str) or not message.strip():
                await websocket.send_json({
                    "type": "error",
                    "message": "chat 消息必须包含非空 message 字符串",
                })
                continue

            if current_task and not current_task.done():
                await websocket.send_json({
                    "type": "error",
                    "message": "上一轮 AI 还在生成，请先发送 stop",
                })
                continue

            await websocket.send_json({"type": "started"})
            current_task = asyncio.create_task(
                stream_ai_reply(websocket, message.strip())
            )

    except WebSocketDisconnect:
        if current_task and not current_task.done():
            current_task.cancel()
    except Exception as exc:
        if current_task and not current_task.done():
            current_task.cancel()
        await websocket.send_json({
            "type": "error",
            "message": f"AI WebSocket 出错: {type(exc).__name__}",
        })
        await websocket.close(code=1011)


class ConnectionManager:
    def __init__(self):
        self.active_connections = list[WebSocket]()
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected: {websocket}")
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()

@router.websocket("/room/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            print(message,"这是收到的信息")
            if message == "exit":
                await websocket.send_text("谢谢使用")
                await websocket.close()
                await manager.disconnect(websocket)
                break
            await manager.broadcast(f"room {room_id} {message}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"有人离开了 {room_id}")
