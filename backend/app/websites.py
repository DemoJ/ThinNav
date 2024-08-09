from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models,schemas
from typing import List
from .database import get_db
from .auth import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Website)
async def create_website(website: schemas.WebsiteCreate, current_user:models.Admin = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    db_website = models.Website(**website.model_dump())
    db.add(db_website)
    await db.commit()
    await db.refresh(db_website)
    return db_website

@router.get("/", response_model=List[schemas.Website])
async def read_websites(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(models.Website, models.Category.name.label('category_name'))
        .join(models.Category, models.Website.category_id == models.Category.id)
    )
    result = await db.execute(stmt)
    websites = result.all()
    # Process the result to match your response model
    response = []
    for website, category_name in websites:
        response.append(schemas.Website(
            id=website.id,
            name=website.name,
            icon_url=website.icon_url,
            description=website.description,
            order=website.order,
            url=website.url,
            category_id=website.category_id,
            category_name=category_name
        ))
    return response

@router.put("/{website_id}", response_model=schemas.Website)
async def update_website(website_id: int, website: schemas.WebsiteCreate, current_user:models.Admin = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    for key, value in website.model_dump(exclude_unset=True).items():
        setattr(db_website, key, value)
    await db.commit()
    await db.refresh(db_website)
    return db_website

@router.delete("/{website_id}", status_code=204)
async def delete_website(website_id: int, current_user:models.Admin = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    await db.delete(db_website)
    await db.commit()
    return {"ok": True}
