# main.py
import uvicorn
from fastapi import FastAPI
from sqlalchemy.future import select
from app import models
from app.models import Admin
from app import categories,websites,admin
from app.database import engine,AsyncSessionLocal


app = FastAPI()

app.include_router(categories.router, tags=["分类接口"], prefix="/categories")
app.include_router(websites.router, tags=["网址接口"], prefix="/websites")
app.include_router(admin.router, tags=["管理员接口"], prefix="/admin")

# 定义启动事件处理函数
async def startup_event():
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        admin_count = await session.execute(select(Admin).limit(1))
        admin_count = admin_count.scalars().first()
        if not admin_count:
            default_admin = Admin(username="admin")
            default_admin.set_password("123456")
            session.add(default_admin)
            await session.commit()
# 定义关闭事件处理函数
async def shutdown_event():
    # 这里可以放置关闭时需要执行的代码
    pass


# 注册生命周期事件处理函数
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True,reload_dirs=["./backend"])
