from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Admin
from .schemas import ChangePasswordRequest
from .database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .auth import create_tokens, get_current_user, refresh_token
from datetime import timedelta, datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/token")

# 定义请求体模型
class RefreshTokenRequest(BaseModel):
    refreshToken: str

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    admin = await db.execute(select(Admin).where(Admin.username == form_data.username))
    admin = admin.scalars().first()
    if not admin or not admin.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    add_expires = timedelta(minutes=1)

    accessToken = create_tokens(
        data={"sub": admin.username}, expires_delta=add_expires
    )[0]
    return {"access_token": accessToken, "token_type": "bearer"}


@router.post("/login")
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    admin = await db.execute(select(Admin).where(Admin.username == form_data.username))
    admin = admin.scalars().first()
    if not admin or not admin.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 获取当前时间
    current_time = datetime.now()

    add_expires = timedelta(minutes=30)

    # 将当前时间加上30分钟
    minute_later = current_time + add_expires

    # 转换为时间戳
    accessToken_expires = int(minute_later.timestamp() * 1000)

    accessToken, refreshToken = create_tokens(
        data={"sub": admin.username}, expires_delta=add_expires
    )
    # 更新数据库中的 refreshToken
    admin.refreshToken = refreshToken
    db.add(admin)
    await db.commit()
    print(f"Login successful. AccessToken: {accessToken}, RefreshToken: {refreshToken}")
    return {
        "success": 1,
        "data": {
            "username": admin.username,
            "roles": ["admin"],
            "accessToken": accessToken,
            "refreshToken": refreshToken,
            "expires": accessToken_expires,
        },
    }


@router.post("/refresh-token")
async def refresh_access_token(
    token_request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
):
    try:
        # 提取 refreshToken
        refresh_token_str = token_request.refreshToken
        print(f"refreshToken: {refresh_token_str}")
        # 验证 refresh_token 的合法性，并生成新的 token
        token_data = await refresh_token(refresh_token_str, db)

        # 获取当前时间
        current_time = datetime.now()

        # 设置 accessToken 的过期时间（30 分钟）
        add_expires = timedelta(minutes=30)
        accessToken_expires = int((current_time + add_expires).timestamp() * 1000)

        # 返回新的 accessToken 和可能更新的 refreshToken
        return {
            "success": 1,
            "data": {
                "accessToken": token_data["accessToken"],
                "refreshToken": token_data.get("refreshToken", refresh_token_str),  # 如果没有生成新 refreshToken，则使用旧的
                "expires": accessToken_expires,
            },
        }

    except HTTPException as e:
        # 捕获 HTTP 异常并抛出
        raise e
    except Exception as e:
        # 捕获其他异常并抛出 500 错误
        raise HTTPException(status_code=500, detail="Failed to refresh token") from e


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Admin = Depends(get_current_user),
):
    admin = current_user
    if not admin.check_password(request.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password"
        )
    admin.set_password(request.new_password)
    await db.commit()
    return {"message": "Password changed successfully"}
