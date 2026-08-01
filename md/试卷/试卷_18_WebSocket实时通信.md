# 试卷：WebSocket 实时通信

> 生成时间：2026-06-16 | 章节：websocket-realtime
> 三轮共 20 题，请在各题答题区填写答案。目标：≥ 18/20 🟢通关。

---

## 第一轮：基础概念（7题）

### 题1：HTTP vs WebSocket

用一句话解释：为什么说 WebSocket 像“打电话”，HTTP 像“寄信”？

**答题区**：

```text
websocket在建立连接之后，在断开之前会保持两边的通信，两遍可以随时互相发送信息，http请求一次返回一次，是被动的
```

---

### 题2：协议升级

WebSocket 连接刚开始握手时，底层一开始是 HTTP 还是 WebSocket？服务器返回哪个状态码表示升级成功？

**答题区**：

```text
HTTP 101
```

---

### 题3：为什么不能用普通 GET 测 WebSocket

下面这个地址为什么不能用普通 `GET` 测？

```text
http://127.0.0.1:8000/ws/message
```

正确测试 WebSocket 的地址应该是什么？

**答题区**：

```text
ws://
```

---

### 题4：FastAPI WebSocket 三行核心代码

下面三行分别做什么？

```python
await websocket.accept()
message = await websocket.receive_text()
await websocket.send_text(...)
```

**答题区**：

```text
接通通信
收取客户端发来的信息
服务器向客户端发送信息
```

---

### 题5：WebSocketDisconnect

`WebSocketDisconnect` 是什么情况下出现？如果不捕获，可能有什么问题？

**答题区**：

```text
在用户主动挂断连接的时候出现，不捕获可能会影响服务器其他服务
```

---

### 题6：Query(...)

`token: str = Query(...)` 在 WebSocket 参数里是什么意思？这里的 `...` 表示什么？

**答题区**：

```text
就是get请求放肆地址后面?token = *** 的查询参数
```

---

### 题7：Hoppscotch 测试 URL

你在 Hoppscotch 里写成：

```text
ws://127.0.0.1:8000/ws/message-auth?toekn=33333
```

为什么服务端不会进入 `token != "123456"` 那个判断？

**答题区**：

```text
token 拼写问题
```

---

## 第二轮：代码诊断（7题）

### 题8：WebSocket 里错误使用 HTTPException

下面这段代码有什么问题？应该怎么改？

```python
@router.websocket("/secure")
async def secure(ws: WebSocket, token: str = Query(...)):
    if token != "123456":
        raise HTTPException(status_code=401, detail="token 错误")
    await ws.accept()
```

**答题区**：

```text
客户端不会收到报错信息，好像在服务端也不会抛出？
```

---

### 题9：close reason 为什么看不到

为什么 Hoppscotch 有时看不到 `websocket.close(reason="token 错误")` 里的 reason，只显示“发生了一些错误”？

如果想让 Hoppscotch 消息区看到 `"token 错误"`，应该怎么做？

**答题区**：

```text
应该是，先连接accept，然后send，最后close
```

---

### 题10：room_id 的真实作用

教程里的：

```python
@router.websocket("/room/{room_id}")
```

这里的 `room_id` 语义上代表什么？它是不是代表个人？

**答题区**：

```text
语义上是代表房间id
```

---

### 题11：是否真的分房

如果 `ConnectionManager` 只有一个：

```python
active_connections: list[WebSocket] = []
```

那么 `/room/a` 和 `/room/b` 是否真的分房？为什么？

**答题区**：

```text
不是，只是id有区别
```

---

### 题12：真正按房间分组

真正按房间分组，连接池应该从 `list[WebSocket]` 变成什么结构？写出大概数据形状即可。

**答题区**：

```python
room_list:list[list[WebSocket]] = []
```

---

### 题13：ConnectionManager 的生产环境限制

为什么内存里的 `ConnectionManager` 不能直接用于多 worker 生产环境？一般用什么解决？

**答题区**：

```text
因为它是在内存里的，关闭后就会消失，而且python每个进程内存都是独立的互补共享，哪怕连接到了一个房间也会因为进程间内存不共享导致看不到对方的信息
```

---

### 题14：认证时 accept 前后区别

WebSocket 认证中，`accept()` 前验证和 `accept()` 后先发错误消息再关闭，各自适合什么场景？

**答题区**：

```text
后者适合需要返回验证不通过信息的事情
```

---

## 第三轮：场景应用（6题）

### 题15：SSE vs WebSocket

AI 只需要流式输出回答，用 SSE 还是 WebSocket 更合适？为什么？

**答题区**：

```text
SSE，因为不需要用户进行打断
```

---

### 题16：为什么打断 AI 需要 WebSocket

用户要中途打断 AI 生成，为什么 SSE 不够，WebSocket 更合适？

**答题区**：

```text
SSE貌似没有打断的方法，ws可以使用协程来关闭流式的函数
```

---

### 题17：create_task 的作用

可打断 AI WebSocket 里，为什么 AI 生成要放进：

```python
asyncio.create_task(...)
```

而不是直接：

```python
await stream_ai(...)
```

**答题区**：

```text
因为直接await就把协程对象交给py自动处理了，create_task是控制权在自己手里
```

---

### 题18：task.cancel()

收到：

```json
{"type": "stop"}
```

时，`task.cancel()` 大概做了什么？

**答题区**：

```text
找到绑定的task对象，停止运行
```

---

### 题19：项目里的 `/ws/ai-interrupt` 消息协议

你项目里的 `/ws/ai-interrupt` 约定了哪些消息类型？至少写出 `chat`、`stop`、`exit` 分别干什么。

**答题区**：

```text
chat 是向ai的流式函数发送信息 stop 是打断ai对话 stop 是让服务器关闭当前对话
```

---

### 题20：核心流程伪代码

用 5-10 行伪代码写出“收到 chat 开始生成，收到 stop 打断”的核心流程。

**答题区**：

```python
@router.websocket("/chat")
async def chat_ws(websocket:WebSocket):
	websocket.accept();
	message = await websocket.receive_json()
    chat_task = None
    try:
        if message["type"] == "chat":
            chat_task = asyncio.create_task(stream_ai(message["message"]))
            async for chunk in chat_task:
                await websocket.send_json(chunk)
        if message["type"] == "stop":
            if chat_task:
                chat_task.cancel()
                await chat_task
                await websocket.send_json({"type": "stop"})
	except WebSocketDisconnect:
		websocket.close(reason="client disconnected")
		return
```

---

> 答完所有题目后，告诉我「答完了」，我来逐题批改。

---

## 📝 批改结果（2026-06-16）

| 题号 | 结果 | 得分 | 点评 |
|------|:----:|------|------|
| 1 | ✅ | 1/1 | HTTP 一问一答、WebSocket 保持连接并双向通信，理解正确 |
| 2 | ✅ | 1/1 | HTTP 握手 + 101 升级，正确 |
| 3 | ⚠️ | 0.5/1 | 知道要用 `ws://`，但缺完整地址和原因：普通 GET 没有 WebSocket Upgrade 握手 |
| 4 | ✅ | 1/1 | accept / receive / send 三步理解正确 |
| 5 | ⚠️ | 0.75/1 | 主动断开方向对；更准确是客户端断开会让当前连接处理协程抛异常，不捕获会产生错误日志或异常退出 |
| 6 | ⚠️ | 0.75/1 | Query 参数方向对；漏了 `...` 表示必填 |
| 7 | ✅ | 1/1 | `toekn` 拼写错误导致 FastAPI 找不到必填 `token`，正确 |
| 8 | ❌ | 0.25/1 | 识别到客户端收不到正常错误，但没说核心：WebSocket 中不该用 `HTTPException`，应 `await ws.close(code=4001)` 或先 accept/send_json/close |
| 9 | ✅ | 1/1 | 先 `accept()` → `send_json()` → `close()`，正确 |
| 10 | ⚠️ | 0.75/1 | 知道是房间 id；漏答“不是个人 id” |
| 11 | ⚠️ | 0.75/1 | 知道不是真分房；更准确是所有连接在同一个 list，广播会发给所有房间 |
| 12 | ⚠️ | 0.5/1 | 知道要嵌套连接集合，但 `list[list[WebSocket]]` 缺少 room_id 映射；推荐 `dict[str, list[WebSocket]]` |
| 13 | ⚠️ | 0.75/1 | 多进程内存不共享说得很好；漏了生产方案：Redis Pub/Sub / broadcaster / 外部消息队列 |
| 14 | ⚠️ | 0.5/1 | 说对了 accept 后适合展示错误消息；漏了 accept 前适合正式认证、坏 token 不建立连接 |
| 15 | ✅ | 1/1 | 只需要服务器单向流式输出，用 SSE，正确 |
| 16 | ⚠️ | 0.75/1 | 方向对；更精确是 SSE 是服务端到客户端单向通道，客户端要另开 HTTP 请求才能表达 stop，而 WebSocket 可同连接双向发 stop |
| 17 | ⚠️ | 0.5/1 | “控制权在自己手里”方向对；核心是 AI 生成放到后台任务，主循环才能继续 `receive_json()` 收到 stop |
| 18 | ⚠️ | 0.75/1 | 大方向对；更准确是向任务注入取消请求，让协程在下一个 await 点抛 `CancelledError`，不是强杀线程 |
| 19 | ⚠️ | 0.5/1 | `chat`、`stop` 部分对；把 `exit` 写成了 stop，漏了 `exit` 是关闭 WebSocket 连接 |
| 20 | ❌ | 0.25/1 | 有 `create_task` 和 `cancel` 意识，但伪代码控制流不对：缺 `while True`，`async for chunk in chat_task` 不成立，直接流式会挡住 stop |

**总分**：14.25 / 20（71%）

**评定**：🟡 待补，不需要重学整章，但需要补 3 个关键点后再补考。

### 残存薄弱点

1. **WebSocket 认证错误处理**
   - HTTP 路由：`raise HTTPException(401)`
   - WebSocket 路由：`await ws.close(code=4001)`，或教学调试时 `accept -> send_json -> close`

2. **真正分房的数据结构**
   - 伪分房：`list[WebSocket]`
   - 真分房：`dict[str, list[WebSocket]]`

```python
rooms = {
    "python": [ws1, ws2],
    "ai": [ws3],
}
```

3. **AI 打断的控制流**
   - 主循环必须一直能 `receive_json()`。
   - AI 生成必须放进后台任务：`current_task = asyncio.create_task(...)`。
   - 收到 `stop` 后取消后台任务：`current_task.cancel()`。

### 标准伪代码

```python
current_task = None

while True:
    data = await websocket.receive_json()

    if data["type"] == "chat":
        if current_task and not current_task.done():
            await websocket.send_json({"type": "error", "message": "请先 stop"})
            continue
        current_task = asyncio.create_task(stream_ai(websocket, data["message"]))

    elif data["type"] == "stop":
        if current_task and not current_task.done():
            current_task.cancel()
            await websocket.send_json({"type": "stopped"})

    elif data["type"] == "exit":
        if current_task and not current_task.done():
            current_task.cancel()
        await websocket.close()
        break
```

### 补考建议

只补考 5 题即可，范围锁定在：

- `HTTPException` vs `websocket.close()`
- `dict[str, list[WebSocket]]` 真分房
- `create_task` 为什么不阻塞主循环
- `task.cancel()` 的真实含义
- `/ws/ai-interrupt` 的消息协议
