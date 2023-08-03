from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# sync_playwright() returns a sync Playwright Object
# with ... as ... ensures proper resource management & close the Playwright instance at the end 

with sync_playwright() as p:
    custom_user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
    custom_referrer = "https://www.facebook.com/"
    custom_http_header = [
        f"--user-agent={custom_user_agent}", 
        f"--referrer={custom_referrer}",
    ]

    browser = p.chromium.launch(headless=False, slow_mo=50, args=custom_http_header)
    
    # creates a new page within the browser
    page = browser.new_page()

    # Set the user-agent header
    page.set_extra_http_headers({"User-Agent": custom_user_agent})

    # Set the referer header
    page.set_extra_http_headers({"referer": custom_referrer})

    # visit the url 
    page.goto("https://www.google.com.sg/") 

    # Get the user-agent string
    user_agent = page.evaluate('''() => window.navigator.userAgent''')
    print("User-Agent:", user_agent)

    # Get the referrer
    referrer = page.evaluate('''() => document.referrer''')
    print("Referrer:", referrer)

