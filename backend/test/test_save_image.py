import io
from PIL import Image, ImageDraw, ImageFont
import os
import tldextract
from urllib.parse import urlparse

def save_icon_image(image: Image.Image, filename: str) -> str:
    # 确保目录存在
    TEST_ICON_DIR = './icons'
    if not os.path.exists(TEST_ICON_DIR):
        os.makedirs(TEST_ICON_DIR)

    """保存图标图像并返回其 URL"""
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # 保存到本地或上传到某个存储服务
    path = f"{TEST_ICON_DIR}/{filename}"
    if not path.endswith(".png"):
        path += ".png"

    with open(path, "wb") as out_file:
        out_file.write(output.read())

    # 返回保存后的图标 URL
    return path

def generate_letter_icon(url):
    """使用网站二级域名的首字母或IP地址的首字母生成图标"""
    extracted = tldextract.extract(url)
    domain = extracted.domain

    # 判断是否为IP地址
    parsed_url = urlparse(url)
    if parsed_url.hostname.replace('.', '').isdigit():
        # 使用IP地址的首字母
        letter = parsed_url.hostname[0].upper()
    else:
        # 使用二级域名的首字母
        letter = domain[0].upper() if domain else 'U'  # 若无效域名则用'U'

    # 创建一个空白图像
    img_size = (64, 64)
    image = Image.new("RGB", img_size, color=(73, 109, 137))

    # 选择字体和字号
    font_path = "arial.ttf"  # 或者使用绝对路径
    try:
        font = ImageFont.truetype(font_path, 36)
    except IOError:
        font = ImageFont.load_default()  # 加载默认字体

    draw = ImageDraw.Draw(image)

    # 计算文字位置以居中显示
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = ((img_size[0] - text_width) / 2, (img_size[1] - text_height) / 2)

    # 绘制文字
    draw.text(position, letter, (255, 255, 255), font=font)

    return image

url = "http://a.b.c.com:9999"
default_icon = generate_letter_icon(url)

# 使用 netloc 作为文件名，并替换掉 : 号
filename = f"{urlparse(url).netloc.replace(':', '_')}_default.png"
icon_url = save_icon_image(default_icon, filename)

print(f"Generated icon URL: {icon_url}")
