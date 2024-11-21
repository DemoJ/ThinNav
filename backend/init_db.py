import asyncio
from sqlalchemy import select
from models import Admin, Base
from database import engine, AsyncSessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    try:
        # 创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # 创建默认管理员
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
        logger.error(f"数据库初始化失败: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db())
