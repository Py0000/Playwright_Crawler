import time
import random

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import user_actions as action
import utility_logging as util_log

# sync_playwright() returns a sync Playwright Object
# with ... as ... ensures proper resource management & close the Playwright instance at the end 

def add_time_for_page_to_load(page):
    try:
        # Wait for the page to load completely (wait for the load event)
        page.wait_for_load_state('load')
    except:
        pass
    
    try:
        # Wait for the body tag to be loaded
        page.wait_for_selector('body')
    except:
        pass



with sync_playwright() as p:
    
    custom_bot_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    custom_referer = "https://www.facebook.com/"

    custom_http_header = [
        f"--user-agent={custom_user_agent}", 
        f"--referer={custom_referer}",
    ]

    browser = p.chromium.launch(headless=False, slow_mo=50, args=custom_http_header)

    # creates a new page within the browser
    page = browser.new_page()

    # Set the user-agent & referrer header
    page.set_extra_http_headers({"User-Agent": custom_user_agent})
    page.set_extra_http_headers({"referer": custom_referer})

    # visit the url 
    page.goto("http://www.youtube.com/") 
    time.sleep(5)

    # Get the user-agent & referrer string
    util_log.test_check_user_agent(page)
    util_log.test_check_referrer(page)

    #add_time_for_page_to_load(page)

    #action.move_mouse_smoothly_top_left_bottom_right(page)

    #action.mouse_click(page, 'left')

    #action.save_screenshot(page, "test.png")

    #action.page_scroll(page)

    #alert_btn = page.locator("text=Trigger a Confirmation")

    #action.dismiss_js_alert(page)

    #alert_btn.click()
    #print(page.locator("id=msg").inner_text())
    #time.sleep(3)
    
    # Get the HTML content of the page
    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    print("Retrieved html content")

