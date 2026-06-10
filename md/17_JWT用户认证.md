# 17. JWT 用户认证

> **这不是用来"背"的安全手册，这是你放在桌面上的外挂菜单。**
> 忘了 JWT 怎么传？`Ctrl+F` 搜"Bearer"，看比喻，抄模板。

---

## 🎯 一句话理解

JWT 是一张**服务器盖章的数字身份卡**。服务器不用记你是谁，只看这张卡的印章对不对、过期了没。

---

## 📖 第一关：认证 vs 授权

### 一句话
- **认证**：查身份证（你是谁？）
- **授权**：看门禁权限（你能进哪间房？）

### 生活类比
想象你进一栋写字楼：
1. **前台查身份证** → 认证（Authentication）→ 没身份证？滚出去（401）
2. **闸机刷门禁卡** → 授权（Authorization）→ 身份证对了但只能去3楼，你按5楼？拒绝（403）

```
你 → [前台: 有身份证?] → [闸机: 能去5楼?] → 进办公室
      ↓ 没有               ↓ 不能
    401 Unauthorized     403 Forbidden
```

> **记住口诀**：401 是"没身份"，403 是"有身份但没权限"。

---

## 📖 第二关：密码绝不能存明文

### 一句话
哈希是**单向绞肉机**：密码进去，变成一团认不出的肉泥，而且倒不回去。

### 生活类比
你在家做一道"秘制酱料"：
- 把牛肉、辣椒、盐扔进绞肉机（哈希函数）
- 出来的是肉泥（哈希值）
- 给你这团肉泥，你能反推出用了多少克盐吗？**不可能。**
- 而且每次加盐量不同（Salt），同样的牛肉进去，出来的肉泥也不一样

### 代码示例
```python
import bcrypt

# ========== 注册时 ==========
# 用户输入: "myPassword123"
# 绞肉机开动，故意绞得慢（约100ms），让暴力破解成本高
hashed = bcrypt.hashpw(
    b"myPassword123",
    bcrypt.gensalt(rounds=10)  # rounds=10 是成本因子，每加1时间翻倍
)
# 存进数据库的:
# b'$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZIMs3xXcJ3...'

# ========== 登录时 ==========
# 用户又输入 "myPassword123"
is_valid = bcrypt.checkpw(
    b"myPassword123",
    hashed  # 从数据库取出来的那团肉泥
)
# True → 密码正确
# False → 密码错误
```

### ⚠️ 常见错误
| 错误 | 原因 | 正确做法 |
|------|------|----------|
| 存明文密码 | 数据库一泄露，全网账号沦陷 | 永远只存 `bcrypt.hashpw` 的结果 |
| 自己写加密算法 | 你写的密码学 = 裸奔 | 用 `bcrypt`、`argon2`、`scrypt`，别发明轮子 |
| 登录提示"密码错误"而不是"账号或密码错误" | 暴露账号存在性，方便撞库 | 统一提示"账号或密码错误" |

### 📋 速查表
```python
# 注册
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10))

# 登录
is_ok = bcrypt.checkpw(password.encode(), stored_hash.encode())
```

---

## 📖 第三关：JWT 是一张三段式防伪门票

### 一句话
JWT = `Header（票头）.Payload（票面信息）.Signature（防伪钢印）`

### 生活类比
想象一张演唱会门票：
- **票头**：印着"本场演出 + 验票方式"（Header: 算法声明）
- **票面**：印着"座位号 + 票价 + 有效日期"（Payload: 用户ID、角色、过期时间）
- **防伪钢印**：场馆用私章盖上去的，你撕了重贴一眼假（Signature: 服务器用 SECRET 签的名）

**关键**：票面信息（Payload）只是用 Base64 包装的，**任何人都能拆开看**，所以别在上面写银行卡密码。

### 代码示例
```python
import jwt
from datetime import datetime, timedelta, timezone

JWT_SECRET = "你的超级机密密钥"  # 从环境变量读！别硬编码！
JWT_ALGORITHM = "HS256"

# ========== 发门票（登录成功时）==========
def create_token(user_id: int, username: str, role: str):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),      # 座位号 = 用户ID
        "username": username,     # 购票人名字
        "role": role,             # VIP区还是普通区
        "iat": now,               # 什么时候印的票
        "exp": now + timedelta(hours=2)  # 两小时后失效
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# 结果: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJqb2huIiwicm9sZSI6IlVTRVIifQ.xxxxxx
#        ↑ Header                    ↑ Payload                              ↑ Signature
```

### ⚠️ 常见错误
| 错误 | 原因 | 正确做法 |
|------|------|----------|
| Payload 放敏感信息 | Base64 可解码，等于明码写信 | 只放用户ID、角色、过期时间 |
| JWT_SECRET 写死在代码里 | 源码泄露 = 全网 Token 可被伪造 | `os.getenv("JWT_SECRET")` |
| 不设 `exp` 过期时间 | Token 一旦发出，永不过期 | 永远加 `exp`，短则15分钟，长则7天 |

### 📋 速查表
```python
# 签发
token = jwt.encode(payload, SECRET, algorithm="HS256")

# 验证
try:
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    # 门票过期了
except jwt.InvalidTokenError:
    # 假票
```

---

## 📖 第四关：配置安全 —— 十二因子原则

### 一句话
**JWT_SECRET 是后端最敏感的配置**，绝不能写死在代码里。配置必须像"调料包"一样，代码是菜，配置是盐，不同环境（开发/测试/生产）加不同的量。

### 生活类比
你开了一家连锁餐厅：
- **代码** = 招牌菜的做法（菜谱是固定的，所有分店一样）
- **配置** = 每分店的地址、外卖平台密钥、后厨门密码（每家店不同）
- 你能把后厨密码印在菜谱上发给所有人吗？**不能。**

### 代码示例
```python
# app/core/config.py
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN_MINUTES = 60 * 24 * 7  # 7天

# 启动时强制检查：没配密钥直接崩溃，绝不带病运行
if not JWT_SECRET:
    raise ValueError("JWT_SECRET 环境变量未设置，服务器拒绝启动")
```

```bash
# .env 文件（本地开发用，绝不提交到 Git！）
JWT_SECRET=your-super-random-secret-key-at-least-32-characters-long
DATABASE_URL=sqlite:///./app.db
```

```gitignore
# .gitignore
.env
*.db
```

```bash
# .env.example（给新成员看的模板，只留字段名，不留真值）
JWT_SECRET=
DATABASE_URL=
```

### 🔍 逐步拆解
1. **代码与配置分离**：代码库里只有 `os.getenv`，没有真密钥。
2. **环境变量注入**：本地用 `.env`，生产用云服务商的秘钥管理（AWS Secrets Manager、阿里云 KMS）。
3. **.env 不加 Git**：一提交，密钥永久留在 Git 历史里，删都删不掉。
4. **启动时校验**：`if not JWT_SECRET: raise`，防止有人忘了配密钥，服务器用空字符串签名 Token（等于没锁门）。

### ⚠️ 常见错误
| 错误 | 后果 |
|------|------|
| JWT_SECRET 硬编码在代码里 | 源码泄露 = 全网 Token 可被伪造 |
| .env 提交到 Git | 密钥永久暴露在版本历史里 |
| 生产环境依赖 .env 文件 | 容器/服务器上文件权限一旦配错，密钥裸奔 |
| 用简单字符串如 "secret" | 暴力破解只需几分钟 |

---

## 📖 第五关：FastAPI 的自动验票机（Depends）

### 一句话
`Depends(get_current_user)` 就是**闸机自动验票机**：每个进接口的人必须先过这关，票不对直接拦下，你的业务代码完全不用管。

### 生活类比
你去健身房：
1. 刷卡进门（请求头带 `Authorization: Bearer <token>`）
2. 闸机自动读取卡号，查数据库确认没过期、没被挂失（`jwt.decode` + 黑名单检查）
3. 闸机把会员信息贴在身上（`request.user = payload`）
4. 教练（业务代码）直接看你身上的标签就知道你是谁

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()  # 自动从请求头提取 Bearer Token

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # 把票取出来
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {
            "id": int(payload["sub"]),
            "username": payload["username"],
            "role": payload["role"]
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="门票过期了")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="假票，滚")

# ========== 使用 ==========
@app.get("/vip-room")
async def enter_vip(user: dict = Depends(get_current_user)):
    # 能走到这里的，票已经验过了
    return {"message": f"欢迎 VIP {user['username']}"}
```

### 🔍 逐步拆解
1. 前端在请求头里放 `Authorization: Bearer eyJhbG...`
2. `HTTPBearer()` 自动把 `eyJhbG...` 提取出来
3. `jwt.decode` 用 SECRET 验证钢印对不对
4. 对的 → 返回用户信息，业务代码执行
5. 错的 → FastAPI 自动返回 401，业务代码**一行不用写**

### 📋 速查表
```python
# 保护任意路由
@app.get("/xxx")
def xxx(user: dict = Depends(get_current_user)):
    ...

# 角色检查
if user["role"] != "ADMIN":
    raise HTTPException(status_code=403, detail="权限不足")
```

---

## 📖 第六关：角色授权 —— VIP 能进，普通会员不能进

### 一句话
认证通过后，还要查"你能进哪间房"。这是**第二道闸机**。

### 代码示例
```python
from fastapi import Depends, HTTPException

# ========== 角色守卫工厂 ==========
def require_role(*allowed_roles: str):
    """用法: Depends(require_role("ADMIN", "EDITOR"))"""
    def checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="权限不足，你的卡进不了这扇门")
        return user
    return Depends(checker)

# ========== 使用 ==========
@app.delete("/articles/{id}")
async def delete_article(user: dict = require_role("ADMIN", "EDITOR")):
    # 能走到这里的，既是合法用户，角色也是 ADMIN 或 EDITOR
    return {"message": f"{user['username']} 删除了文章"}

@app.get("/admin/dashboard")
async def admin_dashboard(user: dict = require_role("ADMIN")):
    return {"stats": "只有管理员能看的数据"}
```

### 🔍 逐步拆解
1. `require_role("ADMIN")` 返回一个 `Depends(checker)`
2. FastAPI 先执行 `get_current_user` 验身份
3. 身份过了再验角色：`user["role"] in allowed_roles`
4. 角色不对 → 403，业务代码**一行不执行**

### 📋 速查表
```python
# 任意角色
def require_role(*roles): ...

# 仅管理员
Depends(require_role("ADMIN"))

# 多角色
Depends(require_role("ADMIN", "EDITOR"))
```

---

## 📖 第七关：注册 / 登录 / 登出完整流水线

### 生活类比
办健身卡全流程：

- **注册**：填表 → 前台查重（这人办过了吗？）→ 交钱（密码哈希存库）→ 发卡（签发 JWT）
- **登录**：报手机号 → 查档案 → 对暗号（比密码）→ 发卡（签发 JWT）
- **登出**：把卡剪了 → 前台在系统里标记"此卡作废"（Token 加入黑名单/删除）

```python
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/auth", tags=["认证"])

# ========== 注册 ==========
@router.post("/register")
def register(dto: RegisterDto, db: Session = Depends(get_db)):
    # 1. 查重：这人办过卡了吗？
    if db.query(User).filter(User.username == dto.username).first():
        raise HTTPException(status_code=400, detail="用户名已被注册")

    # 2. 密码绞肉机处理
    hashed = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt())

    # 3. 入库
    user = User(username=dto.username, password=hashed.decode(), role="USER")
    db.add(user)
    db.commit()
    db.refresh(user)

    # 4. 发门票
    token = create_token(user.id, user.username, user.role)
    return {"access_token": token, "token_type": "bearer"}

# ========== 登录 ==========
@router.post("/login")
def login(dto: LoginDto, db: Session = Depends(get_db)):
    # 1. 查档案
    user = db.query(User).filter(User.username == dto.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="账号或密码错误")

    # 2. 对暗号
    if not bcrypt.checkpw(dto.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="账号或密码错误")

    # 3. 发门票
    token = create_token(user.id, user.username, user.role)
    return {"access_token": token, "token_type": "bearer"}

# ========== 登出（需要认证）==========
@router.post("/logout")
async def logout(
    user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # 把这张卡加入"挂失名单"（黑名单）
    revoked = RevokedToken(token=token, expires_at=...)
    db.add(revoked)
    db.commit()

    return {"message": "退出成功，此 Token 已失效"}
```

### 数据库表设计（Token 黑名单）
```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, index=True)  # 加索引，查黑名单快
    revoked_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)  # 知道它什么时候自然过期，方便定时清理
```

> **为什么存 expires_at？** 因为黑名单会无限增长，你可以写个定时任务，只清理已经自然过期的 Token，释放空间。

---

## 📖 第八关：JWT 的两个致命缺陷与补丁

### 缺陷 1：门票发出后没法"挂失"

**问题**：JWT 是无状态的，服务器只验钢印和日期，不查档案。用户点了"退出登录"，Token 在过期前依然能刷开门。

**补丁：黑名单（Revoked Token）**
在数据库或 Redis 里开一个"挂失名单"，验票前先查名单。

```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # 先看挂失名单
    if db.query(RevokedToken).filter(RevokedToken.token == token).first():
        raise HTTPException(status_code=401, detail="Token 已被撤销")

    # 再正常验票
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    ...
```

> 这违背了 JWT "无状态" 的初衷，但换来了**可控的安全性**。Redis 比数据库更适合做黑名单（自带 TTL 自动过期）。

### 缺陷 2：门票有效期太长不安全，太短用户体验差

**补丁：长短 Token 双卡制**

| 卡类型 | 有效期 | 用途 | 服务器存不存 |
|--------|--------|------|-------------|
| **Access Token（门禁卡）** | 15分钟~2小时 | 刷 API | 不存（纯无状态） |
| **Refresh Token（换卡券）** | 7天~30天 | 换新的门禁卡 | 必须存（数据库/Redis） |

**流程**：
1. 登录 → 服务器同时给**门禁卡** + **换卡券**
2. 平时刷 API → 只带门禁卡，服务器秒验（无状态）
3. 门禁卡过期 → API 返回 401
4. 拿换卡券去 `/refresh` → 服务器查档案确认换卡券没过期、没被挂失 → 发新的门禁卡
5. 真正登出 → 把换卡券从数据库删除/加入黑名单

```
前端 ──Access Token──→ API（闸机秒过，无状态）
   ←──── 401 过期 ────
前端 ──Refresh Token──→ /refresh（前台查档案）
   ←── 新 Access Token ────
```

> 复杂度从"架构"转移到了"代码逻辑"，但这是目前业界平衡安全与性能的最佳实践。

---

## 📋 终极速查表

### 密码哈希
```python
# 注册
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10))

# 登录
bcrypt.checkpw(password.encode(), stored_hash.encode())  # True/False
```

### JWT 签发
```python
payload = {
    "sub": str(user_id),   # 用户ID
    "role": role,           # 角色
    "iat": datetime.now(timezone.utc),
    "exp": datetime.now(timezone.utc) + timedelta(hours=2)
}
token = jwt.encode(payload, SECRET, algorithm="HS256")
```

### JWT 验证 + 保护路由
```python
security = HTTPBearer()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    return jwt.decode(creds.credentials, SECRET, algorithms=["HS256"])

@app.get("/xxx")
def xxx(user=Depends(get_current_user)):
    ...
```

### 角色守卫
```python
def require_role(*roles):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return user
    return Depends(checker)

# 使用
@app.delete("/xxx")
def xxx(user=Depends(require_role("ADMIN"))):
    ...
```

### HTTP 请求头格式
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 环境变量配置
```python
import os
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET 未设置")
```

---

## ✅ 检查点

- [ ] 能用自己的话说出 401 和 403 的区别。
- [ ] 能解释为什么密码必须哈希，bcrypt 的 salt 是干嘛的。
- [ ] 能画出 JWT 三段结构，知道 Payload 能被任何人解码看。
- [ ] 能写出 `Depends(get_current_user)` 保护 FastAPI 路由的代码。
- [ ] 能写出 `require_role("ADMIN")` 角色守卫的代码。
- [ ] 理解 JWT "无状态"的好处和"无法撤销"的坏处。
- [ ] 知道长短 Token 里，为什么 Refresh Token 必须服务端存储。
- [ ] 知道 JWT_SECRET 为什么必须从环境变量读取，绝不能硬编码。
- [ ] 能描述登出时黑名单（RevokedToken）的工作流程。

---

## 🎮 常见陷阱表（贴在显示器上）

| 陷阱 | 后果 |
|------|------|
| JWT_SECRET 硬编码 | 源码泄露 = 全网 Token 可被伪造 |
| Payload 放密码/手机号 | Base64 可解码，信息裸奔 |
| 不设 Token 过期时间 | 一旦签发，永不过期 |
| 登录失败提示"密码错误" | 暴露账号存在性，方便撞库 |
| 只用 JWT 无黑名单实现登出 | 退出后 Token 依然可用 |
| .env 提交到 Git | 密钥永久留在版本历史里 |
| 生产环境依赖 .env 文件 | 文件权限配错 = 密钥裸奔 |

---

## 🗺️ 完整思维导图

```
用户认证
├── 密码安全
│   ├── 绝不存明文
│   ├── bcrypt: 单向哈希 + Salt
│   └── 登录提示模糊化（防撞库）
├── JWT 令牌
│   ├── Header: 算法声明
│   ├── Payload: 用户ID/角色/过期时间（Base64裸奔，不放密）
│   └── Signature: SECRET 防伪签名
├── 配置安全（十二因子）
│   ├── JWT_SECRET 走环境变量
│   ├── .env 不加 Git
│   └── 启动时强制校验
├── FastAPI 实现
│   ├── /register: 查重 → 哈希密码 → 存库 → 发 Token
│   ├── /login: 查库 → 比密码 → 发 Token
│   ├── /logout: Token 加入黑名单
│   ├── Depends(get_current_user): 提取 Bearer → 验签 → 注入 user
│   └── require_role: 在 user.role 上做权限检查
└── 进阶策略
    ├── Token 黑名单: 解决撤销问题（RevokedToken 表）
    ├── 长短 Token: Access(短/无状态) + Refresh(长/存库)
    └── 黑名单清理: 定时删除已过期的 revoked token
```
