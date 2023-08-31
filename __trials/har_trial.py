from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(record_har_path='path_to_save.har')
    page = context.new_page()
    page.goto('https://www.example.com/')
    # Perform some actions here...
    page.close()
    context.close()
    browser.close()
