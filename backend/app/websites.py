from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .database import get_db
from .auth import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Website)
async def create_website(
    website: schemas.WebsiteCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_website = models.Website(**website.model_dump())
    db.add(db_website)
    await db.commit()
    await db.refresh(db_website)

    # 获取关联的 category_name
    category_name = (
        await db.execute(
            select(models.Category.name).where(
                models.Category.id == db_website.category_id
            )
        )
    ).scalar()

    return schemas.Website(
        id=db_website.id,
        name=db_website.name,
        icon_url=db_website.icon_url,
        description=db_website.description,
        order=db_website.order,
        url=db_website.url,
        category_id=db_website.category_id,
        category_name=category_name,
    )


@router.get("/", response_model=schemas.PaginatedWebsites)
async def read_websites(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, description="Number of records to skip", ge=0),
    limit: int = Query(10, description="Maximum number of records to return", ge=1)
):
    # 获取总记录数
    total = await db.scalar(select(func.count()).select_from(models.Website))

    # 获取分页数据，按照 order 字段排序
    stmt = (
        select(models.Website, models.Category.name.label("category_name"))
        .join(models.Category, models.Website.category_id == models.Category.id, isouter=True)
        .order_by(models.Website.order)  # 按 order 字段排序
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    websites = result.all()

    # 处理结果
    response_data = [
        schemas.Website(
            id=website.id,
            name=website.name,
            icon_url=website.icon_url,
            description=website.description,
            order=website.order,
            url=website.url,
            category_id=website.category_id,
            category_name=category_name,
        )
        for website, category_name in websites
    ]

    # 返回分页数据和总记录数
    return schemas.PaginatedWebsites(data=response_data, total=total)


@router.put("/{website_id}", response_model=schemas.Website)
async def update_website(
    website_id: int,
    website: schemas.WebsiteCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")

    for key, value in website.model_dump(exclude_unset=True).items():
        setattr(db_website, key, value)
    await db.commit()
    await db.refresh(db_website)

    # 获取关联的 category_name
    category_name = (
        await db.execute(
            select(models.Category.name).where(
                models.Category.id == db_website.category_id
            )
        )
    ).scalar()

    return schemas.Website(
        id=db_website.id,
        name=db_website.name,
        icon_url=db_website.icon_url,
        description=db_website.description,
        order=db_website.order,
        url=db_website.url,
        category_id=db_website.category_id,
        category_name=category_name,
    )


@router.delete("/{website_id}", status_code=204)
async def delete_website(
    website_id: int,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    await db.delete(db_website)
    await db.commit()
    return {"ok": True}
