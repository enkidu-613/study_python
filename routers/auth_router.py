"""
/auth 路由 —— JWT 用户认证与授权
├── POST /auth/register    注册（查重 → bcrypt 哈希 → 存库 → 发 Token）
├── POST /auth/login       登录（查库 → 比密码 → 发 Token）
├── POST /auth/logout      登出（Token 加入黑名单）
├── GET  /auth/me          查看当前用户身份
└── 依赖: get_current_user（验票机）, require_role（角色守卫）
"""
import os
import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, RevokedToken

# ========== 配置 ==========
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_HOURS = 2  # Access Token 有效期

if not JWT_SECRET:
    raise ValueError("❌ JWT_SECRET 环境变量未设置，服务器拒绝启动！")

router = APIRouter(prefix="/auth", tags=["认证"])
security = HTTPBearer()


# ========== Pydantic 请求体 ==========
class RegisterDto(BaseModel):
    username: str
    password: str


class LoginDto(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str


# ========== 工具函数 ==========
def create_token(user_id: int, username: str, role: str) -> str:
    """签发 JWT 门票"""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRES_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def _hash_token(token: str) -> str:
    """对 Token 做 SHA256，黑名单里不存完整 Token"""
    return hashlib.sha256(token.encode()).hexdigest()


# ========== 依赖：验票机 ==========
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """FastAPI 自动验票：提取 Bearer → 查黑名单 → 验签 → 返回用户信息"""
    token = credentials.credentials

    # ① 查黑名单（挂失的票直接拦）
    token_hash = _hash_token(token)
    if db.query(RevokedToken).filter(RevokedToken.token_hash == token_hash).first():
        raise HTTPException(status_code=401, detail="Token 已被撤销，请重新登录")

    # ② 验签
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="门票已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的门票")

    return {
        "id": int(payload["sub"]),
        "username": payload["username"],
        "role": payload["role"],
    }


# ========== 依赖工厂：角色守卫 ==========
def require_role(*allowed_roles: str):
    """
    角色守卫工厂 —— 用法:
        @app.get("/admin")
        def admin(user: dict = require_role("ADMIN")):
            ...
    """
    def checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"权限不足，需要角色: {allowed_roles}")
        return user
    return Depends(checker)


# ========== 注册 ==========
@router.post("/register", response_model=TokenResponse)
def register(dto: RegisterDto, db: Session = Depends(get_db)):
    """注册：查重 → 密码绞肉 → 存库 → 发 Token"""
    # ① 查重
    if db.query(User).filter(User.username == dto.username).first():
        raise HTTPException(status_code=400, detail="用户名已被注册")

    # ② 密码哈希（绞肉机）
    hashed = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt(rounds=10))

    # ③ 入库
    user = User(username=dto.username, password=hashed.decode(), role="USER")
    db.add(user)
    db.commit()
    db.refresh(user)

    # ④ 发门票
    token = create_token(user.id, user.username, user.role)
    return TokenResponse(access_token=token, username=user.username, role=user.role)


# ========== 登录 ==========
@router.post("/login", response_model=TokenResponse)
def login(dto: LoginDto, db: Session = Depends(get_db)):
    """登录：查库 → 比密码 → 发 Token"""
    # ① 查档案
    user = db.query(User).filter(User.username == dto.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="账号或密码错误")

    # ② 对暗号
    if not bcrypt.checkpw(dto.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="账号或密码错误")

    # ③ 发门票
    token = create_token(user.id, user.username, user.role)
    return TokenResponse(access_token=token, username=user.username, role=user.role)


# ========== 登出 ==========
@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """登出：Token 加入黑名单（挂失）"""
    token = credentials.credentials
    token_hash = _hash_token(token)

    # 解析过期时间放进黑名单，方便定时清理
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                             options={"verify_exp": False})  # 过期也允许挂失
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    except jwt.InvalidTokenError:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRES_HOURS)

    # 避免重复挂失
    if not db.query(RevokedToken).filter(RevokedToken.token_hash == token_hash).first():
        revoked = RevokedToken(token_hash=token_hash, expires_at=expires_at)
        db.add(revoked)
        db.commit()

    return {"message": "已退出登录，Token 已失效"}


# ========== 查看身份 ==========
@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    """查看当前用户身份（需要认证）"""
    return {"id": user["id"], "username": user["username"], "role": user["role"]}


# ========== 受保护示例 ==========
@router.get("/admin")
def admin_only(user: dict = require_role("ADMIN")):
    """只有 ADMIN 能进（演示角色守卫）"""
    return {"message": f"欢迎管理员 {user['username']}", "stats": "这是机密数据"}
