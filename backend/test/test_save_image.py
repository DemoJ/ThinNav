import io
from PIL import Image, ImageDraw, ImageFont
import os
import tldextract
from urllib.parse import urlparse

def save_icon_image(image: Image.Image, filename: str) -> str:
    # 确保目录存在
    TEST_ICON_DIR='./icons'
    if not os.path.exists(TEST_ICON_DIR):
        os.makedirs(TEST_ICON_DIR)

    """保存图标图像并返回其 URL"""
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # 保存到本地或上传到某个存储服务
    path = f"./icons/{filename}"
    with open(path, "wb") as out_file:
        out_file.write(output.read())

    # 返回保存后的图标 URL
    return f"./icons/{filename}"

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

url="http://10.11.0.10:8087/"
default_icon = generate_letter_icon(url)
filename = f"{urlparse(url).netloc}_default.png"
icon_url = save_icon_image(default_icon, filename)
