import uvicorn
from fastapi import FastAPI
from sqlalchemy.future import select
from app.models import Admin
from app import categories, websites, admin, upload, models
from app.database import engine, AsyncSessionLocal
from fastapi.staticfiles import StaticFiles
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI()

# 确保上传目录存在
UPLOAD_FOLDER = "./icons"
try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        logger.info(f"创建上传文件夹: {UPLOAD_FOLDER}")
    else:
        logger.info(f"上传文件夹已存在: {UPLOAD_FOLDER}")
except Exception as e:
    logger.error(f"创建上传文件夹失败: {e}")
    raise

# 挂载静态文件夹
app.mount("/icons", StaticFiles(directory=UPLOAD_FOLDER), name="icons")
logger.info("挂载静态文件夹 /icons")

# 包含路由
try:
    app.include_router(categories.router, tags=["分类接口"], prefix="/categories")
    app.include_router(websites.router, tags=["网址接口"], prefix="/websites")
    app.include_router(admin.router, tags=["管理员接口"], prefix="/admin")
    app.include_router(upload.router, tags=["图标管理"], prefix="/upload")
    logger.info("成功包含所有路由")
except Exception as e:
    logger.error(f"包含路由时出错: {e}")
    raise


# 定义创建数据库及默认管理员的异步函数
async def create_default_admin():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Admin).limit(1))
            existing_admin = result.scalars().first()
            if not existing_admin:
                default_admin = Admin(username="admin")
                default_admin.set_password("123456")
                session.add(default_admin)
                await session.commit()
                logger.info("创建默认管理员: admin")
            else:
                logger.info("默认管理员已存在")
    except Exception as e:
        logger.error(f"创建默认管理员失败: {e}")
        raise


# 定义启动事件处理函数
async def startup_event():
    logger.info("应用启动中...")
    try:
        await create_default_admin()
        logger.info("应用启动完成")
    except Exception as e:
        logger.error(f"启动事件处理失败: {e}")
        raise


# 定义关闭事件处理函数
async def shutdown_event():
    logger.info("应用关闭中...")
    # 在这里添加关闭时需要执行的代码，例如释放资源
    logger.info("应用已关闭")


# 注册生命周期事件处理函数
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

if __name__ == "__main__":
    try:
        # 启动 Uvicorn 服务器
        logger.info("启动 Uvicorn 服务器...")
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            reload_dirs=["./backend"],
            log_level="info",
        )
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
