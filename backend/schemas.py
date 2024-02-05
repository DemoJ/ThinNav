# schemas.py
from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    icon_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
