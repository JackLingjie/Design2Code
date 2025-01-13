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
  
html_content = """<html>\n<header>\n<meta charset=\"utf-8\"/>\n<meta content=\"width=device-width, initial-scale=1\" name=\"viewport\"/>\n<link crossorigin=\"anonymous\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\" integrity=\"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u\" rel=\"stylesheet\"/>\n<link crossorigin=\"anonymous\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css\" integrity=\"sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp\" rel=\"stylesheet\"/>\n<style>\n        .header { margin: 20px 0; }\n        nav ul.nav-pills li { background-color: #333; border-radius: 4px; margin-right: 10px; }\n        .col-lg-3 { width: 24%; margin-right: 1.333333%; }\n        .col-lg-6 { width: 49%; margin-right: 2%; }\n        .col-lg-12, .col-lg-3, .col-lg-6 { margin-bottom: 20px; border-radius: 6px; background-color: #f5f5f5; padding: 20px; }\n        .row .col-lg-3:last-child, .row .col-lg-6:last-child { margin-right: 0; }\n        footer { padding: 20px 0; text-align: center; border-top: 1px solid #bbb; }\n    </style>\n<title>Job Recruitment Portal</title>\n</header>\n<body>\n<main class=\"container\">\n<div class=\"header clearfix\">\n<nav>\n<ul class=\"nav nav-pills pull-left\">\n<li><a href=\"#\">Home</a></li>\n<li><a href=\"#\">Job Listings</a></li>\n<li class=\"active\"><a href=\"#\">About Us</a></li>\n<li><a href=\"#\">Contact</a></li>\n<li><a href=\"#\">FAQ</a></li>\n</ul>\n</nav>\n</div>\n<div class=\"row\"><div class=\"col-lg-3\">\n<h4>Featured Jobs</h4><p>Browse our most popular job listings and find your perfect fit today!</p>\n<a class=\"btn btn-danger\" href=\"#\" role=\"button\">View Jobs</a>\n</div>\n<div class=\"col-lg-3\">\n<h4>Our Services</h4><p>Discover how we can help you in your job search - from resume building to interview coaching.</p>\n<a class=\"btn btn-warning\" href=\"#\" role=\"button\">Learn More</a>\n</div>\n<div class=\"col-lg-3\">\n<h4>Job Alerts</h4><p>Sign up to receive email alerts for new job postings that match your interests.</p>\n<a class=\"btn btn-success\" href=\"#\" role=\"button\">Sign Up Now</a>\n</div>\n<div class=\"col-lg-3\">\n<h4>Contact Us</h4><p>Have any questions or need help? Our friendly team is here to support you!</p>\n<a class=\"btn btn-success\" href=\"#\" role=\"button\">Contact Support</a>\n</div>\n</div>\n<div class=\"row\"><div class=\"col-lg-12\">\n<h4>About Us</h4><p>Learn more about our mission and history, and what sets us apart in the recruitment industry.</p>\n<a class=\"btn btn-danger\" href=\"#\" role=\"button\">Read More</a>\n</div>\n</div>\n<div class=\"row\"><div class=\"col-lg-6\">\n<h4>Employers</h4><p>Looking to post a job? We offer a variety of employer services, check it out now.</p>\n<a class=\"btn btn-danger\" href=\"#\" role=\"button\">For Employers</a>\n</div>\n<div class=\"col-lg-6\">\n<h4>Job Seekers</h4><p>Whether your'e looking for your first job or your next job, we have resources that can help you get there.</p>\n<a class=\"btn btn-warning\" href=\"#\" role=\"button\">For Job Seekers</a>\n</div>\n</div>\n<footer class=\"footer\">\n<p>\u00a9 Job Recruitment Portal 2022</p>\n</footer>\n</main>\n<script src=\"js/jquery.min.js\"></script>\n<script src=\"js/bootstrap.min.js\"></script>\n</body>\n</html>"""  
  
output_path = "output_image.png"  
  
# 运行异步事件循环  
asyncio.run(html_to_image(html_content, output_path))  
  
print(f"Image saved to {output_path}")  