from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

import os 

import crawler_certificate_extractor as certificate_extractor
import crawler_dns_extractor as dns_extractor
import util
import util_def 

async def set_page_referrer(page, ref_flag, to_visit_url):
    referrer = to_visit_url if ref_flag else None 
    await page.set_extra_http_headers({"Referer": referrer})



async def crawl(ref_flag, url, url_hash):
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

        cert_extraction_status = certificate_extractor.extract_certificate_info(url, folder_path)
        dns_extraction_status = dns_extractor.extract_dns_records(url, folder_path)