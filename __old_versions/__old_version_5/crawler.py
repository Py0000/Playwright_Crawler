import os
import random
import time

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import crawler_certificate_extractor as certificate_extractor
import crawler_dns_extractor as dns_extractor
import crawler_utilities
import crawler_support
import util
import util_def


def setup_crawler_context(ref_flag, browser, folder_path):
    har_network_log_file = os.path.join(folder_path, util_def.NETWORK_FILE_BEFORE)
    referrer = util_def.GOOGLE_REFERRER if ref_flag else None
    context = browser.new_context(record_har_path=har_network_log_file)
    page = context.new_page()
    return page, context, referrer



def get_server_side_data(device_conf, ref_flag, act_flag, browser, folder_path, actual_url):
    print("Getting content from server-side...")
    context = browser.new_context()
    page = context.new_page()
    if ref_flag:
        referrer = util_def.GOOGLE_REFERRER if ref_flag else None
        page.set_extra_http_headers({"Referer": referrer})

    try:
        page.route('**/*', lambda route, request: 
                route.abort() if 'script' in request.resource_type else route.continue_())
        
        page.goto(actual_url)

        if act_flag:
            crawler_utilities.check_and_execute_user_actions(device_conf, act_flag, page)
        
        # Gets the html content 
        crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_BEF_FILE)
        server_html_script = page.content()
        soup = BeautifulSoup(server_html_script, "lxml")

        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_BEF_FILE, soup.prettify())
        crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_BEF_FILE)

    except Exception as e:
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_BEF_FILE, f"Error occurred for url: {actual_url}\n{e}")




def get_client_side_script(page, folder_path):
    client_side_scripts = page.evaluate(crawler_utilities.client_side_scripts_injection_code)

    # Format client-side scripts for better readability
    # Create a dictionary to store the client-side script data
    script_data = {}
    for index, script in enumerate(client_side_scripts):
        script_data[f'script_{index + 1}'] = script
    
    # Save data to a JSON file
    crawler_support.save_client_side_script(folder_path, script_data)




def capture_more_detailed_network_logs(page, act_flag):
    # List to store the captured events
    captured_events = []  
    
    # Create a CDP session for the page
    client = page.context.new_cdp_session(page)

    # Enable the Network domain to receive network-related events
    client.send("Network.enable")

    # Set up an event listener for requestWillBeSent
    def capture_request(payload):
        captured_event = payload
        cookies = client.send("Network.getCookies", {"requestId": payload["requestId"]})
        captured_event["cookies"] = cookies
        captured_events.append(captured_event)
    
    client.on("Network.requestWillBeSent", capture_request)
    crawler_utilities.wait_for_page_to_load(page, act_flag)

    return client, captured_events




def get_html_content(device_conf, act_flag, page, folder_path, actual_url, is_embedded):
    # Perform any user-actions if needed
    crawler_utilities.check_and_execute_user_actions(device_conf, act_flag, page)

    # Saves the full page screenshot 
    crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_FILE)

    crawler_utilities.check_and_execute_scroll(page, act_flag)

    # Gets the html content 
    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")
    visited_url = page.url
    
    # Gets embedded link (to be use for further crawling if needed)
    embedded_file_path = ""
    if not is_embedded:
        embedded_file_path = crawler_support.extract_links(folder_path, soup, page, visited_url)
    
    # Extract all the uncommon html_tags used
    crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_FILE)

    # Checks if the visited url is the same as the provided url
    crawler_support.detect_redirection(folder_path, visited_url, actual_url)
    
    # Logs the crawled url for future usage
    crawler_support.save_crawled_url(folder_path, visited_url)

    # Save all client-side scripts
    get_client_side_script(page, folder_path)

    print("Actual url: ", actual_url)
    print("Url visited: ", visited_url)
    print("User-Agent:", page.evaluate('''() => window.navigator.userAgent'''))
    print(f"Referrer: {page.evaluate('''() => document.referrer''')}\n")

    return soup.prettify(), embedded_file_path




def scrape_content(device_conf, act_flag, page, folder_path, ref_url, actual_url, is_embedded):
    if ref_url is not None:
        page.set_extra_http_headers({"Referer": ref_url})

    client, captured_events = capture_more_detailed_network_logs(page, act_flag)
    page.goto(actual_url)
    crawler_utilities.wait_for_page_to_load(page, act_flag)

    client.detach()
    crawler_support.save_more_detailed_network_logs(folder_path, captured_events)

    # get the html script and embedded links in the script
    return get_html_content(device_conf, act_flag, page, folder_path, actual_url, is_embedded)




def scrape_one_level_deeper(device_conf, ref_flag, act_flag, browser, embedded_path, referrer, base_index):
    url_list = crawler_support.get_level_one_embedded_link(embedded_path)

    for url in url_list:
        embedded_url_index = url_list.index(url)
        file_index = f"{base_index}-{embedded_url_index}"
        folder_path = util.generate_crawling_folder_for_url(device_conf, ref_flag, act_flag, file_index)
        page, context, referrer = setup_crawler_context(ref_flag, browser, folder_path)

        certificate_extractor.extract_certificate_info(url, folder_path)
        dns_extractor.extract_dns_records(url, folder_path)
        get_server_side_data(device_conf, ref_flag, act_flag, browser, folder_path, url)

        try:
            content, _ = scrape_content(device_conf, act_flag, page, folder_path, referrer, url, is_embedded=True)
            if content is not None:
                crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, content)
                page.close()
                context.close()

        except Exception as e:
            crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, f"Error occurred for url: {url}\n{e}")
            crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
            page.close()
            context.close()
            continue

        time.sleep(random.randint(5, 10))





def get_dataset(device_conf, ref_flag, act_flag, browser, url, index):
    folder_path = util.generate_crawling_folder_for_url(device_conf, ref_flag, act_flag, index)
    page, context, referrer = setup_crawler_context(ref_flag, browser, folder_path)

    certificate_extractor.extract_certificate_info(url, folder_path)
    dns_extractor.extract_dns_records(url, folder_path)
    get_server_side_data(device_conf, ref_flag, act_flag, browser, folder_path, url)

    try:
        content, embedded_path = scrape_content(device_conf, act_flag, page, folder_path, referrer, url, is_embedded=False)
        # Save obtained html if present
        if content is not None:
            crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, content)
            page.close()
            context.close()
        """
        # Scrape embedded link
        referrer = url if ref_flag else referrer
        scrape_one_level_deeper(device_conf, ref_flag, act_flag, browser, embedded_path, referrer, index)
        """     
    except Exception as e:
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, f"Error occurred for url: {url}\n{e}")
        crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
        page.close()
        context.close()
       



def crawl(device_conf, ref_flag, act_flag, url, index):
    util.generate_crawling_base_folders(device_conf, ref_flag, act_flag)

    # Create the playwright object and browser object
    p = sync_playwright().start()
    
    # Set the user_agent in the browser object for desktop crawler
    custom_user_agent = util_def.DESKTOP_USER_AGENT_MAP.get(device_conf)
    browser = p.chromium.launch(headless=True, args=custom_user_agent)

    # Start crawling the urls to get the required dataset
    get_dataset(device_conf, ref_flag, act_flag, browser, url, index)
    
    browser.close()
    p.stop()