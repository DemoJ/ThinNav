from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models,schemas
from app.models import AsyncSessionLocal
from typing import List,AsyncGenerator

router = APIRouter()

# 异步依赖项，用于获取数据库session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=schemas.Website)
async def create_website(website: schemas.WebsiteCreate, db: AsyncSession = Depends(get_db)):
    db_website = models.Website(**website.model_dump())
    db.add(db_website)
    await db.commit()
    await db.refresh(db_website)
    return db_website

@router.get("/", response_model=List[schemas.Website])
async def read_websites(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Website))
    websites = result.scalars().all()
    return websites

@router.put("/{website_id}", response_model=schemas.Website)
async def update_website(website_id: int, website: schemas.WebsiteCreate, db: AsyncSession = Depends(get_db)):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    for key, value in website.model_dump(exclude_unset=True).items():
        setattr(db_website, key, value)
    await db.commit()
    await db.refresh(db_website)
    return db_website

@router.delete("/{website_id}", status_code=204)
async def delete_website(website_id: int, db: AsyncSession = Depends(get_db)):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    await db.delete(db_website)
    await db.commit()
    return {"ok": True}
