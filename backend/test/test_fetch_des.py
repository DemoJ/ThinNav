import httpx
from bs4 import BeautifulSoup

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

# 测试脚本
async def main():
    url = "https://www.baidu.com"  # 替换为你想测试的 URL
    description = await fetch_website_description(url)
    print(f"Website description: {description}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
