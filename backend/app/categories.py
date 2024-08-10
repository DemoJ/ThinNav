from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .database import get_db
from .auth import get_current_user
from typing import List

router = APIRouter()


@router.post("/", response_model=schemas.Category)
async def create_category(
    category: schemas.CategoryCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[schemas.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category).order_by(models.Category.order))
    categories = result.scalars().all()
    return categories


@router.put("/{category_id}", response_model=schemas.Category)
async def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_category = await session.get(models.Category, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        for var, value in vars(category).items():
            setattr(db_category, var, value) if value else None
        await session.commit()
        await session.refresh(db_category)
        return db_category


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        # 获取分类信息
        db_category = await session.get(models.Category, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")

        # 查询是否存在属于该分类的网址
        result = await session.execute(
            select(models.Website).filter_by(category_id=category_id)
        )
        websites = result.scalars().all()

        if websites:
            # 如果存在网址，则返回提示信息
            raise HTTPException(
                status_code=400,
                detail="Cannot delete category because it has associated websites. Please remove the websites first.",
            )

        # 删除分类
        await session.delete(db_category)
        await session.commit()

        return
