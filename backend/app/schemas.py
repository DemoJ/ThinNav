# schemas.py
from pydantic import BaseModel
from typing import Optional

# 基础Category模型
class CategoryBase(BaseModel):
    name: str
    icon_url: Optional[str] = None
    order: int

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# 基础Website模型
class WebsiteBase(BaseModel):
    name: str
    icon_url: Optional[str] = None
    description: Optional[str] = None
    order: int
    url: str
    category_id: int

class WebsiteCreate(WebsiteBase):
    pass

class Website(WebsiteBase):
    id: int
    class Config:
        orm_mode = True