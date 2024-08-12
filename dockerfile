# 第一步：构建 FastAPI 后端
FROM python:3.10-slim as backend-build

WORKDIR /app

# 复制后端代码并安装依赖
COPY backend/requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# 第二步：构建用户端 Vue 项目
FROM node:18-alpine as frontend-user-build

WORKDIR /app

COPY frontend/navigation/package*.json ./
RUN npm install
COPY frontend/navigation/ .
RUN npm run build

# 第三步：构建后台管理系统 Vue 项目
FROM node:18-alpine as frontend-admin-build

WORKDIR /app
RUN corepack enable
RUN corepack prepare pnpm@8.6.10 --activate

COPY frontend/nav-admin/package.json frontend/nav-admin/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/nav-admin/ .
RUN pnpm build

# 第四步：构建最终的 Nginx 镜像
FROM nginx:stable-alpine

# 复制前端构建的文件
COPY --from=frontend-user-build /app/dist /usr/share/nginx/html/user
COPY --from=frontend-admin-build /app/dist /usr/share/nginx/html/admin

# 复制并配置 FastAPI 应用
COPY --from=backend-build /app /app
COPY docker/web-prod.conf /etc/nginx/conf.d/default.conf

# 安装必要的依赖
RUN apk add --no-cache gcc musl-dev libffi-dev

# 确保虚拟环境的 pip 可以被找到
ENV PATH="/opt/venv/bin:$PATH"

# 安装 uvicorn
RUN pip install uvicorn

# 启动 FastAPI 应用和 Nginx 服务
CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
