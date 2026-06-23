"""
/auth 路由 —— JWT 用户认证与授权
├── POST /auth/register    注册
├── POST /auth/login       登录
├── POST /auth/logout      登出
├── GET  /auth/me          查看当前用户身份
└── 依赖: get_current_user, require_role
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

from app.database import get_db
from app.models import User, RevokedToken

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_HOURS = 2

if not JWT_SECRET:
    raise ValueError("❌ JWT_SECRET 环境变量未设置，服务器拒绝启动！")

router = APIRouter(prefix="/auth", tags=["认证"])
security = HTTPBearer()


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


def create_token(user_id: int, username: str, role: str) -> str:
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
    return hashlib.sha256(token.encode()).hexdigest()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    token = credentials.credentials

    token_hash = _hash_token(token)
    if db.query(RevokedToken).filter(RevokedToken.token_hash == token_hash).first():
        raise HTTPException(status_code=401, detail="Token 已被撤销，请重新登录")

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


def require_role(*allowed_roles: str):
    def checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"权限不足，需要角色: {allowed_roles}")
        return user
    return Depends(checker)


@router.post("/register", response_model=TokenResponse)
def register(dto: RegisterDto, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == dto.username).first():
        raise HTTPException(status_code=400, detail="用户名已被注册")

    hashed = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt(rounds=10))

    user = User(username=dto.username, password=hashed.decode(), role="USER")
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id, user.username, user.role)
    return TokenResponse(access_token=token, username=user.username, role=user.role)


@router.post("/login", response_model=TokenResponse)
def login(dto: LoginDto, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == dto.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="账号或密码错误")

    if not bcrypt.checkpw(dto.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="账号或密码错误")

    token = create_token(user.id, user.username, user.role)
    return TokenResponse(access_token=token, username=user.username, role=user.role)


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    token_hash = _hash_token(token)

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                             options={"verify_exp": False})
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    except jwt.InvalidTokenError:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRES_HOURS)

    if not db.query(RevokedToken).filter(RevokedToken.token_hash == token_hash).first():
        revoked = RevokedToken(token_hash=token_hash, expires_at=expires_at)
        db.add(revoked)
        db.commit()

    return {"message": "已退出登录，Token 已失效"}


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return {"id": user["id"], "username": user["username"], "role": user["role"]}


@router.get("/admin")
def admin_only(user: dict = require_role("ADMIN")):
    return {"message": f"欢迎管理员 {user['username']}", "stats": "这是机密数据"}
