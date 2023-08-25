import time
import random

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import configurations
import crawler_support
import interception
import user_actions
import definitions
import util 

def wait_for_page_to_load(page, action_flag):
    if action_flag:
        user_actions.move_mouse_smoothly_top_left_bottom_right(page)
    
    try:
        # Wait for the page to load completely (wait for the load event)
        page.wait_for_load_state('domcontentloaded')
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



def check_and_execute_user_actions(base_folder_name, action_flag, page):
    if not action_flag:
        pass
    else:
        if "desktop" in base_folder_name:
            user_actions.desktop_user_mouse_movement(page)
        if "mobile" in base_folder_name:
            user_actions.mobile_user_hand_gesture(page)



def check_and_execute_scroll(action_flag, page):
    if action_flag:
        user_actions.page_scroll(page)
    else:
        pass



def get_screenshot(page, base_folder_name, formatted_index, before_after_flag):
    screenshot_path = crawler_support.get_screenshot_file_path(base_folder_name, formatted_index, before_after_flag, is_full=False)
    full_screenshot_path = crawler_support.get_screenshot_file_path(base_folder_name, formatted_index, before_after_flag, is_full=True)
    user_actions.save_screenshot(page, screenshot_path, full_flag=False)
    user_actions.save_screenshot(page, full_screenshot_path, full_flag=True)
    print("Screenshot Captured...")



def get_client_side_script(page, base_folder_name, formatted_index):
    client_side_scripts = page.evaluate(interception.client_side_scripts_injection_code)

    # Format client-side scripts for better readability
    # Create a dictionary to store the client-side script data
    script_data = {}
    for index, script in enumerate(client_side_scripts):
        script_data[f'script_{index + 1}'] = script
    
    # Save data to a JSON file
    crawler_support.save_client_side_script(base_folder_name, script_data, formatted_index)



def get_before_client_side_rendering_data(page, base_folder_name, formatted_index):
    # Get the content before client-side rendering
    get_screenshot(page, base_folder_name, formatted_index, before_after_flag="before")
    before_render_content = page.content()
    before_render_soup = BeautifulSoup(before_render_content, "lxml")

    if before_render_soup is not None:
        crawler_support.save_html_script(base_folder_name, before_render_soup.prettify(), formatted_index, definitions.SUBFOLDER_BEFORE)
    
    else:
        crawler_support.save_html_script(base_folder_name, f"No content shown for {page.url}", formatted_index, definitions.SUBFOLDER_BEFORE)

    crawler_support.save_crawled_url(base_folder_name, page.url, definitions.SUBFOLDER_BEFORE)
    crawler_support.get_all_html_tags(base_folder_name, before_render_soup, formatted_index, definitions.SUBFOLDER_BEFORE)

    return page



def get_html_content(page, base_folder_name, formatted_index, actual_url, action_flag, embedded_flag):
    check_and_execute_user_actions(base_folder_name, action_flag, page)
    
    page = get_before_client_side_rendering_data(page, base_folder_name, formatted_index)
    get_client_side_script(page, base_folder_name, formatted_index)

    # Disable route interception to allow JavaScript execution
    page.unroute('**/*', interception.intercept_script_xhr_requests)
    wait_for_page_to_load(page, action_flag)

    # Setup and get network request after CSR
    interception.intercept_network_request(page, base_folder_name, formatted_index, definitions.SUBFOLDER_AFTER)

    get_screenshot(page, base_folder_name, formatted_index, definitions.SUBFOLDER_AFTER)
    check_and_execute_scroll(action_flag, page)

    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    scraped_url = page.url
    crawler_support.detect_redirection(base_folder_name, scraped_url, actual_url)
    crawler_support.save_crawled_url(base_folder_name, scraped_url, definitions.SUBFOLDER_AFTER)

    embedded_file_path = ""
    if not embedded_flag:
        embedded_file_path = crawler_support.get_embedded_links(base_folder_name, soup, page, actual_url, formatted_index)

    crawler_support.get_all_html_tags(base_folder_name, soup, formatted_index, definitions.SUBFOLDER_AFTER)

    print("Actual url: ", actual_url)
    print("Url visited: ", scraped_url)
    crawler_support.test_check_user_agent(page)
    crawler_support.test_check_referrer(page)

    return soup.prettify(), embedded_file_path



def scrape_content(page, base_folder_name, referer_url, actual_url, formatted_index, action_flag, embedded_flag):
    isDesktop = configurations.desktop_configuration_checker(base_folder_name)
    isMobile = configurations.mobile_configuration_checker(base_folder_name)

    if isDesktop and referer_url is not None:
        # If it is the seed url, visit google first
        # Then inject a javascript click-through to visit the seed url to ensure no empty referrer

        if not embedded_flag and referer_url == definitions.GOOGLE_SEARCH_QUERY_REFERRER:
            referer_url = referer_url + actual_url
            print("Google Referrer executed")
        
        # Set the referrer first
        page.goto(referer_url) 
        wait_for_page_to_load(page, action_flag)

        # Sets up route interception on the page. 
        # The '**/*' pattern matches all network requests. 
        # The intercept_requests function will be called whenever a request is made.
        page.route('**/*', interception.intercept_script_xhr_requests)

        # Setup and get network request before CSR
        interception.intercept_network_request(page, base_folder_name, formatted_index, definitions.SUBFOLDER_BEFORE)

        # Visit the actual webpage
        page.evaluate('window.location.href = "{}";'.format(actual_url))
    
    else: 
        if isMobile and referer_url is not None:
            page.set_extra_http_headers({"Referer": referer_url})
        
         # Sets up route interception on the page. 
        # The '**/*' pattern matches all network requests. 
        # The intercept_requests function will be called whenever a request is made.
        page.route('**/*', interception.intercept_script_xhr_requests)

        # Setup and get network request before CSR
        interception.intercept_network_request(page, base_folder_name, formatted_index, definitions.SUBFOLDER_BEFORE)

        page.goto(actual_url)

    wait_for_page_to_load(page, action_flag)
    return get_html_content(page, base_folder_name, formatted_index, actual_url, action_flag, embedded_flag)




def crawl_depth_one_embedded_links(page, embedded_link_path, index, error_list, base_folder_name, referrer, action_flag):
    url_list = crawler_support.get_level_one_embedded_link(embedded_link_path)

    for url in url_list:
        formatted_index_str = util.format_index_base_file_name(index)
        try:
            content, _ = scrape_content(page, base_folder_name, referrer, url, formatted_index_str, action_flag, embedded_flag=True)

            if content is not None:
                crawler_support.save_html_script(base_folder_name, content, formatted_index_str, definitions.SUBFOLDER_AFTER)
        
        except Exception as e:
            crawler_support.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str, definitions.SUBFOLDER_AFTER)
            crawler_support.save_crawled_url(base_folder_name, definitions.ERROR_URL_FLAG, definitions.SUBFOLDER_AFTER)
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
                crawler_support.save_html_script(base_folder_name, content, formatted_index_str, definitions.SUBFOLDER_AFTER)
                
                # Scrape embedded link
                referrer = url if referrer is not None else referrer
                #index, error_list = crawl_depth_one_embedded_links(page, embedded_path, index, error_list, base_folder_name, referrer, action_flag)
  
        except Exception as e:
            crawler_support.save_html_script(base_folder_name, f"Error occurred for url: {url}\n{e}", formatted_index_str, definitions.SUBFOLDER_AFTER)
            crawler_support.save_crawled_url(base_folder_name, definitions.ERROR_URL_FLAG, definitions.SUBFOLDER_AFTER)
            error_list.append(index)
            index += 1
            continue

        time.sleep(random.randint(5, 10))


def crawl(url_list, config, action_flag, referrer=None):
    print("\nCrawling in progress...")

    p = sync_playwright().start()
    browser, page = configurations.setup_configuration(p, config)

    # Generate base folders for crawling
    base_folder_name = f"{definitions.MAIN_CRAWLING_FOLDER}_{config}"
    sub_folder_list = [
        definitions.CRAWLED_HTML_SCRIPT_FOLDER,
        definitions.CRAWLED_EMBEDDED_LINK_FOLDER,
        definitions.CRAWLED_SCREENSHOT_FOLDER,
        definitions.CRAWLED_FULL_SCREENSHOT_FOLDER,
        definitions.CRAWLED_URL_FOLDER,
        definitions.CRAWLED_HTML_TAG_FOLDER,
        definitions.CRAWLED_REDIRECTION_FOLDER,
        definitions.CRAWLED_NETWORK_LOGS_FOLDER,
        definitions.CRAWLED_CLIENT_SIDE_SCRIPT_FOLDER,
    ]

    util.generate_folder_for_crawling(base_folder_name, sub_folder_list)
    get_dataset(page, base_folder_name, url_list, referrer, action_flag)

    browser.close()
    p.stop()

    print("\nCrawling done...")


# crawl(["https://www.google.com/", "https://www.youtube.com"], definitions.CONFIG_DESKTOP_USER, action_flag=True, referrer=definitions.GOOGLE_SEARCH_QUERY_REFERRER)