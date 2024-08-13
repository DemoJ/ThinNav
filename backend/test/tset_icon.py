import httpx
from urllib.parse import urlparse

def get_favicon_or_apple_touch_icon(url):
    """尝试获取网站的favicon.ico或apple-touch-icon.png的URL"""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # 检查是否存在favicon.ico
    try:
        favicon_response = httpx.get(f"{base_url}/favicon.ico", follow_redirects=True)
        if favicon_response.status_code == 200:
            return f"{base_url}/favicon.ico"
    except httpx.RequestError as e:
        print(f"Request error for favicon.ico: {e}")

    # 检查是否存在apple-touch-icon.png
    try:
        apple_touch_icon_response = httpx.get(f"{base_url}/apple-touch-icon.png", follow_redirects=True)
        if apple_touch_icon_response.status_code == 200:
            return f"{base_url}/apple-touch-icon.png"
    except httpx.RequestError as e:
        print(f"Request error for apple-touch-icon.png: {e}")

    return None

def test_get_favicon_or_apple_touch_icon():
    """测试获取网站图标URL的函数"""
    test_urls = [
        "https://www.baidu.com",  # 替换为你想测试的 URL
    ]

    for url in test_urls:
        icon_url = get_favicon_or_apple_touch_icon(url)
        print(f"Testing URL: {url}")
        if icon_url:
            print(f"Found icon URL: {icon_url}")
        else:
            print("No favicon or apple-touch-icon found.")

if __name__ == "__main__":
    test_get_favicon_or_apple_touch_icon()
