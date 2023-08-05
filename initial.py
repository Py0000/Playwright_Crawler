import time
import random

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import user_actions as action
import utility as util

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



def get_html_content(page, base_folder_name, formatted_index, actual_url, embedded_flag):
    # Can add mouse movement here

    screenshot_path = util.get_screenshot_file_path(base_folder_name, formatted_index)
    action.save_screenshot(page, screenshot_path)
    print("Screenshot Captured...")

    # Can add page scroll here

    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    scraped_url = page.url
    util.detect_redirection(base_folder_name, scraped_url, actual_url)
    util.save_crawled_url(base_folder_name, scraped_url)

    embedded_file_path = ""
    if not embedded_flag:
        embedded_file_path = util.get_embedded_links(base_folder_name, soup, page, actual_url)
    
    util.get_all_html_tags(base_folder_name, soup, formatted_index)

    print("Actual url: ", actual_url)
    print("Url visited: ", scraped_url)
    util.test_check_user_agent(page)
    util.test_check_referrer(page)

    return soup.prettify(), embedded_file_path


def scrape_content(page, base_folder_name, referer_url, actual_url, formatted_index, embedded_flag):
    # If it is the seed url, visit google first
    # Then inject a javascript click-through to visit the seed url to ensure no empty referrer
    if not embedded_flag:
        referer_url = referer_url + actual_url

    # Set the referrer first
    page.goto(referer_url) 
    add_time_for_page_to_load(page)

     # Visit the actual webpage
    page.evaluate('window.location.href = "{}";'.format(actual_url))
    add_time_for_page_to_load(page)

    return get_html_content(page, base_folder_name, formatted_index, actual_url, embedded_flag)


def crawl_depth_one_embedded_links(page, embedded_link_path, index, error_list, base_folder_name, referrer):
    url_list = util.get_level_one_embedded_link(embedded_link_path)

    for url in url_list:
        formatted_index_str = util.format_index_base_file_name(index)
        try:
            content, _ = scrape_content(page, base_folder_name, referrer, url, formatted_index_str, embedded_flag=True)

            if content is not None:
                util.save_html_script(base_folder_name, content, formatted_index_str)
        
        except Exception as e:
            util.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str)
            util.save_crawled_url(base_folder_name, util.ERROR_URL_FLAG)
            error_list.append(index)
            continue

        index += 1
        time.sleep(random.randint(5, 10))
            
    return index, error_list


def get_dataset(page, base_folder_name, url_list):
    error_list = []

    index = 0
    for url in url_list:
        formatted_index_str = util.format_index_base_file_name(index)

        try:
            referrer = util.GOOGLE_SEARCH_QUERY_REFERRER
            content, embedded_path = scrape_content(page, base_folder_name, referrer, url, formatted_index_str, embedded_flag=False)
            index += 1

            if content is not None:
                util.save_html_script(base_folder_name, content, formatted_index_str)
                
                # Scrape embedded link
                referrer = url
                index, error_list = crawl_depth_one_embedded_links(page, embedded_path, index, error_list, base_folder_name, referrer)
            
        except Exception as e:
            util.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str)
            util.save_crawled_url(base_folder_name, util.ERROR_URL_FLAG)
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
        # f"--referer={util.GOOGLE_REFERRER}",
    ]

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, slow_mo=50, args=custom_http_header)

    # creates a new page within the browser
    page = browser.new_page()

    # Set the user-agent & referrer header
    page.set_extra_http_headers({"User-Agent": util.DESKTOP_USER_AGENT})
    # page.set_extra_http_headers({"referer": util.GOOGLE_REFERRER})

    # Can add setting the config for mobile/desktop/bots

    # Generate folders required for crawling
    base_folder_name = f"{util.CRAWLED_DATA_IDENTIFIER}"
    sub_folder_list = [
        util.CRAWLED_HTML_SCRIPT_FOLDER,
        util.CRAWLED_EMBEDDED_LINK_FOLDER,
        util.CRAWLED_PAGE_SCREENSHOT_FOLDER,
        util.CRAWLED_URL_FOLDER,
        util.CRAWLED_HTML_TAG_FOLDER,
        util.CRAWLED_REDIRECTION_FOLDER,
    ]

    util.generate_folder_for_crawling(base_folder_name, sub_folder_list)

    get_dataset(page, base_folder_name, url_list)

    browser.close()
    p.stop()

    print("\nCrawling done...")


crawl(["https://www.youtube.com/"])