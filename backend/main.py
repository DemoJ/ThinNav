import uvicorn
from fastapi import FastAPI
from sqlalchemy.future import select
from app import models
from app.models import Admin
from app import categories, websites, admin, upload
from app.database import engine, AsyncSessionLocal
from fastapi.staticfiles import StaticFiles
import os
from alembic import command
from alembic.config import Config

app = FastAPI()

# 确保目录存在
UPLOAD_FOLDER = "./icons"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 挂载静态文件夹
app.mount("/icons", StaticFiles(directory="./icons"), name="icons")

app.include_router(categories.router, tags=["分类接口"], prefix="/categories")
app.include_router(websites.router, tags=["网址接口"], prefix="/websites")
app.include_router(admin.router, tags=["管理员接口"], prefix="/admin")
app.include_router(upload.router, tags=["图标管理"])

# 定义启动事件处理函数
async def startup_event():
    try:
        print("应用正在启动...")  # 添加调试输出
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

        # 数据库迁移应该放在启动前的步骤，避免阻塞事件循环
        print("数据库初始化完成")
    except Exception as e:
        print(f"启动事件处理失败: {e}")

# 定义关闭事件处理函数
async def shutdown_event():
    pass

# 注册生命周期事件处理函数
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# 数据库迁移可以通过命令手动运行，避免放在异步的上下文中
def run_db_migration():
    try:
        # 执行 Alembic 数据库迁移
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("数据库迁移完成")

    except Exception as e:
        print(f"数据库迁移失败: {e}")

if __name__ == "__main__":
    # 启动前运行数据库迁移，避免放入异步上下文中阻塞
    run_db_migration()

    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=["./backend"]
    )
