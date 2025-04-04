import os
import shutil
from pydantic import BaseModel
from fastapi import Depends, APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from .auth import get_current_user
from . import models
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

router = APIRouter()
UPLOAD_FOLDER = "./icons"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/token")
MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class URLRequest(BaseModel):
    url: str

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否在允许的格式中"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), current_user: models.Admin = Depends(get_current_user)
):
    # 检查文件扩展名
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed.",
        )

    # 检查文件大小
    file_size_mb = len(await file.read()) / (1024 * 1024)  # 文件大小以 MB 为单位
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit.",
        )

    # 重置文件指针
    file.file.seek(0)

    # 保存文件
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 返回图标的 URL（假设使用相对路径）
    icon_url = f"./icons/{file.filename}"

    return JSONResponse(content={"icon_url": icon_url})


@router.post("/get_icon/")
async def get_icon(request: URLRequest, current_user: models.Admin = Depends(get_current_user)):
    print(f"Request data: {request}")
    url = request.url
    try:
        # 添加日志记录调试信息
        print(f"Attempting to get icon from URL: {url}")
        
        # 确保URL不为空且是有效的
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            raise HTTPException(status_code=400, detail="Invalid URL. Must start with http:// or https://")
        
        # 添加浏览器头信息模拟真实浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com/",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
            
        # 获取网页内容
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0, headers=headers) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()  # 确保请求成功
            except Exception as e:
                print(f"Error fetching URL {url}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {e}")

        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找图标链接
        link = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
        if link and link.get("href"):
            icon_url = link["href"]

            # 如果图标 URL 是相对路径，转换为绝对路径
            if not icon_url.startswith(("http://", "https://")):
                icon_url = urljoin(url, icon_url)
            
            print(f"Icon found: {icon_url}")
            return {"icon_url": icon_url}
        else:
            # 尝试查找其他可能的图标
            apple_icon = soup.find("link", rel="apple-touch-icon")
            if apple_icon and apple_icon.get("href"):
                icon_url = apple_icon["href"]
                if not icon_url.startswith(("http://", "https://")):
                    icon_url = urljoin(url, icon_url)
                print(f"Apple icon found: {icon_url}")
                return {"icon_url": icon_url}
            
            # 返回域名的favicon.ico
            parsed_url = urlparse(url)
            domain_favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
            print(f"Using default favicon: {domain_favicon}")
            return {"icon_url": domain_favicon}

    except httpx.RequestError as e:
        print(f"Network error: {e}")
        raise HTTPException(status_code=500, detail=f"Network error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
