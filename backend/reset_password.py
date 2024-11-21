import asyncio
from sqlalchemy.future import select
from app.database import AsyncSessionLocal
from app.models import Admin
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def reset_admin_password():
    try:
        async with AsyncSessionLocal() as session:
            # 查找admin用户
            result = await session.execute(select(Admin).filter(Admin.username == "admin"))
            admin = result.scalar_one_or_none()
            
            if admin is None:
                logger.error("未找到admin用户")
                return
            
            # 重置密码为123456
            admin.set_password("123456")
            await session.commit()
            logger.info("密码重置成功！新密码为: 123456")
            
    except Exception as e:
        logger.error(f"重置密码时发生错误: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(reset_admin_password())
