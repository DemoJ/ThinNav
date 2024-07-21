from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Admin
from app.schemas import ChangePasswordRequest
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from app.auth import create_tokens, get_current_user, refresh_token
from datetime import timedelta,datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/token")

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

    accessToken= create_tokens(
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

    add_expires = timedelta(minutes=1)

    # 将当前时间加上一分钟
    minute_later = current_time + add_expires

    # 转换为时间戳
    accessToken_expires = int(minute_later.timestamp()* 1000)

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
            "expires": accessToken_expires
        },
    }


@router.post("/refresh-token")
async def refresh_access_token(refreshToken: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        print(refreshToken)
        token_data = await refresh_token(refreshToken, db)
        return {
            "success": 1,
            "data": {
                "accessToken": token_data['accessToken'],
                "refreshToken": token_data['refreshToken'],
                "token_type": "bearer"
            }
        }
    except HTTPException as e:
        raise e


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
