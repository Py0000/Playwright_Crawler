import time
import random

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import user_actions as action
import utility as util
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


def get_dataset(page, base_folder_name, url_list):
    error_list = []

    index = 0
    for url in url_list:
        formatted_index_str = util.format_index_base_file_name(index)

        # visit the url 
        page.goto(url) 
        add_time_for_page_to_load(page)

        try:
            # Get the HTML content of the page
            html_content = page.content()
            soup = BeautifulSoup(html_content, "lxml")

            embedded_path = util.get_embedded_links(base_folder_name, soup, page, url)

            # Get the user-agent & referrer string
            util_log.test_check_user_agent(page)
            util_log.test_check_referrer(page)

            index += 1

            if soup is not None:
                util.save_html_script(base_folder_name, soup.prettify(), formatted_index_str)
                

                #Scrape embedded link
            
        except Exception as e:
            util.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str)
            error_list.append(index)
            index += 1
            continue
    
        time.sleep(random.randint(5, 10))
    
    for j in error_list:
        print("Error occurred for link: ", j)
    
    print("Crawled dataset generated...")


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
        
        


def setup_desktop_user_browser(custom_user_agent, custom_referer):
    return


def crawl(url_list):
    print("\nCrawling in progress...")

    custom_http_header = [
        f"--user-agent={util.DESKTOP_USER_AGENT}", 
        f"--referer={util.GOOGLE_REFERRER}",
    ]

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, slow_mo=50, args=custom_http_header)

    # creates a new page within the browser
    page = browser.new_page()

    # Set the user-agent & referrer header
    page.set_extra_http_headers({"User-Agent": util.DESKTOP_USER_AGENT})
    page.set_extra_http_headers({"referer": util.GOOGLE_REFERRER})

    # Can add setting the config for mobile/desktop/bots

    # Generate folders required for crawling
    base_folder_name = f"{util.CRAWLED_DATA_IDENTIFIER}"
    sub_folder_list = [
        util.CRAWLED_HTML_SCRIPT_FOLDER,
        util.CRAWLED_EMBEDDED_LINK_FOLDER,
    ]

    util.generate_folder_for_crawling(base_folder_name, sub_folder_list)

    get_dataset(page, base_folder_name, url_list)

    browser.close()
    p.stop()

    print("\nCrawling done...")


crawl(["https://www.google.com.sg/"])