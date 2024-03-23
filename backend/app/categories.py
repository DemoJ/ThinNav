from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app import schemas
from app.models import AsyncSessionLocal
from typing import List,AsyncGenerator

categories=APIRouter()

# 异步依赖项，用于获取数据库session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@categories.post("/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@categories.get("/", response_model=List[schemas.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category))
    categories = result.scalars().all()
    return categories