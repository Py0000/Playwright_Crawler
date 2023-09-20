import hashlib
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

import os 

import crawler_actions
import crawler_certificate_extractor as certificate_extractor
import crawler_dns_extractor as dns_extractor
import crawler_utilities
import util
import util_def 


# Waits for page to complete loading 
async def wait_for_page_to_load(page):
    await crawler_actions.move_mouse_smoothly(page)
    try:
        # Wait for the page to load completely (wait for the load event)
        await page.wait_for_load_state('domcontentloaded')
    except:
        await page.wait_for_timeout(2000)

    try:
        await page.wait_for_load_state('networkidle')
    except:
        await page.wait_for_timeout(5000)


# Sets the playwright page referrer to the url provided if ref_flag is set.
# Otherwise, set it to None (i.e. Empty)
async def set_page_referrer(page, ref_flag, to_visit_url):
    referrer = to_visit_url if ref_flag else None 
    await page.set_extra_http_headers({"Referer": referrer})


async def get_server_side_data(p, ref_flag, folder_path, to_visit_url):
    # Intercept network requests
    def block_external_resources_request(route, request):
        if request.resource_type != "document":
            route.abort()
        else:
            route.continue_()
    
    try:
        win_chrome_v116_user_agent = [f"--user-agent={util_def.USER_USER_AGENT_WINDOWS_CHROME}"]
        browser = await p.chromium.launch(headless=True, args=win_chrome_v116_user_agent)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        await set_page_referrer(page, ref_flag, to_visit_url)

        # Ensure that the routing function is applied to all requests
        await page.route('**/*', block_external_resources_request)
        await page.goto(to_visit_url)
        server_move_status = await crawler_actions.execute_user_action(page)
        wait_for_page_to_load(page)

        server_screenshot_status = await crawler_utilities.save_screenshot(page, folder_path, util_def.FILE_SCREENSHOT_BEF)
        server_html_script = await page.content()
        soup = BeautifulSoup(server_html_script, "lxml")
        crawler_utilities.save_html_script(folder_path, util_def.FILE_HTML_SCRIPT_BEF, soup.prettify())
        server_html_tag = crawler_utilities.get_unique_html_tags(soup)
        status = "Success"

    except Exception as e:
        crawler_utilities.save_html_script(
            folder_path, util_def.FILE_HTML_SCRIPT_BEF, f"Error occurred for url: {to_visit_url}\n{e}"
        )
        status = "Error"

    finally:
        await page.close()
        await context.close()
        await browser.close()
        return server_html_tag, status, server_move_status, server_screenshot_status



async def get_client_side_script(page, folder_path):
    try:
        client_side_scripts = await page.evaluate(crawler_utilities.client_side_scripts_injection_code)

        # Format client-side scripts for better readability
        # Create a dictionary to store the client-side script data
        script_data = {}
        for index, script in enumerate(client_side_scripts):
            script_data[f'script_{index + 1}'] = script
        
        # Save data to a JSON file
        crawler_utilities.save_client_side_script(folder_path, script_data)
        status = "Success"
    except:
        status = "Failed"
    finally:
        return status




async def crawl(url, ref_flag):
    # Generate sha256 hash for url
    url_hash = hashlib.sha256(visited_url.encode()).hexdigest()

    # Setup folders and paths required for data storage 
    util.generate_base_folder_for_crawled_dataset(ref_flag)
    folder_path = util.generate_folder_for_individual_url_dataset(ref_flag, url_hash)
    har_network_path = os.path.join(folder_path, util_def.FILE_NETWORK_HAR)

    async with async_playwright() as p:
        win_chrome_v116_user_agent = [f"--user-agent={util_def.USER_USER_AGENT_WINDOWS_CHROME}"]
        browser = await p.chromium.launch(headless=True, args=win_chrome_v116_user_agent)
        context = await browser.new_context(record_har_path=har_network_path)
        page = await context.new_page()
        await set_page_referrer(page, ref_flag, url)

        try:
            cert_extraction_status = certificate_extractor.extract_certificate_info(url, folder_path)
            dns_extraction_status = dns_extractor.extract_dns_records(url, folder_path)
            server_html_tag, server_html_status, server_move_status, server_screenshot_status = await get_server_side_data(p, ref_flag, folder_path, url)

            captured_events = []
            client = await page.context.new_cdp_session(page)
            await client.send("Network.enable")

            async def capture_request(payload):
                captured_event = payload
                captured_events.append(captured_event)

            async def capture_response(payload):
                url = payload['response']['url']
                # Check if the response has any content
                if payload['response']['status'] in [204, 304]:
                    return
                
                try:
                    response_body = await client.send("Network.getResponseBody", {"requestId": payload['requestId']})
                    mime_type = payload['response']['mimeType']
                    file_name = crawler_utilities.get_detailed_network_response_data_path(folder_path)
                    decoded_data = crawler_utilities.decode_network_response(response_body) # Decode base64 if needed
                    crawler_utilities.save_decoded_file_data(file_name, mime_type, decoded_data)
                except Exception as e:
                    if "Protocol error (Network.getResponseBody)" in str(e):
                        pass
                    else:
                        print(e)

            client.on("Network.requestWillBeSent", capture_request)
            client.on("Network.responseReceived", capture_response)

            await page.goto(url)
            await wait_for_page_to_load(page)
            visited_url = page.url

            client_move_status = await crawler_actions.execute_user_action(page)
            client_screenshot_status = await crawler_utilities.save_screenshot(page, folder_path, util_def.FILE_SCREENSHOT_AFT)
            html_content = await page.content()
            soup = BeautifulSoup(html_content, "lxml")
            client_html_tag = crawler_utilities.save_unique_html_tags(soup)
            crawler_utilities.save_unique_html_tags(folder_path, server_html_tag, client_html_tag)
            await crawler_utilities.extract_links(folder_path, soup, page, visited_url)
            client_client_side_script_status = await get_client_side_script(page, folder_path)
            
            user_agent = await page.evaluate('''() => window.navigator.userAgent''')
            referrer = await page.evaluate('''() => document.referrer''')
            print("Actual url: ", url)
            print("Url visited: ", visited_url)
            print("User-Agent:", user_agent)
            print(f"Referrer: {referrer}")

            content = soup.prettify()
            if content is not None:
                crawler_utilities.save_html_script(folder_path, util_def.FILE_HTML_SCRIPT_AFT, content)
            
            client_html_script_status = "Success"

        except Exception as e:
            crawler_utilities.save_html_script(folder_path, util_def.FILE_HTML_SCRIPT_AFT, f"Error occurred for url: {url}\n{e}")
            client_html_script_status = "Failed"
        
        finally:
            detailed_network_status = crawler_utilities.save_more_detailed_network_logs(folder_path, captured_events)
            await page.close()
            await context.close()
            await browser.close()
            await p.stop()

            log_data = {
                "Url visited": visited_url,
                "Provided Url": url,
                "Has Url changed?": visited_url != url,
                "Provided Url hash (sha256)": url_hash,
                "Certificate Extraction": cert_extraction_status,
                "DNS Records Extraction": dns_extraction_status,
                "Mouse moved when obtaining server-side data?": server_move_status,
                "Server-Side HTML script obtained?": server_html_status,
                "Server-side screenshot obtained?": server_screenshot_status,
                "Mouse moved when obtaining client-side data?": client_move_status,
                "Client-Side HTML script obtained?": client_html_script_status,
                "Client-side screenshot obtained?": client_screenshot_status,
                "Client-Side scripts obtained?":  client_client_side_script_status,
                "Network data saved?": detailed_network_status
            }

            log_output_path = os.path.join(os.getcwd(), folder_path, util_def.FILE_CRAWL_LOG_INFO)
            util.save_data_to_json_format(log_output_path, log_data)

