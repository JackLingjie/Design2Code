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
  
html_content = """<html tid="0"> <body tid="1"> <div id="divSearchResults" tid="2"> <input class="not-empty" id="DeviceType" tid="3"/> <input class="not-empty" id="NumFound" tid="4"/> <input class="not-empty" id="VacancySearchParameters_PageIndex" tid="5"/> <div class="job-card" tid="6"> <div class="row" tid="7"> <div class="col-12 job-card-head" tid="8"> <a tid="9"> <h2 tid="10"> Senior Researcher: Products, Services and Solutions(ICT) </h2> </a> </div> <div class="col-6 job-card-left" tid="11"> <ul tid="12"> <li tid="13"> Gauteng </li> <li tid="14"> Job Type: Permanent </li> <li tid="15"> Posted: 21 Oct 2020 <br tid="16"/> <span tid="17"> 61 Days left </span> </li> </ul> </div> <div class="col-6 job-card-right" tid="18"> <span class="mx-2 d-flex" tid="19"> <a class="line-0" tid="20"> <i class="far fa-envelope position-relative" tid="21"> </i> </a> </span> <span class="mr-0 ml-2 d-flex" tid="22"> <a class="line-0" tid="23"> <i class="far fa-heart" tid="24"> </i> </a> </span> </div> </div> </div> <div class="job-card" tid="25"> <div class="row" tid="26"> <div class="col-12 job-card-head" tid="27"> <a tid="28"> <h2 tid="29"> Various - Control Specialist, Robotic Technician &amp; Process Engineer </h2> </a> </div> <div class="col-6 job-card-left" tid="30"> <ul tid="31"> <li tid="32"> Pretoria </li> <li tid="33"> Job Type: Permanent </li> <li tid="34"> Posted: 21 Oct 2020 <br tid="35"/> <span tid="36"> 61 Days left </span> </li> </ul> </div> <div class="col-6 job-card-right" tid="37"> <span class="mx-2 d-flex" tid="38"> <a class="line-0" tid="39"> <i class="far fa-envelope position-relative" tid="40"> </i> </a> </span> <span class="mr-0 ml-2 d-flex" tid="41"> <a class="line-0" tid="42"> <i class="far fa-heart" tid="43"> </i> </a> </span> </div> </div> </div> <div class="job-card" tid="44"> <div class="row" tid="45"> <div class="col-12 job-card-head" tid="46"> <a tid="47"> <h2 tid="48"> Senior Audit Manager Financial Services Audit </h2> </a> </div> <div class="col-6 job-card-left" tid="49"> <ul tid="50"> <li tid="51"> Johannesburg </li> <li tid="52"> Job Type: Permanent </li> <li tid="53"> Posted: 21 Oct 2020 <br tid="54"/> <span tid="55"> 61 Days left </span> </li> </ul> </div> <div class="col-6 job-card-right" tid="56"> <span class="mx-2 d-flex" tid="57"> <a class="line-0" tid="58"> <i class="far fa-envelope position-relative" tid="59"> </i> </a> </span> <span class="mr-0 ml-2 d-flex" tid="60"> <a class="line-0" tid="61"> <i class="far fa-heart" tid="62"> </i> </a> </span> <span tid="63"> <img class="d-inline-block" tid="64"/> </span> </div> </div> </div> <div class="w-100 hide-lg mb-15 c24-refine-results" tid="65"> <button class="btn btn-primary green-hover refine-search-btn" tid="66"> <span class="mr-15 d-inline-block position-relative bottom-3" tid="67"> <img tid="68"/> </span> REFINE YOUR SEARCH </button> </div> </div> </body> </html>"""  
  
output_path = "output_image.png"  
  
# 运行异步事件循环  
asyncio.run(html_to_image(html_content, output_path))  
  
print(f"Image saved to {output_path}")  