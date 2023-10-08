from datetime import datetime
import hashlib
import os 
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

import crawler_actions
import crawler_certificate_extractor as certificate_extractor
import crawler_dns_extractor as dns_extractor
import crawler_utilities
import util
import util_def 

ERROR_MSG = "Error visiting page"

# Waits for page to complete loading 
async def wait_for_page_to_load(page):
    await crawler_actions.move_mouse_smoothly(page)
    try:
        # Wait for the page to load completely (wait for the dom contentload event)
        await page.wait_for_load_state('domcontentloaded')
    except:
        await page.wait_for_timeout(2000)

    try:
        # Wait for the page to no more network interaction
        await page.wait_for_load_state('networkidle')
    except:
        await page.wait_for_timeout(5000)


# Sets the playwright page referrer to the url provided if ref_flag is set.
# Otherwise, set it to None (i.e. Empty)
async def set_page_referrer(page, ref_flag, to_visit_url):
    if ref_flag:
        await page.set_extra_http_headers({"Referer": to_visit_url})


# Obtains the server-side data for the webpage
# Data retrieves includes: Page Screenshot, Page HTML Script
async def get_server_side_data(browser, ref_flag, folder_path, to_visit_url):
    # Intercept network requests
    async def block_external_resources_request(route, request):
        if request.resource_type != "document":
            await route.abort()
        else:
            await route.continue_()
    
    try:
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        await set_page_referrer(page, ref_flag, to_visit_url)

        # Ensure that the routing function is applied to all requests
        await page.route('**/*', block_external_resources_request)
        await page.goto(to_visit_url)
        server_move_status = await crawler_actions.execute_user_action(page)
        await wait_for_page_to_load(page)

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
        status = "Error visiting page"
        server_move_status = "Error visiting page"
        server_screenshot_status = "Error visiting page"
        server_html_tag = "Error visiting page"

    finally:
        await page.close()
        await context.close()
        return server_html_tag, status, server_move_status, server_screenshot_status


# Obtains all the client-side calls that is present in the page HTML Script
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


def obtain_certificate_info(visited_url, folder_path):
    try:
        # Obtains the TLS/SSL certificate info for the page
        cert_extraction_status = certificate_extractor.extract_certificate_info(visited_url, folder_path)
    except:
        cert_extraction_status = "Error retrieving certificate info"
    finally:
        return cert_extraction_status
        

def obtain_dns_records_info(visited_url, folder_path):
    try:
        # Obtains the DNS records info for the page
        dns_extraction_status = dns_extractor.extract_dns_records(visited_url, folder_path)
    except:
        dns_extraction_status = "Error retrieving dns info"
    finally:
        return dns_extraction_status        


# dataset_folder_name: refers to the name of the (base)folder to store the crawled data
async def crawl(browser, url, dataset_folder_name, ref_flag):
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    time_crawled = datetime.now()

    # Setup folders and paths required for data storage 
    base_folder_path = util.generate_base_folder_for_crawled_dataset(ref_flag, dataset_folder_name)
    folder_path = util.generate_folder_for_individual_url_dataset(url_hash, base_folder_path)
    har_network_path = os.path.join(folder_path, util_def.FOLDER_NETWORK_FRAGMENTS ,util_def.FILE_NETWORK_HAR)

    context = await browser.new_context(record_har_path=har_network_path, record_har_content="attach")
    page = await context.new_page()
    await set_page_referrer(page, ref_flag, url)
    
    main_http_status = "Not Visited"
    try:
        # Obtains the server-side view of the HTML Script and page screenshot 
        server_html_tag, server_html_status, server_move_status, server_screenshot_status = await get_server_side_data(browser, ref_flag, folder_path, url)

        # Global variable to track the last request time
        last_request_data = {"timestamp": None}

        # List. To hold network resquest made when visiting the page.
        captured_events = []
        
        # Function to capture and store all network requests made.
        async def capture_request(payload):
            captured_event = payload
            captured_events.append(captured_event)
            last_request_data["timestamp"] = datetime.now()
        
        async def check_for_timeout(client):
            await asyncio.sleep(5)
            
            # If there hasn't been a request for TIMEOUT_DURATION seconds
            last_request_time = last_request_data["timestamp"]
            if last_request_time is None or (datetime.now() - last_request_time).seconds >= 5:
                client.off("Network.requestWillBeSent", capture_request)
                print("No network requests for 5s, proceeding...")
        
        
        client = await page.context.new_cdp_session(page) # Utilize CDP to capture network requests.
        await client.send("Network.enable")
        asyncio.create_task(check_for_timeout(client))
        client.on("Network.requestWillBeSent", capture_request)

        response = await page.goto(url, timeout=10000)
        await wait_for_page_to_load(page)
        visited_url = page.url # See if url changes after visiting the page.
        if response:
            main_http_status = response.status

        client_move_status = await crawler_actions.execute_user_action(page) # Mimics user movements when visiting the page.
        client_screenshot_status = await crawler_utilities.save_screenshot(page, folder_path, util_def.FILE_SCREENSHOT_AFT)
        html_content = await page.content()
        soup = BeautifulSoup(html_content, "lxml")
        client_html_tag = crawler_utilities.get_unique_html_tags(soup)
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

        detailed_network_status = crawler_utilities.save_more_detailed_network_logs(folder_path, captured_events)
        
        cert_extraction_status = obtain_certificate_info(visited_url, folder_path)
        dns_extraction_status = obtain_dns_records_info(visited_url, folder_path)

        

    except Exception as e:
        crawler_utilities.save_html_script(folder_path, util_def.FILE_HTML_SCRIPT_AFT, f"Error occurred for url: {url}\n{e}")
        client_html_script_status = "Failed"

        visited_url = url
        server_move_status = ERROR_MSG
        server_html_status = ERROR_MSG
        server_screenshot_status = ERROR_MSG
        dns_extraction_status = ERROR_MSG
        cert_extraction_status = ERROR_MSG
        client_move_status = ERROR_MSG
        client_html_script_status = ERROR_MSG
        client_screenshot_status = ERROR_MSG
        client_client_side_script_status = ERROR_MSG
        detailed_network_status = ERROR_MSG
    
    finally:
        if page:
            await page.close()
        if context:
            await context.close()

        log_data = {
            "Url visited": visited_url,
            "Provided Url": url,
            "Has Url changed?": visited_url != url,
            "Status": main_http_status,
            "Provided Url Hash (in SHA-256)": url_hash,
            "Time crawled": time_crawled.strftime("%d/%m/%Y %H:%M:%S"),
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

        output_path = os.path.join(folder_path, util_def.FILE_CRAWL_LOG_INFO)
        util.save_data_to_json_format(output_path, log_data)

        # Generate a semaphore file to signal that it is ready to be sent to databse
        util.generate_semaphore_lock_file(folder_path)
