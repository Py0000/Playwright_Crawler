import time
import random

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import crawler_support as crawler
import user_actions as action
import utility as util



def desktop_user_mouse_movement(page):
    action.dismiss_js_alert(page)
    action.move_mouse_smoothly_top_left_bottom_right(page)
    action.mouse_click(page, 'left')
    action.mouse_click(page, "right")


def mobile_user_hand_gesture(page):
    action.dismiss_js_alert(page)
    action.touchscreen(page)


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

    try:
        page.waitForLoadState('networkidle')
    except:
        pass
    

def wait_for_page_to_load(page, action_flag):
    if action_flag:
        action.move_mouse_smoothly_top_left_bottom_right(page)
    
    add_time_for_page_to_load(page)


def check_and_execute_user_actions(base_folder_name, action_flag, page):
    if not action_flag:
        pass
    else:
        if "desktop" in base_folder_name:
            desktop_user_mouse_movement(page)
        if "mobile" in base_folder_name:
            mobile_user_hand_gesture(page)


def check_and_execute_scroll(action_flag, page):
    if action_flag:
        action.page_scroll(page)
    else:
        pass

def get_html_content(page, base_folder_name, formatted_index, actual_url, action_flag, embedded_flag):
    
    check_and_execute_user_actions(base_folder_name, action_flag, page)

    screenshot_path = crawler.get_screenshot_file_path(base_folder_name, formatted_index)
    action.save_screenshot(page, screenshot_path)
    print("Screenshot Captured...")

    check_and_execute_scroll(action_flag, page)

    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    scraped_url = page.url
    crawler.detect_redirection(base_folder_name, scraped_url, actual_url)
    crawler.save_crawled_url(base_folder_name, scraped_url)

    embedded_file_path = ""
    if not embedded_flag:
        embedded_file_path = crawler.get_embedded_links(base_folder_name, soup, page, actual_url)
    
    crawler.get_all_html_tags(base_folder_name, soup, formatted_index)

    print("Actual url: ", actual_url)
    print("Url visited: ", scraped_url)
    crawler.test_check_user_agent(page)
    crawler.test_check_referrer(page)

    return soup.prettify(), embedded_file_path


def scrape_content(page, base_folder_name, referer_url, actual_url, formatted_index, action_flag, embedded_flag):
    isDesktop = util.CONFIG_DESKTOP_BOT in base_folder_name or util.CONFIG_DESKTOP_USER in base_folder_name 
    isMobile = util.CONFIG_MOBILE_BOT in base_folder_name or util.CONFIG_MOBILE_USER in base_folder_name

    if isDesktop and referer_url is not None :
        # If it is the seed url, visit google first
        # Then inject a javascript click-through to visit the seed url to ensure no empty referrer
        if not embedded_flag and referer_url == util.GOOGLE_SEARCH_QUERY_REFERRER:
            referer_url = referer_url + actual_url
            print("Google Referrer executed")

        # Set the referrer first
        page.goto(referer_url) 
        wait_for_page_to_load(page, action_flag)

        # Visit the actual webpage
        page.evaluate('window.location.href = "{}";'.format(actual_url))

    elif isMobile and referer_url is not None :
        page.set_extra_http_headers({"Referer": referer_url})
        page.goto(actual_url)

    # Not referrer set
    else:
        page.goto(actual_url)
        
    wait_for_page_to_load(page, action_flag)
    return get_html_content(page, base_folder_name, formatted_index, actual_url, action_flag, embedded_flag)


def crawl_depth_one_embedded_links(page, embedded_link_path, index, error_list, base_folder_name, referrer, action_flag):
    url_list = crawler.get_level_one_embedded_link(embedded_link_path)

    for url in url_list:
        formatted_index_str = util.format_index_base_file_name(index)
        try:
            content, _ = scrape_content(page, base_folder_name, referrer, url, formatted_index_str, action_flag, embedded_flag=True)

            if content is not None:
                crawler.save_html_script(base_folder_name, content, formatted_index_str)
        
        except Exception as e:
            crawler.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str)
            crawler.save_crawled_url(base_folder_name, util.ERROR_URL_FLAG)
            error_list.append(index)
            continue

        index += 1
        time.sleep(random.randint(5, 10))
            
    return index, error_list


def get_dataset(page, base_folder_name, url_list, referrer, action_flag):
    error_list = []

    index = 0
    for url in url_list:
        formatted_index_str = util.format_index_base_file_name(index)

        try:
            content, embedded_path = scrape_content(page, base_folder_name, referrer, url, formatted_index_str, action_flag, embedded_flag=False)
            index += 1

            if content is not None:
                crawler.save_html_script(base_folder_name, content, formatted_index_str)
                
                # Scrape embedded link
                referrer = url if referrer is not None else referrer
                index, error_list = crawl_depth_one_embedded_links(page, embedded_path, index, error_list, base_folder_name, referrer, action_flag)
            
        except Exception as e:
            crawler.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str)
            crawler.save_crawled_url(base_folder_name, util.ERROR_URL_FLAG)
            error_list.append(index)
            index += 1
            continue
    
        time.sleep(random.randint(5, 10))
    
    for j in error_list:
        print("Error occurred for link: ", j)
    
    print("Crawled dataset generated...")
        
        


def setup_desktop_crawler(playwright_object, config):
    # desktop_user_agent = util.DESKTOP_USER_AGENT_LIST[random.randint(1,2)]
    user_agent_map = {
        util.CONFIG_DESKTOP_USER: [f"--user-agent={util.DESKTOP_USER_AGENT_2}"],
        util.CONFIG_DESKTOP_BOT: [f"--user-agent={util.DESKTOP_BOT_AGENT}"],
    }

    custom_user_agent = user_agent_map.get(config)

    browser = playwright_object.chromium.launch(headless=False, slow_mo=50, args=custom_user_agent)

    # creates a new page within the browser
    page = browser.new_page()

    return browser, page


def setup_mobile_user_crawler(playwright_object):
    browser = playwright_object.webkit.launch(headless=False, slow_mo=50)
    context = browser.new_context(
        **playwright_object.devices['Pixel 5']
    )

    page = context.new_page()
    return browser, page


def setup_mobile_bot_crawler(playwright_object):
    browser = playwright_object.webkit.launch(headless=False, slow_mo=50)
    pixel_5_bot = playwright_object.devices['Pixel 5'].copy()
    pixel_5_bot['user_agent'] = util.MOBILE_BOT_AGENT

    context = browser.new_context(
        **pixel_5_bot
    )

    page = context.new_page()
    return browser, page


def crawl(url_list, config, action_flag, referrer=None):
    print("\nCrawling in progress...")

    p = sync_playwright().start()

   
    if util.CONFIG_MOBILE_USER in config:
        browser, page = setup_mobile_user_crawler(p)
    
    elif util.CONFIG_MOBILE_BOT in config:
        browser, page = setup_mobile_bot_crawler(p)
    
    else:
        browser, page = setup_desktop_crawler(p, config)

    

    # Generate folders required for crawling
    base_folder_name = f"{util.CRAWLED_DATA_IDENTIFIER}_{config}"
    sub_folder_list = [
        util.CRAWLED_HTML_SCRIPT_FOLDER,
        util.CRAWLED_EMBEDDED_LINK_FOLDER,
        util.CRAWLED_PAGE_SCREENSHOT_FOLDER,
        util.CRAWLED_URL_FOLDER,
        util.CRAWLED_HTML_TAG_FOLDER,
        util.CRAWLED_REDIRECTION_FOLDER,
    ]

    crawler.generate_folder_for_crawling(base_folder_name, sub_folder_list)

    get_dataset(page, base_folder_name, url_list, referrer, action_flag)

    browser.close()
    p.stop()

    print("\nCrawling done...")


#crawl(["https://www.google.com/"], util.CONFIG_DESKTOP_USER, action_flag=True, referrer=util.FACEBOOK_REFERRER)

'''
def list_available_devices():
    with sync_playwright() as p:
        devices = p.devices

        print("Available Devices:")
        for device_name in devices.keys():
            print(f"- {device_name}")

list_available_devices()
'''