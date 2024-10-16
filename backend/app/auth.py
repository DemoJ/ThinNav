from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .database import get_db
from .models import Admin
import secrets
import string
import os
from dotenv import load_dotenv, set_key


def generate_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_or_create_secret_key():
    # 获取当前脚本所在的目录
    env_path = os.path.join(".", ".env")

    # 如果 .env 文件存在，尝试读取 SECRET_KEY
    if os.path.exists(env_path):
        load_dotenv(env_path)
        secret_key = os.getenv("JWT_SECRET_KEY")

        if secret_key:
            print("从现有 .env 文件中读取 SECRET_KEY")
            return secret_key

    # 如果 .env 不存在或没有 SECRET_KEY，生成新的
    new_secret_key = generate_secret_key()

    # 创建或更新 .env 文件
    set_key(env_path, "JWT_SECRET_KEY", new_secret_key)

    print(f"新的 SECRET_KEY 已生成并保存到 {env_path}")
    return new_secret_key


SECRET_KEY = get_or_create_secret_key()
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/token")


def create_tokens(
    data: dict,
    expires_delta: timedelta = None,
    refresh_expires_delta: timedelta = timedelta(days=1),
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    accessToken = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Create refresh token
    refresh_expire = datetime.now(timezone.utc) + refresh_expires_delta
    refreshToken = jwt.encode(
        {"exp": refresh_expire, "sub": data["sub"]}, SECRET_KEY, algorithm=ALGORITHM
    )

    return accessToken, refreshToken


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    print(f"Received token: {token}")  # 添加这行来检查 token 的值
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        result = await db.execute(select(Admin).where(Admin.username == username))
        admin = result.scalars().first()
        if admin is None:
            raise credentials_exception
        return admin
    except JWTError:
        raise credentials_exception


async def refresh_token(refreshToken: str, db: AsyncSession = Depends(get_db)):
    print(f"Received refreshToken: {refreshToken}")  # 添加这行来检查 refreshToken 的值
    try:
        payload = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token:Username is None",
                headers={"WWW-Authenticate": "Bearer"},
            )
        result = await db.execute(select(Admin).where(Admin.username == username))
        admin = result.scalars().first()
        if admin is None or admin.refreshToken != refreshToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 生成新的 accessToken 和 refreshToken
        new_access_token, new_refresh_token = create_tokens({"sub": username})

        # 更新数据库中的 refreshToken
        admin.refreshToken = new_refresh_token
        await db.commit()
        print(f"Update refreshToken successful.  RefreshToken: {new_refresh_token}")
        return {"accessToken": new_access_token, "refreshToken": new_refresh_token}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
