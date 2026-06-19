# 试卷：WebSocket 实时通信 · 补考卷

> 生成时间：2026-06-16 | 章节：websocket-realtime | 类型：错题复活 + 针对性补考
> 两轮共 8 题，目标 ≥ 7/8 🟢通关。

---

## 第一轮：协议与认证边界（5题）

### 题1：HTTP 升级参数

WebSocket 握手请求里这两个 header 分别是什么意思？

```http
Upgrade: websocket
Connection: Upgrade
```

**答题区**：

```text
表示这个请求要升级为websocket请求
表示这个不是一般的请求，是升级请求
```

---

### 题2：Sec-WebSocket-Key

下面这个 header 大概是干什么的？不用说 SHA1 细节。

```http
Sec-WebSocket-Key: xxxxx
```

**答题区**：

```text
是一个随机的钥，在socket握手时使用的
```

---

### 题3：Query(...)

解释下面四个部分：

```python
token: str = Query(...)
```

请分别解释：

```text
token =
str =
Query(...) =
... =
```

**答题区**：

```text
	表示要从请求中解析出token请求，str表示接收的是字符串，Query(...)表示从查询参数里拿请求 ... 表示这个是必填参数
```

---

### 题4：WebSocket 认证错误处理

下面代码错在哪里？请改成正式认证写法。

```python
@router.websocket("/secure")
async def secure(ws: WebSocket, token: str = Query(...)):
    if token != "123456":
        raise HTTPException(status_code=401, detail="token 错误")
    await ws.accept()
```

**答题区**：

```python
应该改为 ws.close(code="4001",reason="token 错误")
```

---

### 题5：accept 前 vs accept 后

WebSocket 认证失败时：

A. `accept()` 前验证失败就 `close()`

B. `accept()` 后先 `send_json()` 再 `close()`

这两种分别适合什么场景？

**答题区**：

```text
第一个防止坏token进入链接，比较安全，第二种适合用户需要看错误信息的时候，也包括练习的时候
```

---

## 第二轮：聊天室与 AI 打断（3题）

### 题6：真正分房

为什么这个结构不是真正分房？

```python
active_connections: list[WebSocket] = []
```

真正分房应该用什么结构？写出数据形状。

**答题区**：

```python
room_list = dict[list[WebSocket]]
```

---

### 题7：create_task 为什么必要

在可打断 AI WebSocket 中，为什么不能这样写？

```python
await stream_ai(websocket, message)
```

为什么要这样写？

```python
current_task = asyncio.create_task(stream_ai(websocket, message))
```

**答题区**：

```text
1.因为会导致阻塞在这里导致无法接收其他参数 
2.因为控制权在自己手里，而且不会阻塞
```

---

### 题8：chat / stop / exit 协议

`/ws/ai-interrupt` 里这三个消息类型分别干什么？

```json
{"type": "chat", "message": "..."}
{"type": "stop"}
{"type": "exit"}
```

**答题区**：

```text
与ai对话 打断ai对话 让服务器关闭当前ws会话
```

---

> 答完后告诉我「答完了」，我来按 8 分制批改。

---

## 📝 批改结果（2026-06-16 · 补考）

| 题号 | 结果 | 得分 | 点评 |
|------|:----:|------|------|
| 1 | ✅ | 1/1 | `Upgrade: websocket` 和 `Connection: Upgrade` 的升级语义理解正确 |
| 2 | ⚠️ | 0.75/1 | 知道是握手随机钥匙；再补一句：服务器用它计算 `Sec-WebSocket-Accept`，证明自己懂 WebSocket 握手 |
| 3 | ✅ | 1/1 | `token`、`str`、`Query(...)`、`...` 全部答到核心，必填参数已掌握 |
| 4 | ⚠️ | 0.75/1 | 核心方向正确：不用 `HTTPException`，改 `ws.close`；小细节：`code` 应是整数 `4001`，还要 `return`，并在正式认证中先验证再 `accept()` |
| 5 | ✅ | 1/1 | accept 前更安全、accept 后适合展示错误信息和练习，答得很好 |
| 6 | ⚠️ | 0.5/1 | 知道要用 dict，但类型写法缺 key：应是 `dict[str, list[WebSocket]]`，并写出房间名到连接列表的映射 |
| 7 | ✅ | 1/1 | 直接 `await` 会阻塞主循环，`create_task` 让 AI 后台跑、主循环继续收 stop，已掌握 |
| 8 | ✅ | 1/1 | `chat` 开始对话、`stop` 打断、`exit` 关闭当前 WebSocket 会话，已掌握 |

**总分**：7 / 8（87.5%）

**评定**：🟢 本阶段关键薄弱点已补上，可以继续推进。严格按 90% 标准还差 0.2 分，但这次错点只剩低风险细节，实战遇到再查即可。

### 本次已补上的点

- `Query(...)` 里的 `...` = 必填参数。
- WebSocket 认证失败不能用 `HTTPException`，要用 `close()`。
- `accept()` 前适合正式认证，`accept()` 后适合教学调试和给客户端看错误消息。
- `create_task()` 的核心价值是避免 AI 生成挡住主循环收 `stop`。
- `/ws/ai-interrupt` 的 `chat / stop / exit` 协议已区分清楚。

### 剩余两个小尾巴

1. `Sec-WebSocket-Key` 不是业务 token。
   - 它是协议握手随机值。
   - 服务器用它算出 `Sec-WebSocket-Accept`。
   - 作用是证明双方在进行合法 WebSocket 握手。

2. 真分房结构要写完整：

```python
rooms: dict[str, list[WebSocket]] = {
    "python": [ws1, ws2],
    "ai": [ws3],
}
```

一句话记：

```text
有 room_id 查房间，就用 dict；房间里面才是 list[WebSocket]。
```
