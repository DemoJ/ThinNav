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
async def get_icon(request: URLRequest,current_user: models.Admin = Depends(get_current_user)):
    url = request.url
    try:
        # 获取网页内容
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()  # 确保请求成功

        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找图标链接
        link = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
        if link and link.get("href"):
            icon_url = link["href"]

            # 如果图标 URL 是相对路径，转换为绝对路径
            if not icon_url.startswith(("http://", "https://")):
                from urllib.parse import urljoin

                icon_url = urljoin(url, icon_url)

            return {"icon_url": icon_url}
        else:
            raise HTTPException(status_code=404, detail="Icon not found")

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
