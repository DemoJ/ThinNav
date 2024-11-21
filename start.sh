#!/bin/bash

# 检查 SQLite 数据库文件是否存在并初始化数据库
echo "Initializing database..."
python init_db.py

if [ $? -ne 0 ]; then
    echo "Database initialization failed!"
    exit 1
fi

# 执行数据库迁移
echo "Running database migrations..."
alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Migration failed!"
    exit 1
fi

# 启动应用服务器
echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 启动Nginx
echo "Starting Nginx..."
nginx -g "daemon off;"