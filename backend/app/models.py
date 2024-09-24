# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship,declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

# 基础的声明式基类
Base = declarative_base()

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
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # 添加更新时间字段
    category = relationship("Category", back_populates="websites")

Category.websites = relationship("Website", order_by=Website.order, back_populates="category")

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    refreshToken = Column(String, nullable=True)  # 添加 refresh_token 字段

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
