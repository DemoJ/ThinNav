from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.database import get_db
from app.models import Admin

SECRET_KEY = "-84iFQMj5Hd_PV2v2tkDKdPG5hpFTsi_wEtyp8h7-fs"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def create_tokens(data: dict, expires_delta: timedelta = None, refresh_expires_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
<<<<<<< HEAD
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
=======
        expire = datetime.now() + timedelta(minutes=15)
>>>>>>> d227d92b60f057fd21b65d54200f7ee98b1e441b
    to_encode.update({"exp": expire})
    accessToken = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Create refresh token
    refresh_expire = datetime.now(timezone.utc) + refresh_expires_delta
    refreshToken = jwt.encode({"exp": refresh_expire, "sub": data["sub"]}, SECRET_KEY, algorithm=ALGORITHM)

    return accessToken, refreshToken

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        result = await db.execute(select(Admin).where(Admin.username == username))
        admin = result.scalars().first()
        if admin is None or admin.refreshToken != refreshToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        new_access_token, new_refresh_token = create_tokens({"sub": username})  # 确保这个函数定义正确
        return {"accessToken": new_access_token, "refreshToken": new_refresh_token}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )