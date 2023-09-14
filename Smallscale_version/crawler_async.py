import base64 
import hashlib
import os
import random
import time

from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup

import crawler_certificate_extractor as certificate_extractor
import crawler_dns_extractor as dns_extractor
import crawler_utilities
import crawler_support
import util
import util_def


async def set_page_referrer(page, ref_flag, actual_url, is_embedded):
    if is_embedded:
        referrer = actual_url if ref_flag != util_def.NO_REF else None
    else:
        if ref_flag == util_def.NO_REF:
            referrer = None
        elif ref_flag == util_def.SELF_REF:
            referrer = actual_url
        else: 
            referrer = util_def.REFERRER_MAP.get(ref_flag)
    
    await page.set_extra_http_headers({"Referer": referrer})


async def get_server_side_data(p, device_conf, ref_flag, act_flag, folder_path, url):
    custom_user_agent = util_def.DESKTOP_USER_AGENT_MAP.get(device_conf)
    browser = await p.chromium.launch(headless=True, args=custom_user_agent)
    context = await browser.new_context()
    page = await context.new_page()
    await set_page_referrer(page, ref_flag, url, is_embedded=False)

    try:
        # Ensure that the routing function is also asynchronous
        await page.route('**/*', lambda route, request: 
                route.abort() if 'script' in request.resource_type else route.continue_())
        await page.goto(url)
        await crawler_utilities.check_and_execute_user_actions(act_flag, page)
        await crawler_utilities.wait_for_page_to_load(page, act_flag)
        await crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_BEF_FILE)
        server_html_script = await page.content()
        soup = BeautifulSoup(server_html_script, "lxml")
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_BEF_FILE, soup.prettify())
        crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_BEF_FILE)
    
    except Exception as e:
        crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_BEF_FILE, f"Error occurred for url: {url}\n{e}")
    
    finally:
        await page.close()
        await context.close()
        await browser.close()


async def get_client_side_script(page, folder_path):
    client_side_scripts = await page.evaluate(crawler_utilities.client_side_scripts_injection_code)

    # Format client-side scripts for better readability
    # Create a dictionary to store the client-side script data
    script_data = {}
    for index, script in enumerate(client_side_scripts):
        script_data[f'script_{index + 1}'] = script
    
    # Save data to a JSON file
    crawler_support.save_client_side_script(folder_path, script_data)



async def crawl(device_conf, ref_flag, act_flag, url, index):
    # Folders & Files for storing data
    util.generate_crawling_base_folders(device_conf, ref_flag, act_flag)
    folder_path = util.generate_crawling_folder_for_url(device_conf, ref_flag, act_flag, index)
    har_network_log_file = os.path.join(folder_path, util_def.NETWORK_FILE_BEFORE)

    async with async_playwright() as p:
        custom_user_agent = util_def.DESKTOP_USER_AGENT_MAP.get(device_conf)
        browser = await p.chromium.launch(headless=True, args=custom_user_agent)
        context = await browser.new_context(record_har_path=har_network_log_file)
        page = await context.new_page()
        await set_page_referrer(page, ref_flag, url, is_embedded=False)

        certificate_extractor.extract_certificate_info(url, folder_path)
        dns_extractor.extract_dns_records(url, folder_path)
        await get_server_side_data(p, device_conf, ref_flag, act_flag, folder_path, url)

        try:
            captured_events = []
            client = await page.context.new_cdp_session(page)
            await client.send("Network.enable")

            async def capture_response(payload):
                url = payload['response']['url']
                # Check if the response has any content
                if payload['response']['status'] in [204, 304]:
                    return
                
                try:
                    response_body = await client.send("Network.getResponseBody", {"requestId": payload['requestId']})
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
                    if "Protocol error (Network.getResponseBody)" in str(e):
                        pass
                    else:
                        print(e)
            
            async def capture_request(payload):
                captured_event = payload
                #requestId = payload["requestId"]
                #cookies = client.send("Network.getCookies", {"requestId": requestId})
                #captured_event["cookies"] = cookies
                captured_events.append(captured_event)
            
            client.on("Network.requestWillBeSent", capture_request)
            client.on("Network.responseReceived", capture_response)

            await page.goto(url, wait_until="networkidle")
            await crawler_utilities.wait_for_page_to_load(page, act_flag)

            await crawler_utilities.check_and_execute_user_actions(act_flag, page)
            await crawler_utilities.get_screenshot(page, folder_path, util_def.SCREENSHOT_FILE)
            html_content = await page.content()
            soup = BeautifulSoup(html_content, "lxml")
            crawler_support.get_all_html_tags(folder_path, soup, util_def.HTML_TAG_FILE)
            visited_url = page.url
            crawler_support.detect_redirection(folder_path, visited_url, url)
            crawler_support.save_crawled_url(folder_path, visited_url)
            embedded_file_path = await crawler_support.extract_links(folder_path, soup, page, visited_url)
            await get_client_side_script(page, folder_path)

            print("Actual url: ", url)
            print("Url visited: ", visited_url)
            print("User-Agent:", await page.evaluate('''() => window.navigator.userAgent'''))
            print(f"Referrer: {await page.evaluate('''() => document.referrer''')}")

            content = soup.prettify()
            if content is not None:
                crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, content)
        
        except Exception as e:
            crawler_support.save_html_script(folder_path, util_def.HTML_SCRIPT_FILE, f"Error occurred for url: {url}\n{e}")
            crawler_support.save_crawled_url(folder_path, util_def.ERROR_URL_FLAG)
        
        finally:
            crawler_support.save_more_detailed_network_logs(folder_path, captured_events)
            await page.close()
            await context.close()
            await browser.close()
            await p.stop()