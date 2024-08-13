import httpx
from PIL import Image, ImageDraw, ImageFont
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

router = APIRouter()


async def fetch_website_description(url: str) -> str:
    """从网站抓取描述"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            # 处理可能的重定向
            final_url = response.url
            print(f"Final URL after redirects: {final_url}")

            soup = BeautifulSoup(response.text, "html.parser")
            description_tag = soup.find("meta", attrs={"name": "description"})
            if description_tag:
                return description_tag.get("content", "").strip()
            return ""
    except Exception as e:
        print(f"Error fetching description from {url}: {e}")
        return ""


async def save_icon_image(image: Image.Image, filename: str) -> str:
    """保存图标图像并返回其 URL"""
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # 保存到本地或上传到某个存储服务
    path = f"/icons/{filename}"
    async with aiofiles.open(path, "wb") as out_file:
        await out_file.write(output.read())

    # 返回保存后的图标 URL
    return f"/icons/{filename}"

def get_favicon_or_apple_touch_icon(url):
    """尝试获取网站的favicon.ico或apple-touch-icon.png的URL"""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # 检查是否存在favicon.ico
    favicon_response = httpx.get(f"{base_url}/favicon.ico", follow_redirects=True)
    if favicon_response.status_code == 200:
        return f"{base_url}/favicon.ico"

    # 检查是否存在apple-touch-icon.png
    apple_touch_icon_response = httpx.get(
        f"{base_url}/apple-touch-icon.png", follow_redirects=True
    )
    if apple_touch_icon_response.status_code == 200:
        return f"{base_url}/apple-touch-icon.png"

    return None


def generate_letter_icon(url):
    """使用网站首字母生成图标"""
    extracted = tldextract.extract(url)
    domain = extracted.domain
    letter = domain[0].upper()

    # 创建一个空白图像
    img_size = (64, 64)
    image = Image.new("RGB", img_size, color=(73, 109, 137))

    # 选择字体和字号
    font = ImageFont.truetype("arial.ttf", 36)
    draw = ImageDraw.Draw(image)

    # 计算文字位置以居中显示
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = ((img_size[0] - text_width) / 2, (img_size[1] - text_height) / 2)

    # 绘制文字
    draw.text(position, letter, (255, 255, 255), font=font)

    return image


@router.post("/", response_model=schemas.Website)
async def create_website(
    website: schemas.WebsiteCreate,
    current_user: models.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    url = website.url

    # 尝试获取图标的 URL
    icon_url = get_favicon_or_apple_touch_icon(url)

    if not icon_url:
        # 如果图标不存在，则生成一个默认图标并保存
        default_icon = generate_letter_icon(url)
        filename = f"{urlparse(url).netloc}_default.png"
        icon_url = await save_icon_image(default_icon, filename)

    # 抓取网站描述
    description = await fetch_website_description(url)

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
    skip: int = Query(0, description="Number of records to skip", ge=0),
    limit: int = Query(10, description="Maximum number of records to return", ge=1),
):
    # 获取总记录数
    total = await db.scalar(select(func.count()).select_from(models.Website))

    # 获取分页数据，按照 order 字段排序
    stmt = (
        select(models.Website, models.Category.name.label("category_name"))
        .join(
            models.Category,
            models.Website.category_id == models.Category.id,
            isouter=True,
        )
        .order_by(models.Website.order)  # 按 order 字段排序
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    websites = result.all()

    # 处理结果
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

    # 返回分页数据和总记录数
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
