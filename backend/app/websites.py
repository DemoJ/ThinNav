import httpx
from PIL import Image, ImageDraw, ImageFont, ImageOps
from urllib.parse import urlparse
import tldextract
import io
import aiofiles
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .database import get_db
from .auth import get_current_user
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def fetch_website_description(url: str) -> str:
    """从网站抓取描述"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True, verify=False) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")

        meta_tags = [
            soup.find("meta", attrs={"name": "description"}),
            soup.find("meta", attrs={"property": "og:description"}),
            soup.find("meta", attrs={"property": "description"}),
            soup.find("meta", attrs={"property": "twitter:description"}),
            soup.find("meta", attrs={"itemprop": "description"}),
            soup.find("meta", attrs={"http-equiv": "description"})
        ]

        # 遍历找到的 meta 标签列表，返回第一个有 content 属性的标签
        for tag in meta_tags:
            if tag and tag.get("content"):
                logger.info(f"Description found: {tag.get('content')}")
                return tag.get("content").strip()

        # 如果没有找到，返回空字符串
        logger.info("No description found")
        return ""
    except Exception as e:
        print(f"Error fetching description from {url}: {e}")
        return ""


async def save_icon_image(image: Image.Image, filename: str) -> str:
    """保存图标图像并返回其 URL"""
    # 替换文件名中的非法字符
    filename = filename.replace(":", "_")

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # 异步保存到本地
    path = f"./icons/{filename}"
    if not path.endswith(".png"):
        path += ".png"

    async with aiofiles.open(path, "wb") as out_file:
        await out_file.write(output.read())

    # 返回保存后的图标 URL
    return path


async def get_icon(url):
    """尝试获取网站图标的URL"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    try:
        # 获取网页内容
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
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

            print(f"Icon found: {icon_url}")
            # 下载图标并返回 URL
            # 如果是 png 或者 ico 格式的图标，下载图标并返回
            if icon_url.endswith((".png", ".ico")):
                 async with httpx.AsyncClient() as client:
                    response = await client.get(icon_url)
                    response.raise_for_status()
                    icon_image = Image.open(io.BytesIO(response.content))
                    filename = f"{urlparse(url).netloc}_icon.png"
                    icon_url = await save_icon_image(icon_image, filename)
                    print(f"Icon saved: {icon_url}")
            elif icon_url.endswith(".svg"):
                # 如果是 svg 格式的图标，异步保存到本地svg
                async with httpx.AsyncClient() as client:
                    response = await client.get(icon_url)
                    response.raise_for_status()
                    filename = icon_url.split("/")[-1]
                    path = f"./icons/{filename}"
                    async with aiofiles.open(path, "wb") as out_file:
                        await out_file.write(response.content)
                    icon_url = path
            return icon_url
        else:
            raise HTTPException(status_code=404, detail="Icon not found")

    except Exception as e:
        print(f"Error fetching icon: {e}")
        return None


def generate_letter_icon(url):
    """使用网站二级域名的首字母或IP地址的首字母生成圆形图标"""
    extracted = tldextract.extract(url)
    domain = extracted.domain

    # 判断是否为IP地址
    parsed_url = urlparse(url)
    if parsed_url.hostname.replace(".", "").isdigit():
        # 使用IP地址的首字母
        letter = parsed_url.hostname[0].upper()
    else:
        # 使用二级域名的首字母
        letter = domain[0].upper() if domain else "U"  # 若无效域名则用'U'

    # 创建一个空白图像
    img_size = (64, 64)
    image = Image.new("RGB", img_size, color=(73, 109, 137))

    # 创建一个圆形蒙版
    mask = Image.new("L", img_size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + img_size, fill=255)

    # 应用蒙版以生成圆形图像
    image = ImageOps.fit(image, img_size, centering=(0.5, 0.5))
    image.putalpha(mask)

    # 选择字体和字号
    font_path = "./fonts/Roboto-Regular.ttf"  # 使用相对路径指向Roboto字体文件
    try:
        font = ImageFont.truetype(font_path, 48)
    except IOError:
        font = ImageFont.load_default()  # 加载默认字体

    draw = ImageDraw.Draw(image)

    # 计算文字边界框
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 垂直居中调整
    position = (
        (img_size[0] - text_width) / 2,
        (img_size[1] - text_height) / 2 - (bbox[1] / 2),
    )

    # 绘制文字
    draw.text(position, letter, (255, 255, 255), font=font)

    return image


async def  get_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
        logger.info(f"Title found: {title}")
        return title
    except Exception as e:
        print(f"Error fetching title from {url}: {e}")
        return ""



@router.post("/", response_model=schemas.Website)
async def create_website(
    website: schemas.WebsiteCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    url = website.url

    # 尝试获取图标的 URL
    icon_url = await get_icon(url)
    logger.info(f"Icon URL: {icon_url}")

    if not icon_url:
        # 如果图标不存在，则生成一个默认图标并保存
        default_icon = generate_letter_icon(url)
        filename = f"{urlparse(url).netloc}_default.png"
        icon_url = await save_icon_image(default_icon, filename)

    if not website.name:
        website.name = await get_title(url)
    logger.info(f"Name: {website.name}")


    # 抓取网站描述
    description = await fetch_website_description(url)
    logger.info(f"Description: {description}")
    # 创建网站条目
    db_website = models.Website(
        name=website.name,
        url=url,
        icon_url=icon_url,
        description=description,
        order=website.order,
        category_id=website.category_id,
    )
    db.add(db_website)
    await db.commit()
    await db.refresh(db_website)

    # 获取关联的 category_name
    category_name = (
        await db.execute(
            select(models.Category.name).where(
                models.Category.id == db_website.category_id
            )
        )
    ).scalar()

    return schemas.Website(
        id=db_website.id,
        name=db_website.name,
        icon_url=db_website.icon_url,
        description=db_website.description,
        order=db_website.order,
        url=db_website.url,
        category_id=db_website.category_id,
        category_name=category_name,
    )


@router.get("/", response_model=schemas.PaginatedWebsites)
async def read_websites(
    db: AsyncSession = Depends(get_db),
    skip: Optional[int] = Query(None, description="Number of records to skip", ge=0),
    limit: Optional[int] = Query(
        None, description="Maximum number of records to return", ge=1
    ),
    all_data: Optional[bool] = Query(
        False, description="Fetch all data without pagination"
    ),
    search: Optional[str] = Query(None, description="Search keyword for website name"),
):
    # 基础查询语句，包含左连接和排序
    stmt = (
        select(models.Website, models.Category.name.label("category_name"))
        .join(
            models.Category,
            models.Website.category_id == models.Category.id,
            isouter=True,
        )
        .order_by(models.Website.order)  # 按 order 字段排序
    )

    # 如果有搜索关键词，添加模糊搜索条件
    if search:
        stmt = stmt.where(models.Website.name.ilike(f"%{search}%"))

    # 如果 all_data 为 True，获取所有数据
    if all_data:
        result = await db.execute(stmt)
        websites = result.all()

        response_data = [
            schemas.Website(
                id=website.id,
                name=website.name,
                icon_url=website.icon_url,
                description=website.description,
                order=website.order,
                url=website.url,
                category_id=website.category_id,
                category_name=category_name,
            )
            for website, category_name in websites
        ]

        total = len(response_data)
        return schemas.PaginatedWebsites(data=response_data, total=total)

    # 如果没有 all_data，为分页数据
    total = await db.scalar(select(func.count()).select_from(stmt.subquery()))

    stmt = stmt.offset(skip or 0).limit(limit or 10)
    result = await db.execute(stmt)
    websites = result.all()

    response_data = [
        schemas.Website(
            id=website.id,
            name=website.name,
            icon_url=website.icon_url,
            description=website.description,
            order=website.order,
            url=website.url,
            category_id=website.category_id,
            category_name=category_name,
        )
        for website, category_name in websites
    ]

    return schemas.PaginatedWebsites(data=response_data, total=total)


@router.put("/{website_id}", response_model=schemas.Website)
async def update_website(
    website_id: int,
    website: schemas.WebsiteCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")

    for key, value in website.model_dump(exclude_unset=True).items():
        setattr(db_website, key, value)
    await db.commit()
    await db.refresh(db_website)

    # 获取关联的 category_name
    category_name = (
        await db.execute(
            select(models.Category.name).where(
                models.Category.id == db_website.category_id
            )
        )
    ).scalar()

    return schemas.Website(
        id=db_website.id,
        name=db_website.name,
        icon_url=db_website.icon_url,
        description=db_website.description,
        order=db_website.order,
        url=db_website.url,
        category_id=db_website.category_id,
        category_name=category_name,
    )


@router.delete("/{website_id}", status_code=204)
async def delete_website(
    website_id: int,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_website = await db.get(models.Website, website_id)
    if not db_website:
        raise HTTPException(status_code=404, detail="Website not found")
    await db.delete(db_website)
    await db.commit()
    return {"ok": True}
