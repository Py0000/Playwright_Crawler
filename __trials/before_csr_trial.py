from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

p = sync_playwright().start()
browser = p.chromium.launch(headless=False, slow_mo=50)
context =  browser.new_context()

page = context.new_page()

page.route('**/*', lambda route, request: 
        route.abort() if 'script' in request.resource_type else route.continue_())

page.goto("https://www.google.com.sg")
page.screenshot(path="ss.png", full_page=True)

server_content = page.content()
soup = BeautifulSoup(server_content, "lxml")

print(soup.prettify())