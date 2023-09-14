import base64 
import hashlib
import os
import random
import time

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import crawler_certificate_extractor as certificate_extractor
import crawler_dns_extractor as dns_extractor
import crawler_detail_network_extractor as network_extractor
import crawler_utilities
import crawler_support
import util
import util_def

def set_page_referrer(page, ref_flag, actual_url, is_embedded):
    if is_embedded:
        referrer = actual_url if ref_flag != util_def.NO_REF else None
    else:
        if ref_flag == util_def.NO_REF:
            referrer = None
        elif ref_flag == util_def.SELF_REF:
            referrer = actual_url
        else: 
            referrer = util_def.REFERRER_MAP.get(ref_flag)
    
    page.set_extra_http_headers({"Referer": referrer})


def get_server_side_data(p, device_conf, ref_flag, act_flag, folder_path, url):
    custom_user_agent = util_def.DESKTOP_USER_AGENT_MAP.get(device_conf)
    browser = p.chromium.launch(headless=True, args=custom_user_agent)
    context = browser.new_context()
    page = context.new_page()
    set_page_referrer(page, ref_flag, url, is_embedded=False)

    try:
        page.route('**/*', lambda route, request: 
                route.abort() if 'script' in request.resource_type else route.continue_())
        page.goto(url)
        crawler_utilities.check_and_execute_user_actions(act_flag, page)
        crawler_utilities.wait_for_page_to_load(page, act_flag)
        crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_BEF_FILE)
        server_html_script = page.content()
        soup = BeautifulSoup(server_html_script, "lxml")
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_BEF_FILE, soup.prettify())
        crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_BEF_FILE)
    
    except Exception as e:
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_BEF_FILE, f"Error occurred for url: {url}\n{e}")
    
    finally:
        page.close()
        context.close()
        browser.close()




def get_client_side_script(page, folder_path):
    client_side_scripts = page.evaluate(crawler_utilities.client_side_scripts_injection_code)

    # Format client-side scripts for better readability
    # Create a dictionary to store the client-side script data
    script_data = {}
    for index, script in enumerate(client_side_scripts):
        script_data[f'script_{index + 1}'] = script
    
    # Save data to a JSON file
    crawler_support.save_client_side_script(folder_path, script_data)



"""
def scrape_one_level_deeper(p, device_conf, ref_flag, act_flag, browser, embedded_path, base_index):
    url_list = crawler_support.get_level_one_embedded_link(embedded_path)

    for url in url_list:
        embedded_url_index = url_list.index(url)
        file_index = f"{base_index}-{embedded_url_index}"
        folder_path = util.generate_crawling_folder_for_url(device_conf, ref_flag, act_flag, file_index)
        har_network_log_file = os.path.join(folder_path, util_def.NETWORK_FILE_BEFORE)
        context = browser.new_context(record_har_path=har_network_log_file)
        page = context.new_page()
        set_page_referrer(page, ref_flag, url, is_embedded=True)

        certificate_extractor.extract_certificate_info(url, folder_path)
        dns_extractor.extract_dns_records(url, folder_path)
        get_server_side_data(p, device_conf, ref_flag, act_flag, folder_path, url)
    

        try:
            captured_events = []  # List to store the captured events
            client = page.context.new_cdp_session(page) # Create a CDP session for the page
            client.send("Network.enable") # Enable the Network domain to receive network-related events

            def capture_response(payload):
                url = payload['response']['url']
                # Check if the response has any content
                if payload['response']['status'] in [204, 304]:
                    return
                
                page.wait_for_timeout(500) # Introduce a small delay
                response_body = client.send("Network.getResponseBody", {"requestId": payload['requestId']})
                mime_type = payload['response']['mimeType']
                data_folder_path = crawler_support.get_detailed_network_response_data_path(folder_path)
                file_name = os.path.join(data_folder_path, f"{hashlib.sha256(url.encode()).hexdigest()}")

                # Decode base64 if needed
                if response_body['base64Encoded']:
                    decoded_data = base64.b64decode(response_body['body'])
                else:
                    decoded_data = response_body['body']
                
                if "html" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".html", decoded_data)
                elif "xml" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".xml", decoded_data)
                elif "json" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".json", decoded_data)
                elif "javascript" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".js", decoded_data)
                elif "css" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".css", decoded_data)
                elif "image" in mime_type:
                    with open(file_name + ".png", "wb") as f:
                        f.write(decoded_data)
                elif "font/woff2" in mime_type:
                    with open(file_name + ".woff2", "wb") as f:
                        f.write(decoded_data)
                elif "text" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".txt", decoded_data)
                else:
                    # Default: save as binary
                    with open(file_name + ".bin", "wb") as f:
                        f.write(decoded_data)
                
            def capture_request(payload):
                captured_event = payload
                #requestId = payload["requestId"]
                #cookies = client.send("Network.getCookies", {"requestId": requestId})
                #captured_event["cookies"] = cookies
                captured_events.append(captured_event)
            
            # obtain the network request
            client.on("Network.requestWillBeSent", capture_request)
            client.on("Network.responseReceived", capture_response)

            page.goto(url)
            crawler_utilities.wait_for_page_to_load(page, act_flag)

            crawler_utilities.check_and_execute_user_actions(act_flag, page)
            crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_FILE)
            html_content = page.content()
            soup = BeautifulSoup(html_content, "lxml")
            crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_FILE)
            visited_url = page.url
            crawler_support.detect_redirection(folder_path, visited_url, url)
            crawler_support.save_crawled_url(folder_path, visited_url)
            get_client_side_script(page, folder_path)

            print("Actual url: ", url)
            print("Url visited: ", visited_url)
            print("User-Agent:", page.evaluate('''() => window.navigator.userAgent'''))
            print(f"Referrer: {page.evaluate('''() => document.referrer''')}\n")

            content = soup.prettify()
            if content is not None:
                crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, content)
            
        except Exception as e:
            crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, f"Error occurred for url: {url}\n{e}")
            crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
        
        finally:
            page.close()
            context.close()
            time.sleep(random.randint(5, 10))
"""


def crawl(device_conf, ref_flag, act_flag, url, index):
    # Folders & Files for storing data
    util.generate_crawling_base_folders(device_conf, ref_flag, act_flag)
    folder_path = util.generate_crawling_folder_for_url(device_conf, ref_flag, act_flag, index)
    har_network_log_file = os.path.join(folder_path, util_def.NETWORK_FILE_BEFORE)

    # Create the playwright object, browser, context & page object
    # Set the user_agent in the browser object for desktop crawler
    p = sync_playwright().start()
    custom_user_agent = util_def.DESKTOP_USER_AGENT_MAP.get(device_conf)
    browser = p.chromium.launch(headless=True, args=custom_user_agent)
    context = browser.new_context(record_har_path=har_network_log_file)
    page = context.new_page()
    set_page_referrer(page, ref_flag, url, is_embedded=False)

    certificate_extractor.extract_certificate_info(url, folder_path)
    dns_extractor.extract_dns_records(url, folder_path)
    get_server_side_data(p, device_conf, ref_flag, act_flag, folder_path, url)

    try:
        captured_events = []  # List to store the captured events
        client = page.context.new_cdp_session(page) # Create a CDP session for the page
        client.send("Network.enable") # Enable the Network domain to receive network-related events

        def capture_response(payload):
            url = payload['response']['url']
            # Check if the response has any content
            if payload['response']['status'] in [204, 304]:
                return
            
            page.wait_for_timeout(500) # Introduce a small delay
            try:
                response_body = client.send("Network.getResponseBody", {"requestId": payload['requestId']})
                mime_type = payload['response']['mimeType']
                data_folder_path = crawler_support.get_detailed_network_response_data_path(folder_path)
                file_name = os.path.join(data_folder_path, f"{hashlib.sha256(url.encode()).hexdigest()}")

                # Decode base64 if needed
                if response_body['base64Encoded']:
                    decoded_data = base64.b64decode(response_body['body'])
                else:
                    decoded_data = response_body['body']
                
                if "html" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".html", decoded_data)
                elif "xml" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".xml", decoded_data)
                elif "json" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".json", decoded_data)
                elif "javascript" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".js", decoded_data)
                elif "css" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".css", decoded_data)
                elif "image" in mime_type:
                    with open(file_name + ".png", "wb") as f:
                        f.write(decoded_data)
                elif "font/woff2" in mime_type:
                    with open(file_name + ".woff2", "wb") as f:
                        f.write(decoded_data)
                elif "text" in mime_type:
                    crawler_support.save_decoded_file_data(file_name + ".txt", decoded_data)
                else:
                    # Default: save as binary
                    with open(file_name + ".bin", "wb") as f:
                        f.write(decoded_data)
            
            except Exception as e:
                print("No response that correspond to the requestId")
            
        def capture_request(payload):
            captured_event = payload
            #requestId = payload["requestId"]
            #cookies = client.send("Network.getCookies", {"requestId": requestId})
            #captured_event["cookies"] = cookies
            captured_events.append(captured_event)
        
        # obtain the network request
        client.on("Network.requestWillBeSent", capture_request)
        client.on("Network.responseReceived", capture_response)

        page.goto(url)
        crawler_utilities.wait_for_page_to_load(page, act_flag)

        crawler_utilities.check_and_execute_user_actions(act_flag, page)
        crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_FILE)
        html_content = page.content()
        soup = BeautifulSoup(html_content, "lxml")
        crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_FILE)
        visited_url = page.url
        crawler_support.detect_redirection(folder_path, visited_url, url)
        crawler_support.save_crawled_url(folder_path, visited_url)
        embedded_file_path = crawler_support.extract_links(folder_path, soup, page, visited_url)
        get_client_side_script(page, folder_path)

        print("Actual url: ", url)
        print("Url visited: ", visited_url)
        print("User-Agent:", page.evaluate('''() => window.navigator.userAgent'''))
        print(f"Referrer: {page.evaluate('''() => document.referrer''')}")

        content = soup.prettify()
        if content is not None:
            crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, content)

        """
        # Scrape embedded links
        scrape_one_level_deeper(p, device_conf, ref_flag, act_flag, browser, embedded_file_path, index)
        """

    except Exception as e:
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, f"Error occurred for url: {url}\n{e}")
        crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
    
    finally:
        crawler_support.save_more_detailed_network_logs(folder_path, captured_events)
        page.close()
        context.close()
        browser.close()
        p.stop()
        



