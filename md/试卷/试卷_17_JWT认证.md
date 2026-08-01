# 试卷：JWT 用户认证

> 生成时间：2026-06-12 | 章节：jwt-auth
> 三轮共 12 题，请在各题答题区填写答案。

---

## 第一轮：基础概念（5题）

### 题1：认证 vs 授权 —— 401 vs 403

一个用户登录成功了（拿到了 JWT），但他的角色是 `USER`，他尝试访问 `/auth/admin`（需要 `ADMIN` 角色）。

**答题区**：

```text
他收到的是 401 还是 403？为什么？
403 因为他有角色而没有权限
```

---

### 题2：bcrypt 绞肉机 —— 盐从哪里来

注册时 `bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))` 生成了 hash 存入数据库。登录验证时 `bcrypt.checkpw(用户输入, 库里的hash)` 是如何工作的？盐从哪来的？

**答题区**：

```text
盐是库自动生成的 ，通过 bcrypt.gensalt(rounds=10) 延迟大约100ms，使得更难破解
```

---

### 题3：JWT 三段结构

JWT 的格式是 `xxxxx.yyyyy.zzzzz`。这三段分别叫什么？哪一段可以直接被任何人解码看到内容？

**答题区**：

```text
英文我忘记了，反正是用户信息 和 加密密钥 和加密类型
```

---

### 题4：Depends 链式执行顺序

```python
@app.get("/vip")
def vip(user: dict = Depends(get_current_user)):
    ...
```

当请求到达 `/vip` 时，`get_current_user` 自身又有 `Depends(security)` 和 `Depends(get_db)`。请用箭头写出完整的执行顺序：

**答题区**：

```text
前端请求 → `Depends(security)` 获取token -> `Depends(get_db)`查询是否有这个角色，但是你这边中间件是不是用错了，这个我记得知识获取用户信息的中间件，获取用户角色的是使用闭包的
```

---

### 题5：JWT 失效问题

JWT 最大的天然缺陷是什么？你的项目用了什么方案来补救？

**答题区**：

```text
无状态，退出登陆后仍旧可以被拿来使用，使用黑名单数据库来补救
```

---

## 第二轮：细节深挖（5题）

### 题6：登录失败时为什么要统一返回「账号或密码错误」而不是「用户不存在」？

```python
# routers/auth_router.py 登录逻辑
user = db.query(User).filter(User.username == dto.username).first()
if not user:
    raise HTTPException(status_code=401, detail="账号或密码错误")
if not bcrypt.checkpw(...):
    raise HTTPException(status_code=401, detail="账号或密码错误")
```

**答题区**：

```text
为了防止黑客遍历用户撞库
```

---

### 题7：`jwt.decode` 接受 `algorithms=["HS256"]` 是列表不是字符串，为什么？

**答题区**：

```text
可以使用多种加密方式，所以使用列表要好一点
```

---

### 题8：登出时 `options={"verify_exp": False}` 是干什么的？

登出的代码中对已经过期的 Token 仍然尝试解析 payload：

```python
payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                     options={"verify_exp": False})
```

**答题区**：

```text
过期也允许存入黑名单数据库
```

---

### 题9：黑名单为什么用 SHA256 前 64 位而不是存完整 Token？

```python
token_hash = hashlib.sha256(token.encode()).hexdigest()[:64]
```

**答题区**：

```text
？这个本质上就是对hash进行了转位16字符串的操作，转换后刚好就是64位也不需要截取了，不过怎么转的我有点忘了，反正就是二进制转32字节的数据转16进制字符串？
```

---

### 题10：`require_role` 为什么返回的是 `Depends(checker)` 而不是直接返回 `checker`？

```python
def require_role(*allowed_roles):
    def checker(user = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(403, ...)
        return user
    return Depends(checker)    # ← 为什么不是 return checker？
```

**答题区**：

```text
因为不使用闭包函数接收不到*allowed_roles
```

---

## 第三轮：场景应用（2题）

### 题11：代码补全 —— 写出 get_current_user 的核心逻辑

请补全以下代码（用 `# ...` 注释替代 you don't need to write everything）：

```python
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """验票机：提取 Bearer Token → 查黑名单 → 验签 → 返回用户身份"""
    token = credentials.credentials

    # ① 查黑名单

    # ② 验签

    # ③ 返回身份信息
```

**答题区**：

```python
token_hash = hashlib.sha256(token.encode()).hexdigest()
if db.query(Blacklist).filter(Blacklist.token_hash == token_hash).first():
    raise HTTPException(status_code=401, detail="Token 已在黑名单中")
try:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                         options={"verify_exp": False})
except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token 过期")
except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Token 无效")
---
上面这些混着ai补全写的，对库的的使用还是生疏
```


### 题12：诊断 Bug

小明写了这段代码，运行时发现所有接口都不需要 Token 就能访问，哪里出错了？

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_current_user(token: str = Header(...)):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    return payload

@app.get("/users/me")
def me(user = get_current_user):   # ← 出问题的行
    return {"user": user}
```

**答题区**：

```text
他没有使用依赖注入控制反转 Depends
```

---

> 答完所有题目后，告诉我「答完了」，我来逐题批改。

---

## 📝 批改结果（2026-06-12）

| 题号 | 结果 | 得分 | 点评 |
|------|:----:|------|------|
| 1 | ✅ | 1/1 | 401 vs 403 区分正确 |
| 2 | ⚠️ | 0.5/1 | 说了注册时盐自动生成，漏了 checkpw 验证时盐从存储 hash 字符串中提取 |
| 3 | ⚠️ | 0.5/1 | Payload 方向对，但第三段叫 Signature 不是"加密密钥" |
| 4 | ✅ | 1/1 | 正确识别 security→get_db 链路，且指出 /vip 只有验票没有角色校验——题目设计失误 |
| 5 | ✅ | 1/1 | 无状态缺陷 + 黑名单方案，完全正确 |
| 6 | ✅ | 1/1 | 防用户名枚举/撞库 |
| 7 | ⚠️ | 0.5/1 | "可用多种"对但不精确，核心是**防算法混淆攻击**（强制白名单） |
| 8 | ✅ | 1/1 | 过期也允许挂失 |
| 9 | ⚠️ | 0.5/1 | 技术过程对（SHA256→hex=64位），但没说**安全原因**：黑名单泄露不可逆 |
| 10 | ⚠️ | 0.5/1 | 解释了闭包工厂，但没答 Depends() 包裹原因：让 FastAPI 递归解析依赖链 |
| 11 | ⚠️ | 0.5/1 | 流程骨架对，但 ① 不该设 verify_exp=False（验票必须验过期）② 缺 return 用户字典 |
| 12 | ✅ | 1/1 | 少了 Depends 导致依赖链断裂 |

**总分**: 9 / 12（75%）
**评定**: 🟡 补漏

### ⚠️ 错题分析

#### ❌ 薄弱点 1：bcrypt.checkpw 的完整验证流程

你在题2中只答了注册时的盐生成，没说验证时 checkpw 怎么拿到盐。
**一句话记**: `$2b$10$SALT(22字符)HASH(31字符)` —— 盐就嵌在库里的 60 字符 hash 里，checkpw 提取→重哈希→对比。
```text
注册时：
    gensalt(10)  →  随机盐: "N9qo..." //同时会吧版本号和成本因子打进去
    hashpw("mypassword", "N9qo...")  →  60字符哈希
    存入数据库  →  $2b$10$N9qo...IeIjZIMs3xXcJ3...

验证时：
    用户输入: "mypassword"
    从数据库取出: $2b$10$N9qo...IeIjZIMs3xXcJ3...
    checkpw 内部：
        → 拆出盐: "N9qo..." // 按照$分割提取出两个关键信息 成本因子和盐
        → hashpw("mypassword", "N9qo...")  →  新哈希
        → 新哈希 == 库里的哈希?  →  True ✅
```

#### ❌ 薄弱点 2：JWT 三段精确命名

不知道第三段叫 Signature、第一段叫 Header。
**一句话记**: Header.Payload.Signature，Payload 是 Base64 裸奔的，**绝对不能放密码**。


#### ❌ 薄弱点 3：jwt.decode algorithms 安全原因

题7只说了"可以用多种"，没说出安全本质。
**一句话记**: `algorithms` 是列表 = **强制白名单**，防止攻击者传 `"none"` 绕过签名验证。

#### ❌ 薄弱点 4：get_current_user 代码细节

题11你 AI 补全写了 `verify_exp=False`，这在验票机里是严重错误——验票必须验过期！
**一句话记**: `verify_exp=False` 只在登出时用（过期也允许挂失），验票机绝不能用。

#### ❌ 薄弱点 5：return Depends(checker) 的真相

题10你答了闭包工厂（外层），但没答 Depends 包裹（内层）。
**一句话记**: 不用 `Depends()` 包裹，FastAPI 把 checker 当普通函数直接调，**不会**递归解析它内部的 `Depends(get_current_user)`。

### 🟢 强项（继续保持）

- ✅ 401 vs 403 区分清晰
- ✅ JWT 无状态缺陷和黑名单方案理解到位
- ✅ 统一错误信息防撞库的安全意识
- ✅ Depends 缺失导致的 Bug 能一眼诊断

---

## 🔁 重点复习卡（5个薄弱点）

> 每题一句话口诀 + 核心代码，考前扫一遍足矣。

---

### 复习 1：bcrypt.checkpw 完整流程  ← [原题 题2](#题2bcrypt-绞肉机--盐从哪里来)

**口诀**: `$2b$10$` + 盐22字符 + hash31字符 = 60字符全包，checkpw 提取盐→重哈希→对比

```python
# 库里存的 hash（60字符长这样）
# $2b$10$N9qo8uLOickgx2ZMRZoMyeIjZIMs3xXcJ3...

# 验证时 checkpw 内部等价于：
# ① 从 $2b$10$N9qo8uLOickgx2ZMRZoMye... 提取盐 "N9qo8uLOickgx2ZMRZoMye"
# ② new_hash = bcrypt.hashpw(用户输入, 提取的盐)
# ③ return new_hash == 库里的hash
bcrypt.checkpw(dto.password.encode(), user.password.encode())
```

---

### 复习 2：JWT 三段精确命名  ← [原题 题3](#题3jwt-三段结构)

**口诀**: **H**eader.**P**ayload.**S**ignature — HPS 记忆法。Payload = Base64 裸奔，别放密码！

```
eyJhbGciOiJIUzI1NiJ9  .  eyJzdWIiOiIxIn0  .  xxxxx_signature_xxxxx
     ↑ Header                ↑ Payload            ↑ Signature
  算法类型(Base64)      用户数据(Base64裸奔)     HMAC-SHA256签名
```

---

### 复习 3：algorithms 列表的安全原因  ← [原题 题7](#题7jwtdecode-接受-algorithmshs256-是列表不是字符串为什么)

**口诀**: 列表 = 白名单，防 `"none"` 算法绕过签名

```python
# ✅ 正确 — 显式声明只允许 HS256
jwt.decode(token, SECRET, algorithms=["HS256"])

# ❌ 如果允许字符串 "none"，攻击者可以：
# jwt.decode(fake_token, SECRET, algorithms="none")  # 直接不验签！
```

---

### 复习 4：verify_exp=False 只能登出用  ← [原题 题11](#题11代码补全--写出-get_current_user-的核心逻辑)

**口诀**: 验票必验过期，挂失才跳过

```python
# 验票机 get_current_user — 正常验过期
payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
# ❌ 绝不要加 options={"verify_exp": False}

# 登出 logout — 过期也允许挂失
payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                     options={"verify_exp": False})  # ✅ 仅此处
```

---

### 复习 5：return Depends(checker) 不是 return checker  ← [原题 题10](#题10require_role-为什么返回的是-dependschecker-而不是直接返回-checker)

**口诀**: 没有 `Depends()` 包裹 → FastAPI 不递归解析子依赖

```python
def require_role(*allowed_roles):
    def checker(user = Depends(get_current_user)):  # ← 子依赖
        if user["role"] not in allowed_roles:
            raise HTTPException(403, ...)
        return user
    return Depends(checker)  # ✅ 告诉 FastAPI: "checker 也是依赖，请解析它的 Depends()"
    # return checker         # ❌ FastAPI 当普通函数直接调，不会解析 Depends(get_current_user)
```

---

> 以上 5 张卡片覆盖了你本次全部薄弱点，3 天后回来重做只需看这一页。

