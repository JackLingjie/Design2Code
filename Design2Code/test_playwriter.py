import asyncio  
from playwright.async_api import async_playwright  
  
async def html_to_image(html_content, output_path):  
    async with async_playwright() as playwright:  
        # 启动浏览器  
        browser = await playwright.chromium.launch()  
        # 打开新页面  
        page = await browser.new_page()  
        # 设置页面内容  
        await page.set_content(html_content)  
        # 截取全页面截图  
        await page.screenshot(path=output_path, full_page=True)  
        # 关闭浏览器  
        await browser.close()  
  
html_content = """  
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Test HTML</title>  
</head>  
<body>  
    <h1>Hello, World!</h1>  
    <p>This is a test HTML content.</p>  
</body>  
</html>  
"""  
  
output_path = "output_image.png"  
  
# 运行异步事件循环  
asyncio.run(html_to_image(html_content, output_path))  
  
print(f"Image saved to {output_path}")  