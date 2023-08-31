from playwright.sync_api import sync_playwright
import time
def load_html_content(html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_context().new_page()
        
        # Set page content directly
        page.set_content(html_content)

        time.sleep(20)
        
        # Perform any operations you want, e.g., take a screenshot
        page.screenshot(path='screenshot.png', full_page=True)
        
        # browser.close()

# Example usage
with open('html_script_aft.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

load_html_content(html_content)

