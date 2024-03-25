# main.py
import uvicorn
from fastapi import FastAPI
from app import models
from app.models import engine
from app import categories,websites


app = FastAPI()

app.include_router(categories.router, tags=["分类接口"], prefix="/categories")
app.include_router(websites.router, tags=["网址接口"], prefix="/websites")

# 定义启动事件处理函数
async def startup_event():
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# 定义关闭事件处理函数
async def shutdown_event():
    # 这里可以放置关闭时需要执行的代码
    pass


# 注册生命周期事件处理函数
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
