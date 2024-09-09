import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator

# 数据库URL，适用于异步数据库引擎
# 对于SQLite异步使用示例: DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# 对于PostgreSQL异步使用示例: DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# 数据库文件路径
DATABASE_URL = "sqlite+aiosqlite:///db/data.db"

# 判断文件是否存在，不存在则创建
if not os.path.exists('db'):
    os.makedirs('db')

if not os.path.exists('db/data.db'):
    with open('db/data.db', 'w') as f:
        f.write('')

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建异步会话工厂
# expire_on_commit=False 是在异步使用时的推荐设置
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

# 基础的声明式基类
Base = declarative_base()

# 异步依赖项，用于获取数据库session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
