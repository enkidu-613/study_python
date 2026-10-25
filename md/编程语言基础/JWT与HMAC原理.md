# JWT 与 HMAC 原理

> 本章学什么：JWT 三段的真实结构、签名到底怎么算出来的、为什么签名必须覆盖 header、编码/加密/混淆/签名四个词的区别。
> 本章不学什么：不学怎么用 JWT 保护路由（那是 `17_JWT用户认证.md` 的事）、不学 bcrypt、不学 OAuth/OIDC。
> 与 17 章的分工：17 章教你"怎么用"（复制 `get_current_user` 模板）；本章教你"底层怎么工作"（签名是 HMAC 算出来的指纹，不是加密）。

---

## 1. 核心问题：服务器怎么"不记你"却验证你

### 无状态认证的一句话理解

**Session（老办法）**：登录后服务器把"你是谁"记在内存/数据库里，发你一个 ID 卡号，每次请求拿卡号来查。

**JWT（新办法）**：登录后服务器把"你是谁"写进一张**盖章的通行证**发给你，之后**服务器什么都不记**，只看通行证的印章对不对、过期了没。

> 这就是为什么 JWT 叫"无状态"——验证所需的全部信息都在令牌里，服务器不用查库。

### 生活类比

JWT 是一张**盖了服务器专属印章的数字身份卡**：

- 卡面内容（你是谁、什么时候过期）——谁都能读
- 印章（签名）——只有服务器能盖，别人盖不出来

用户能**看**卡面，但不能**改**卡面——一改，印章就对不上了。

---

## 2. JWT 三段结构

你登录后拿到的 access token 长这样（真实示例来自本项目 `server/app/auth/service.py:73-86`）：

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMTEx... .Wj5Q7jE8Zk3y...
└── 段1: header ──┘ └── 段2: payload ──┘   └── 段3: 签名 ──┘
```

| 段 | 内容 | 谁能读 | 处理方式 |
|---|---|---|---|
| header | `{"alg":"HS256","typ":"JWT"}` —— 声明用什么算法签名 | 任何人（base64 解码即见） | 编码 |
| payload | `sub`(用户ID)、`email`、`exp`(过期)、`iat`、`jti`... | 任何人（base64 解码即见） | 编码 |
| 签名 | HMAC-SHA256 输出的 32 字节指纹 | 可见，但无法反推密钥 | 指纹 |

**关键事实：JWT 三段全都是 base64url 编码，不是加密。** 任何人拿到 token 都能解码出你的 user_id、email——这不是漏洞，是设计。安全性全靠第三段签名保证"内容没被改过"。

---

## 3. 签名到底怎么算的

### 3.1 一句话

```
签名段 = HMAC-SHA256( token_signing_key, header编码 + "." + payload编码 )
```

**输入是 header 和 payload 的 base64 编码拼起来**（中间一个点），不是原始 JSON，也不是只有 payload。

### 3.2 项目里的实际代码

```python
# server/app/auth/service.py:71-86 —— 签发
def issue(self, user_id, email):
    return jwt.encode(
        {
            "iss": "studyflow-api",
            "aud": "studyflow-client",
            "sub": str(user_id),      # 你是谁
            "email": email,
            "type": "access",
            "jti": str(uuid4()),      # 令牌唯一 ID
            "iat": int(now.timestamp()),          # 签发时间
            "exp": int((now + ttl).timestamp()),  # 过期时间
        },
        self._signing_key,            # ← token_signing_key 就是它
        algorithm="HS256",
    )
```

`jwt.encode` 内部调用的就是 Python 标准库（你不用自己写）：

```python
import hmac, hashlib
signature = hmac.new(
    signing_key,                 # token_signing_key
    b"header.payload",           # 前两段 base64 拼起来
    hashlib.sha256,
).digest()                       # 32 字节（256 bit）指纹
```

### 3.3 底层数学结构（RFC 2104，了解即可）

HMAC 不是"把密钥拼进消息再哈希"这么简单，而是两次哈希防止长度扩展攻击：

```
HMAC(K, m) = H( (K ⊕ opad) || H( (K ⊕ ipad) || m ) )
                └─外层哈希─┘   └────内层哈希────┘

其中：
  H    = SHA-256
  K    = token_signing_key（补齐到块长 64 字节）
  ipad = 0x36 重复 64 次
  opad = 0x5c 重复 64 次
  ||   = 字节拼接
  ⊕    = 按位异或
```

### 3.4 类比：印章与印痕

```
token_signing_key  = 印章本身（存在服务器保险柜）
token 里的签名段   = 盖在纸上的印痕（谁都能看，但印不出印章）
```

印痕看得见，但无法从印痕逆向铸造出印章——因为 HMAC-SHA256 是单向函数，知道输入和输出也无法反推密钥（256 bit 密钥空间暴力搜索不可行）。

---

## 4. 为什么签名必须覆盖 header

### 一句话

**header 里声明了"我用什么算法签名"，而签名必须保护这个声明本身**——否则攻击者改 header 就能让服务器按攻击者指定的方式验证（甚至不验证）。

### 攻击演示：算法混淆攻击

如果签名只覆盖 payload、不覆盖 header：

```
用户原本的 token：H₁.P.S₁      （H₁ 声明 HS256）
攻击者篡改：     H₂.P.S₁      （H₂ 改成 {"alg":"none"}）
```

- 服务器解码 header 看到 `alg=none` → 按"不签名"处理 → **完全绕过验证，任意伪造身份**
- 或者改成 `alg=RS256` → 服务器若误信，可能用错误的密钥路径验证

这是 JWT 历史上真实的漏洞（2015-2017 年大量库中招）。

### 签名覆盖 header 后

```
签名段 = HMAC(key, base64(header) + "." + base64(payload))
```

攻击者一改 header（哪怕一个字母），重算出的签名就和第三段对不上 → 401 拒绝。

**签名范围 = 所有会被解码执行的内容。** header 决定验证方式、payload 决定身份，两个都要被保护。

### 项目里的双重防线

```python
# server/app/auth/service.py:90-92 —— 验证
jwt.decode(
    token,
    self._signing_key,
    algorithms=["HS256"],   # 服务器只接受 HS256，防算法混淆
    ...
)
```

- 签名覆盖 header → header 无法被篡改（第一道防线）
- 服务器硬编码 `algorithms=["HS256"]` → 即使塞个 `alg:none` 的 token 也直接拒绝（第二道防线）

### 类比

header 像合同封面上的"本文件用 XX 印章"。印章（签名）必须同时盖住封面声明和正文——否则撕掉封面换一张写着"无需盖章"的封面，正文就绕过验证了。

---

## 5. 编码 ≠ 加密 ≠ 混淆 ≠ 签名

这四个词最容易混，一张表分清：

| 维度 | 编码 encoding | 加密 encryption | 混淆 obfuscation | 签名 signing (HMAC) |
|---|---|---|---|---|
| 目的 | 换表示形式 | 藏内容 | 让人读不懂 | 证明没被改 + 认证来源 |
| 可逆性 | ✅ 可逆（解码即读） | ✅ 可逆（有密钥） | 通常可逆（费劲） | ❌ 完全不可逆 |
| 密钥参与 | ❌ 不需要 | ✅ 需要 | 不一定 | ✅ 必须用 token_signing_key |
| 安全来源 | 无（公开） | 密钥保密 | 靠"难看"（不提供真正安全） | 密钥保密 |
| token 里的例子 | header、payload | 无（JWT 不用加密段） | 无 | 第三段 |

### 记忆锚点

```
编码 = 换形式（可读）
加密 = 藏内容（可逆）
混淆 = 装难看（可还原）
签名 = 指纹（不可逆 + 密钥参与 + 防篡改）
```

**你的 token 里：前两段是"编码"，第三段是"指纹"，没有一段是"加密"。** 这也正是为什么 token 里不能放密码、API Key——因为除了签名段，其余内容谁都能读出来。

---

## 6. 盐（salt）和签名密钥的区别

### 一句话

**盐是"打散器"（公开，不保密）；签名密钥是"印章"（机密，必须藏好）。** 两者都是随机 hex 字符串，但用途完全不同。

| 维度 | 盐 salt | token_signing_key |
|---|---|---|
| 用途 | 密码哈希随机化：相同密码 → 不同哈希 | JWT 签名/验签 |
| 谁持有 | 随哈希一起存储，**非机密** | **机密**，仅服务器持有 |
| 泄漏后果 | 无（本来就存着） | 可伪造任意用户的令牌 |
| 长度要求 | 16 字节左右即可 | ≥32 字节（本项目生成 32B/256bit） |
| 每个实例 | 每个密码哈希一个 | 全局唯一 |

### 项目里的盐在哪（自动管理，不用你管）

| 位置 | 用法 |
|---|---|
| 密码哈希 | `argon2-cffi` 的 `PasswordHasher`（`service.py:133`）每次 `hash(password)` 自动生成随机盐，嵌入哈希字符串：`$argon2id$v=19$m=65536,t=3,p=4$<盐>$<哈希>` |
| 备份加密 | `infra/backup/backup.sh` 的 `openssl enc -aes-256-cbc -pbkdf2`——PBKDF2 的盐由 OpenSSL 自动生成并存在加密文件头部 |

### 为什么容易混淆

两者都以随机值形式出现、都参与密码学计算、都是 hex 字符串——但：

- 盐**不保密**，只是打散相同输入的输出
- 签名密钥**必须保密**，它本身就是认证的信任根

---

## 7. 签发与验证完整流水线

### 签发（登录成功时，4 步）

```
① 组装 header  = {"alg":"HS256","typ":"JWT"}          → base64url → H
② 组装 payload = {sub, email, exp, iat, jti, ...}      → base64url → P
③ 计算签名     = HMAC-SHA256(token_signing_key, H+"."+P) → 32字节 → S
④ 拼成 token   = H + "." + P + "." + base64url(S)
```

### 验证（每次请求时，4 步）

```
收到 token = H.P.S
① base64 解码 P → 读取 user_id、email、exp（读取身份，不依赖签名）
② 重算 HMAC(key, H + "." + P) → 得到 S'
③ 比对 S' 与 S
    ├─ 相等 → 身份可信，继续校验
    └─ 不等 → 有人改了 H 或 P → 401 拒绝
④ 检查剩余项（service.py:96-106）：
    ├─ exp 没过期（15 分钟有效期）
    ├─ iat 不晚于当前（防未来时间戳）
    └─ type == "access"（防止拿 refresh token 当 access 用）
```

### 项目里的验证代码

```python
# server/app/auth/service.py:88-112
def decode(self, token):
    claims = jwt.decode(
        token,
        self._signing_key,
        algorithms=["HS256"],
        audience="studyflow-client",
        issuer="studyflow-api",
        options={"require": [...], "verify_exp": False, "verify_iat": False},
    )
    if claims["type"] != "access":
        raise ValueError("wrong token type")
    # 手动检查 iat/exp（因为上面 verify 被关了，配合注入时钟）
    ...
    return UserContext(user_id=UUID(claims["sub"]), email=claims["email"])
```

---

## 8. 常见错误

| 错误理解 | 为什么不对 | 正确理解 |
|---|---|---|
| "token 是加密的，别人读不了" | 三段全是 base64url 编码，谁都能解码读 header/payload | 前两段公开可读，只有签名段是防篡改指纹 |
| "签名是用 payload 算的" | 签名输入是 header 编码 + "." + payload 编码，header 也必须被覆盖 | 签名 = HMAC(key, H + "." + P)，防止算法混淆攻击 |
| "签名会参与自己的计算" | 签名是最后拼进第三段的，不递归 | 先算签名，再拼 token |
| "签名就是加密" | 加密可逆、藏内容；签名不可逆、只做校验 | 签名 = 指纹，不是加密 |
| "token_signing_key 是盐" | 盐公开不保密；签名密钥必须保密 | 盐=打散器，密钥=印章 |
| "HS256 是唯一的签名算法" | JWT 还支持 RS256/ES256 等非对称算法 | 本项目用 HS256（对称，一个密钥签+验） |

---

## 9. 速查表

| 问题 | 答案 |
|---|---|
| JWT 是什么 | 盖章的无状态通行证，验证信息全在令牌里 |
| 三段结构 | `header.payload.签名`，全部 base64url |
| header 里有什么 | `{"alg":"HS256","typ":"JWT"}` |
| 签名公式 | `HMAC-SHA256(key, header编码.payload编码)` |
| 签名输入为什么含 header | 防算法混淆攻击（alg=none 绕过验证） |
| HMAC 是什么 | RFC 2104 标准，两次哈希，Python `hmac` 标准库 |
| 编码 vs 加密 vs 混淆 vs 签名 | 换形式 / 藏内容 / 装难看 / 指纹 |
| 盐 vs 签名密钥 | 公开打散器 vs 机密印章 |
| 签发 4 步 | 组装 H → 组装 P → HMAC 算 S → 拼 token |
| 验证 4 步 | 解码 P 读身份 → 重算 S' → 比对 → 检查 exp/iat/type |
| 密钥泄漏后果 | 可伪造任意令牌；换 key → 所有旧令牌作废 |

---

## ✅ 检查点

- [ ] 能用自己的话解释：为什么 JWT 是"无状态"认证？
- [ ] 能说出 token 三段分别是什么、哪段是编码、哪段是指纹？
- [ ] 知道签名为什么必须覆盖 header（算法混淆攻击）？
- [ ] 能区分编码/加密/混淆/签名四个词？
- [ ] 知道盐和 token_signing_key 的区别，以及项目里盐在哪？
- [ ] 打开 `server/app/auth/service.py` 能定位 `issue`（签发）和 `decode`（验证）？
