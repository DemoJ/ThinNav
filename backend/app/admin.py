from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Admin
from app.schemas import ChangePasswordRequest
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, get_current_user
from datetime import timedelta

router = APIRouter()


@router.post("/login")
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
    accessToken_expires = timedelta(minutes=15)
    accessToken = create_access_token(
        data={"sub": admin.username}, expires_delta=accessToken_expires
    )
    return {"success": 1, "data": {"accessToken": accessToken, "token_type": "bearer"}}

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
