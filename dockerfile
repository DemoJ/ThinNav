# 第一步：构建用户端 Vue 项目
FROM node:18-alpine as frontend-user-build

WORKDIR /app

COPY frontend/navigation/package*.json ./
RUN npm install
COPY frontend/navigation/ .
RUN npm run build

# 第二步：构建后台管理系统 Vue 项目
FROM node:18-alpine as frontend-admin-build

WORKDIR /app
RUN corepack enable
RUN corepack prepare pnpm@8.6.10 --activate

COPY frontend/nav-admin/package.json frontend/nav-admin/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/nav-admin/ .
RUN pnpm build

# 第三步：构建最终的 Python + Nginx 镜像
FROM python:3.10-slim

# 安装 Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制前端构建的文件
COPY --from=frontend-user-build /app/dist /usr/share/nginx/html/user
COPY --from=frontend-admin-build /app/dist /usr/share/nginx/html/admin

# 复制并安装 FastAPI 应用及其依赖
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
RUN touch /app/.env

# 复制 Alembic 配置和迁移脚本
COPY alembic.ini .
COPY migrations/ ./migrations/

# 复制并配置 Nginx
COPY docker/web-prod.conf /etc/nginx/conf.d/default.conf

# 启动 Alembic 迁移，并在之后启动 FastAPI 应用和 Nginx 服务
CMD uvicorn main:app --host 0.0.0.0 --port 8000 && alembic upgrade head & nginx -g "daemon off;"
