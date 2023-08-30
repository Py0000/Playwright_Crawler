import os
import random
import time

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import crawler_actions
import crawler_support
import util
import util_def


def wait_for_page_to_load(page, act_flag):
    if act_flag:
        crawler_actions.move_mouse_smoothly_top_left_bottom_right(page)
    
    try:
        # Wait for the page to load completely (wait for the load event)
        page.wait_for_load_state('domcontentloaded')
    except:
        pass

    try:
        page.wait_for_load_state('networkidle')
    except:
        pass


def setup_crawler_context(device_conf, ref_flag, act_flag, browser, device, index):
    # Generate a folder for each url to store data & obtain path to store har files
    folder_path = util.generate_crawling_folder_for_url(device_conf, ref_flag, act_flag, index)
    har_network_log_file = os.path.join(folder_path, util_def.NETWORK_FILE_BEFORE)

    # Create a new context and page for crawling
    referrer = util_def.GOOGLE_SEARCH_QUERY_REFERRER if ref_flag else None

    context = browser.new_context(record_har_path=har_network_log_file)

    is_mobile = util.mobile_configuration_checker(device_conf)
    if is_mobile:
        context = browser.new_context(**device, record_har_path=har_network_log_file)
        referrer = util_def.GOOGLE_REFERRER if ref_flag else None

    page = context.new_page()

    return folder_path, page, context, referrer


def crawl(device_conf, ref_flag, act_flag, url_list):
    print("\nCrawling in progress...\n")
    # Generate the base folders (i.e. 16 different combinations) to store data
    util.generate_crawling_base_folders()

    # Create the playwright object and browser object
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True, slow_mo=50)
    device = ""

    # Set the user_agent in the browser object for desktop crawler
    # Set the device for mobile crawler
    is_desktop_device = util.desktop_configuration_checker(device_conf)
    if is_desktop_device:
        custom_user_agent = util_def.DESKTOP_USER_AGENT_MAP.get(device_conf)
        browser = p.chromium.launch(headless=False, slow_mo=50, args=custom_user_agent)
    else:
        if device_conf == util_def.MOBILE_USER:
            device = p.devices['Pixel 5']
        else:
            device = p.devices['Pixel 5'].copy()
            device['user_agent'] = util_def.MOBILE_BOT_AGENT

    # Start crawling the urls to get the required dataset
    get_dataset(device_conf, ref_flag, act_flag, device, browser, url_list)

    browser.close()
    p.stop()
    print("\nCrawling done...")



def get_dataset(device_conf, ref_flag, act_flag, device, browser, url_list):
    # Store the list of urls that encountered errors
    error_list = []

    # Visits each url in the provided list
    for url in url_list:
        url_index = str(url_list.index(url))

        folder_path, page, context, referrer = setup_crawler_context(device_conf, ref_flag, act_flag, browser, device, url_index)

        try:
            content, embedded_path = scrape_content(device_conf, act_flag, page, folder_path, referrer, url, is_embedded=False)
            
            # Save obtained html if present
            if content is not None:
                crawler_support.save_html_script(folder_path, content)
                page.close()
                context.close()

                # Scrape embedded link
                referrer = url if referrer is not None else referrer
                error_list = scrape_one_level_deeper(device_conf, ref_flag, act_flag, browser, device, embedded_path, url, url_index, error_list)
        
        except Exception as e:
            crawler_support.save_html_script(folder_path, f"Error occurred for url: {url}\n{e}")
            crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
            error_list.append(url_index)
            page.close()
            context.close()
            continue

        time.sleep(random.randint(10, 20))



def scrape_one_level_deeper(device_conf, ref_flag, act_flag, browser, device, embedded_path, referrer, base_index, error_list):
    url_list = crawler_support.get_level_one_embedded_link(embedded_path)

    for url in url_list:
        embedded_url_index = url_list.index(url)
        file_index = f"{base_index}-{embedded_url_index}"
        folder_path, page, context, _ = setup_crawler_context(device_conf, ref_flag, act_flag, browser, device, file_index)
        try:
            content, _ = scrape_content(device_conf, act_flag, page, folder_path, referrer, url, is_embedded=True)

            if content is not None:
                crawler_support.save_html_script(folder_path, content)
                page.close()
                context.close()

        except Exception as e:
            crawler_support.save_html_script(folder_path, f"Error occurred for url: {url}\n{e}")
            crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
            error_list.append(file_index)
            page.close()
            context.close()
            continue

    time.sleep(random.randint(5, 10))
            
    return error_list        



def scrape_content(device_conf, act_flag, page, folder_path, ref_url, actual_url, is_embedded):
    if ref_url is not None:
        # set referrer for mobile crawler
        page.set_extra_http_headers({"Referer": ref_url})
        
        page.goto(actual_url)
    
    wait_for_page_to_load(page, act_flag)

    # get the html script and embedded links in the script
    return get_html_content(device_conf, act_flag, page, folder_path, actual_url, is_embedded)



def get_html_content(device_conf, act_flag, page, folder_path, actual_url, is_embedded):
    # Perform any user-actions if needed
    check_and_execute_user_actions(device_conf, act_flag, page)

    # Saves the full page screenshot 
    get_screenshot(page, folder_path)

    check_and_execute_scroll(page, act_flag)

    ### Might need to get page ss before csr

    # Gets the html content 
    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    visited_url = page.url

    # Checks if the visited url is the same as the provided url
    crawler_support.detect_redirection(folder_path, visited_url, actual_url)

    # Logs the crawled url for future usage
    crawler_support.save_crawled_url(folder_path, visited_url)

    # Gets embedded link (to be use for further crawling if needed)
    embedded_file_path = ""
    if not is_embedded:
        embedded_file_path = crawler_support.extract_links(folder_path, soup, page, visited_url)
    
    # Extract all the uncommon html_tags used
    crawler_support.get_all_html_tags(folder_path, soup)

    # Save all client-side scripts
    get_client_side_script(page, folder_path)

    print("Actual url: ", actual_url)
    print("Url visited: ", visited_url)
    print("User-Agent:", page.evaluate('''() => window.navigator.userAgent'''))
    print(f"Referrer: {page.evaluate('''() => document.referrer''')}\n")

    return soup.prettify(), embedded_file_path


def get_client_side_script(page, folder_path):
    client_side_scripts = page.evaluate(crawler_support.client_side_scripts_injection_code)

    # Format client-side scripts for better readability
    # Create a dictionary to store the client-side script data
    script_data = {}
    for index, script in enumerate(client_side_scripts):
        script_data[f'script_{index + 1}'] = script
    
    # Save data to a JSON file
    crawler_support.save_client_side_script(folder_path, script_data)




def check_and_execute_user_actions(device_conf, act_flag, page):
    if not act_flag:
        pass
    else:
        if util.desktop_configuration_checker(device_conf):
            crawler_actions.desktop_user_mouse_movement(page)
        else:
            crawler_actions.mobile_user_hand_gesture(page)



def check_and_execute_scroll(page, act_flag):
    if act_flag:
        crawler_actions.page_scroll(page)
    else:
        pass



def get_screenshot(page, folder_path):
    path = os.path.join(folder_path, util_def.SCREENSHOT_FILE)
    crawler_support.save_screenshot(page, path)
    print("Screenshot Captured...")


crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=True, url_list=["https://www.youtube.com"])