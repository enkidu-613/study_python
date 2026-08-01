# 试卷：WebSocket 实时通信 · 二次补考

> 生成时间：2026-06-16 | 章节：websocket-realtime | 类型：剩余错题收口
> 一轮共 5 题，目标 ≥ 4.5/5 🟢通关。

---

## 剩余错题收口（5题）

### 题1：Sec-WebSocket-Key 的身份

`Sec-WebSocket-Key` 是不是用户登录 token？它属于协议层还是业务层？

**答题区**：

```text
不是，属于协议层 客户端发送这个确认服务端是不是真的支持ws协议，如果支持服务端会计算这串随机字符串并加上ws固定或随机的字符串计算后返回客户端，使用Sec-WebSocket-Accept 返回
```

---

### 题2：Sec-WebSocket-Accept 的来源

服务器收到：

```http
Sec-WebSocket-Key: xxxxx
```

之后会返回：

```http
Sec-WebSocket-Accept: yyyyy
```

`Sec-WebSocket-Accept` 大概是怎么来的？它证明了什么？

**答题区**：

```text
如果支持服务端会计算这串随机字符串并加上ws固定或随机的字符串计算后返回客户端，使用Sec-WebSocket-Accept 返回
```

---

### 题3：正式认证的顺序

请补全一个正式认证版 WebSocket 路由。要求：

- token 错误时不建立连接
- close code 使用整数
- 认证失败后不要继续执行

```python
@router.websocket("/secure")
async def secure(ws: WebSocket, token: str = Query(...)):
    # 在这里补全
```

**答题区**：

```python
if token !== "true token"
	ws.close(code=4001,reason="token 错误")
	return
ws.accpet()
```

---

### 题4：教学调试的顺序

如果为了让 Hoppscotch 消息区能看到 `"token 错误"`，认证失败时应该采用什么顺序？

请用 3 个步骤写出来。

**答题区**：

```text
1.accpet
2.send_json
3.close code=4001
```

---

### 题5：真分房类型

为什么真正分房要写成：

```python
rooms: dict[str, list[WebSocket]]
```

请分别解释 `str` 和 `list[WebSocket]` 各代表什么，并写出一个数据形状。

**答题区**：

```python
# str 是key的类型，list[WebSocket]代表的是key的值类型
rooms_dict = {
	room_a:[ws1,ws2],
	room_b:[ws3,ws4]
}
```

---

> 答完后告诉我「答完了」，我会把批改结果追加到这份二次补考卷。

---

## 📝 批改结果（2026-06-16 · 二次补考）

| 题号 | 结果 | 得分 | 点评 |
|------|:----:|------|------|
| 1 | ✅ | 1/1 | 明确答出不是用户 token，属于协议层，并知道服务端会返回 `Sec-WebSocket-Accept` |
| 2 | ⚠️ | 0.75/1 | 方向正确：由客户端 key 加固定字符串计算得到；小细节：固定字符串不是随机字符串，是 RFC 规定的固定 GUID |
| 3 | ⚠️ | 0.75/1 | 认证顺序对：先判断 token，错了 close + return，再 accept；但代码有 Python 语法问题：应使用 `!=`、`await`，`accept` 拼写要正确 |
| 4 | ✅ | 1/1 | 教学调试顺序正确：`accept -> send_json -> close` |
| 5 | ✅ | 1/1 | 真分房结构已掌握：`str` 是房间 key，`list[WebSocket]` 是该房间连接列表 |

**总分**：4.5 / 5（90%）

**评定**：🟢 通关。WebSocket 阶段核心薄弱点已补齐。

### 最后保留的两个小提醒

1. `Sec-WebSocket-Accept` 的固定字符串不是随机的。

```text
Sec-WebSocket-Accept = base64(sha1(Sec-WebSocket-Key + 固定 GUID))
```

这个细节不影响你写业务代码，知道它是“协议握手校验”即可。

2. 正式认证代码要写成 Python 语法：

```python
@router.websocket("/secure")
async def secure(ws: WebSocket, token: str = Query(...)):
    if token != "true token":
        await ws.close(code=4001, reason="token 错误")
        return

    await ws.accept()
```

### 通关结论

你已经掌握：

- WebSocket HTTP Upgrade 握手的核心字段。
- `Sec-WebSocket-Key` 和业务 token 的边界。
- `Query(...)` 必填参数。
- WebSocket 正式认证与教学调试的差异。
- 真分房结构 `dict[str, list[WebSocket]]`。
- AI 可打断接口里的后台任务控制思路。
