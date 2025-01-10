## 本地部署说明
以下部署以ubuntu server 24.04 LTS为例
#### 1. 准备环境  
    确保你的本地机器已经安装了以下工具：

    · Node.js 18（用于构建前端）

    · Python 3.10（用于运行后端）

    · pnpm（用于构建后台管理系统）

    · Nginx（用于服务前端静态文件）

    · Git（用于克隆项目）

#### 2. 克隆项目  
将项目代码克隆到本地：  
```
git clone https://github.com/DemoJ/ThinNav.git
cd ThinNav
```

#### 3. 构建用户端 Vue 项目  
第一步，构建用户端 Vue 项目：

进入用户端项目目录：
```
cd frontend/navigation
```
安装依赖并构建：
```
npm install
npm run build
```
构建完成后，生成的静态文件会放在 dist 目录中。将 dist 目录复制到一个统一的静态文件目录（例如 /var/www/html/user）：
```
sudo mkdir -p /var/www/html/user
sudo cp -r dist/* /var/www/html/user/
```
#### 4. 构建后台管理系统 Vue 项目  
返回项目目录
```
cd ../..
```
进入后台管理系统项目目录：
```
cd frontend/nav-admin
```
安装依赖并构建：
```
pnpm install --frozen-lockfile
pnpm build
```
构建完成后，生成的静态文件会放在 dist 目录中。将 dist 目录复制到一个统一的静态文件目录（例如 /var/www/html/admin）：
```
sudo mkdir -p /var/www/html/admin
sudo cp -r dist/* /var/www/html/admin/
```
#### 5. 配置 Nginx  
修改 Nginx 默认配置文件
```
sudo vim /etc/nginx/sites-available/default
```
将原始内容全部删掉，然后复制以下内容写入
```
server {
    listen 80;
    server_name _;

    # 用户端
    location / {
        root /var/www/html/user;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 管理后台
    location /admin {
        alias /var/www/html/admin/;
        index index.html;
        try_files $uri $uri/ /admin/index.html;
    }
    # 静态文件
    location /icons/ {
        proxy_pass http://127.0.0.1:8000/icons/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }


    # 后端api
    location /api/ {
        # 移除 /api 前缀
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8000;
        # 设置一些基本的代理头
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```  

测试 Nginx 配置并重启服务：
```
sudo nginx -t
sudo systemctl restart nginx
```
访问前端项目：

用户端：http://{该机器ip地址}

后台管理系统：http://{该机器ip地址}/admin

#### 6. 部署 FastAPI 后端
返回项目目录
```
cd ../..
```
进入后端项目目录：
```
cd backend
```
创建并激活 Python 虚拟环境：
```
sudo apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
```
提前安装编译所需依赖
```
sudo apt install python3-dev zlib1g-dev libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev
```
安装python依赖：
```
pip install -r requirements.txt
```
创建数据库
```
python init_db.py
```
运行 FastAPI 应用：
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
访问 FastAPI 后端
API 文档：http://{该机器ip地址}:8000/docs  
确认没问题后，ctrl+c关掉  

*如果你在本机部署并希望长期使用 FastAPI 后端服务，推荐将 uvicorn 配置为系统服务。这样可以确保服务在后台运行，支持开机自启动，并且方便管理和监控。*