import uvicorn
from fastapi import FastAPI
from sqlalchemy.future import select
from app import models
from app.models import Admin
from app import categories, websites, admin, upload
from app.database import engine, AsyncSessionLocal
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from alembic import command
from alembic.config import Config

app = FastAPI()

# 确保目录存在
UPLOAD_FOLDER = "./icons"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 挂载静态文件夹
app.mount("/icons", StaticFiles(directory="./icons"), name="icons")

# 包含路由
app.include_router(categories.router, tags=["分类接口"], prefix="/categories")
app.include_router(websites.router, tags=["网址接口"], prefix="/websites")
app.include_router(admin.router, tags=["管理员接口"], prefix="/admin")
app.include_router(upload.router, tags=["图标管理"])


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def create_default_admin():
    async with AsyncSessionLocal() as session:
        admin_count = await session.execute(select(Admin).limit(1))
        admin_count = admin_count.scalars().first()
        if not admin_count:
            default_admin = Admin(username="admin")
            default_admin.set_password("123456")
            session.add(default_admin)
            await session.commit()


def run_alembic_upgrade():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


async def startup_event():
    await create_tables()
    await create_default_admin()

    # 在单独的线程中运行 Alembic 升级
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run_alembic_upgrade)


# 定义关闭事件处理函数
async def shutdown_event():
    # 这里可以放置关闭时需要执行的代码
    pass


# 注册生命周期事件处理函数
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=["./backend"]
    )
