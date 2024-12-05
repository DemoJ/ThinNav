import asyncio
from sqlalchemy import select, text
from app.models import Admin, Base
from app.database import engine, AsyncSessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alembic目标版本号
ALEMBIC_TARGET_VERSION = "4f57cda68ec2"

async def init_db():
    try:
        # 创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            # 检查或创建 alembic_version 表
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS alembic_version (
                    version_num VARCHAR(32) NOT NULL
                );
            """))
            # 检查 alembic_version 表中是否已经有版本号
            result = await conn.execute(text("SELECT version_num FROM alembic_version LIMIT 1;"))
            version = result.scalar()

            if version is None:
                # 设置初始 Alembic 版本号
                await conn.execute(text("INSERT INTO alembic_version (version_num) VALUES (:version);"), {"version": ALEMBIC_TARGET_VERSION})
                logger.info(f"已设置 Alembic 版本号为: {ALEMBIC_TARGET_VERSION}")
            else:
                logger.info(f"Alembic 版本号已存在: {version}")

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
