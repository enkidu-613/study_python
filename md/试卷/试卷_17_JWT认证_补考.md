# 试卷：JWT 认证 · 补考卷

> 生成时间：2026-06-12 | 章节：jwt-auth | 类型：补考（错题变种 + 陷阱题）
> 两轮共 7 题，目标 ≥ 6/7 🟢通关

---

## 第一轮：错题变种（5题）

### 题1：识别 bcrypt hash 结构

下面是一个 bcrypt hash，请标注每部分是什么：

```
$2b$12$L9qo8uLOickgx2ZMRZoMyeXjZIMs3xXcLmBxmq...
```

**答题区**：
```text
$2b$     → 版本号
$12$     → 成本因子
	L9qo8uLOickgx2ZMRZoMye  → 盐
XjZIMs3xXcLmBxmq...      → 这个不知道了
```

---

### 题2：JWT Payload 安全

JWT 的 Payload 段是 Base64 编码。有人说"既然是 Base64，我把密码也放 Payload 里没关系，反正别人看不懂"。这句话错在哪？

**答题区**：
```text
base64就是明文转编码，这是可逆的
```

---

### 题3：algorithms 不是装饰

```python
# 同事写的代码
jwt.decode(token, SECRET, algorithms="HS256")
```

代码 review 时你坚持要改成 `algorithms=["HS256"]`。同事说"就一个算法，列表和字符串有什么区别？"请用一句话解释——关键词中包含"攻击"。

**答题区**：
```text
这个是一个白名单，防止服务器被伪造token攻击
```

---

### 题4：场景判断 —— verify_exp=False 该不该加

以下三个场景，哪些**应该**设置 `options={"verify_exp": False}`？

A. 用户访问 `/auth/me` 查看个人信息
B. 用户点击"退出登录"
C. 管理员查看所有在线用户列表

**答题区**：
```text
退出登陆的时候，其余都不应该加入
```

---

### 题5：Depends 包裹的本质

```python
def require_role(*roles):
    def checker(user = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(403, "...")
        return user
    return Depends(checker)
```

如果最后一行改成 `return checker`（去掉 Depends），运行时会发生什么？

**答题区**：
```text
不会执行 该函数以及递归他里面的 Depends
```

---

## 第二轮：陷阱题（2题）

### 题6：陷阱 —— hash 相同吗？

```python
hash1 = bcrypt.hashpw(b"admin123", bcrypt.gensalt(rounds=10))
hash2 = bcrypt.hashpw(b"admin123", bcrypt.gensalt(rounds=10))
```

`hash1 == hash2` 是 True 还是 False？为什么？

**答题区**：
```text
hash不相同，因为每次生成的盐都是不同的
```

---

### 题7：陷阱 —— 两段式"JWT"

小明说他收到了一个"两段式的 JWT"：`xxxxx.yyyyy`（只有两段，没有第三段）。这个 Token 能被 `jwt.decode()` 正常验证通过吗？为什么？

**答题区**：
```text
不能因为 必须要有signature，把payload和header加在一起使用heder指定的算法再配一把密钥，得到的结果就是signatrue
```

---

> 答完后告诉我「答完了」。

---

## 📝 批改结果（2026-06-12 · 补考）

| 题号 | 结果 | 得分 | 点评 |
|------|:----:|------|------|
| 1 | ⚠️ | 0.75/1 | 版本号/成本因子/盐 全对，最后一段是**哈希值**（31字符） |
| 2 | ✅ | 1/1 | Base64 是编码不是加密，可逆，Payload 等于明文 |
| 3 | ⚠️ | 0.5/1 | "白名单""防伪造"方向对，但缺关键词：**算法混淆攻击**、**"none" 算法** |
| 4 | ✅ | 1/1 | 只有登出需要，验票/查列表都不该加 |
| 5 | ✅ | 1/1 | Depends 包裹 = 递归解析子依赖，去掉 = 依赖链断裂 |
| 6 | ✅ | 1/1 | 盐随机 → 同一密码两次 hash 不可能相同 |
| 7 | ✅ | 1/1 | 缺 Signature → jwt.decode 格式校验失败，清楚 JWT 三段关系 |

**总分**: 6.25 / 7（89%）
**评定**: 🟡 补漏（距通关 90% 差 1 题）

### 📊 对比上次

| | 第一次 | 补考 |
|------|:--:|:--:|
| 总分 | 75% | **89%** ↑ |
| bcrypt hash 结构 | 0.5 | **0.75** ↑ |
| JWT Payload 裸奔 | 0.5 | **1.0** ✅ |
| algorithms 安全 | 0.5 | 0.5 |
| verify_exp=False | 0.5 | **1.0** ✅ |
| Depends 包裹 | 0.5 | **1.0** ✅ |

### ⚠️ 残存薄弱点（仅1个）

**algorithms 安全原因**：你说了"白名单"和"防伪造"，但没说出攻击名。完整答案：

> `algorithms` 是列表 = **算法白名单**，防止**算法混淆攻击**（Algorithm Confusion Attack）。如果接受字符串，攻击者可以把算法设成 `"none"`，jwt.decode 跳过签名验证直接通过。

其余 6 个薄弱点全部消灭 ✅。
