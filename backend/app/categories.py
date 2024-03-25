from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models,schemas
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

@categories.put("/{category_id}", response_model=schemas.Category)
async def update_category(category_id: int, category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_category = await session.get(models.Category, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        for var, value in vars(category).items():
            setattr(db_category, var, value) if value else None
        await session.commit()
        await session.refresh(db_category)
        return db_category

@categories.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_category = await session.get(models.Category, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        await session.delete(db_category)
        await session.commit()
        return {"ok": True}