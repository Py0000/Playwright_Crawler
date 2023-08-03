from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

# sync_playwright() returns a sync Playwright Object
# with ... as ... ensures proper resource management & close the Playwright instance at the end 

def test_check_user_agent(page):
    user_agent = page.evaluate('''() => window.navigator.userAgent''')
    print("User-Agent:", user_agent)

def test_check_referrer(page):
    referrer = page.evaluate('''() => document.referrer''')
    print("Referrer:", referrer)


with sync_playwright() as p:
    
    custom_user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
    custom_referer = "https://www.facebook.com/"

    custom_http_header = [
        # f"--user-agent={custom_user_agent}", 
        f"--referer={custom_referer}",
    ]

    browser = p.chromium.launch(headless=False, slow_mo=50, args=custom_http_header)


    # browser = p.chromium.launch(headless=False, slow_mo=50)

    # creates a new page within the browser
    page = browser.new_page()

    # Set the user-agent header
    # page.set_extra_http_headers({"User-Agent": custom_user_agent})

    # Set the referer header
    page.set_extra_http_headers({"referer": custom_referer})

    # visit the url 
    page.goto("https://www.google.com.sg/") 
    time.sleep(5)

    # Get the user-agent string
    test_check_user_agent(page)

    # Get the referrer
    test_check_referrer(page)

    # Wait for the page to load completely (wait for the load event)
    page.wait_for_load_state('load')

    # Get the HTML content of the page
    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    print(soup.prettify())

