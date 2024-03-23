# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .models import AsyncSessionLocal, engine
from typing import List,AsyncGenerator

app = FastAPI()

# 定义启动事件处理函数
async def startup_event():
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# 定义关闭事件处理函数
async def shutdown_event():
    # 这里可以放置关闭时需要执行的代码
    pass

# 注册生命周期事件处理函数
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# 异步依赖项，用于获取数据库session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[schemas.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category))
    categories = result.scalars().all()
    return categories
