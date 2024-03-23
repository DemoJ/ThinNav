# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///backend/db/data.db"  # 注意使用aiosqlite
Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# 定义Category模型
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    icon_url = Column(String)
    order = Column(Integer, index=True)

# 定义Website模型
class Website(Base):
    __tablename__ = 'websites'
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    name = Column(String, index=True)
    icon_url = Column(String)
    description = Column(String)
    order = Column(Integer, index=True)
    url = Column(String, nullable=False)
    category = relationship("Category", back_populates="websites")

Category.websites = relationship("Website", order_by=Website.order, back_populates="category")
