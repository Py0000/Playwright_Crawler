import asyncio
import argparse
import aiohttp
from playwright.async_api import async_playwright
from aiohttp import ClientTimeout
import queue
import threading

import analyzer
import crawler_main as crawler
import util_def

async def initialize_playwright_object_browser():
    async with async_playwright() as playwright_obj:
        return playwright_obj


async def cleanup_playwright_object_browser(playwright_obj):
    if playwright_obj:
        await playwright_obj.stop()


async def start_crawling(browser, feed, dataset_folder_name):
    seed_url = feed

    print("Crawling in progress...")
    print(f"\n------------------------------\nConfiguration: Referrer set\nUrl: {seed_url}\n-----------------------------")
    await crawler.crawl(browser, seed_url, dataset_folder_name, ref_flag=True)

    print(f"\n------------------------------\nConfiguration: No Referrer set\nUrl: {seed_url}\n-----------------------------")
    await crawler.crawl(browser, seed_url, dataset_folder_name, ref_flag=False)
    print("\nCrawling done...")



def start_analysing(dataset_folder_name, analyzed_data_folder_name):
    analyzer.extract_and_analyse(dataset_folder_name, analyzed_data_folder_name, ref_flag=True)
    analyzer.extract_and_analyse(dataset_folder_name, analyzed_data_folder_name, ref_flag=False)
    analyzer.analysis_page_for_differences(dataset_folder_name, analyzed_data_folder_name)
    return



OPENPHISH_FEEDS_URL = "https://opfeeds.s3-us-west-2.amazonaws.com/OPBL/phishing_blocklist.txt"
feeds_queue = queue.Queue()

async def fetch_openphish_feeds():
    print("Fetching feeds")
    timeout = ClientTimeout(total=300)
    while True:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get(OPENPHISH_FEEDS_URL) as response:
                    if response.status == 200:
                        feeds = await response.text()
                        urls = feeds.splitlines()
                        for url in urls:  
                            feeds_queue.put(url)
                        feeds_path = "feeds/urls/openphish_feeds.txt"
                        with open(feeds_path, 'a') as file:
                            file.write(feeds)
                    await asyncio.sleep(300)  # waits for 5 minutes before the next fetch
                    
            except Exception as e:
                print("Error fetching feeds from url: ", e)
                await asyncio.sleep(300) # waits for 5 minutes before the next fetch



async def process_feeds_from_queue(folder_name, browser):
    while True:
        if not feeds_queue.empty():
            print("Processing feeds")
            feed_to_process = feeds_queue.get()
            await process_current_feed(feed_to_process, folder_name, browser)
            feeds_queue.task_done()
        else:
            print("No feeds")
            await asyncio.sleep(300)  # Wait for 5 minute before checking the queue again




async def process_current_feed(feed, folder_name, browser):
    dataset_folder_name = f"{util_def.FOLDER_DATASET_BASE}_{folder_name}"
    analyzed_data_folder_name = f"{util_def.FOLDER_ANALYSIS_BASE}_{folder_name}"

    await start_crawling(browser, feed, dataset_folder_name)
    # start_analysing(dataset_folder_name, analyzed_data_folder_name)


def run_fetch_openphish_feeds():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_openphish_feeds())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder name.")
    parser.add_argument("folder_name", help="Name of the folder")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    p = loop.run_until_complete(initialize_playwright_object_browser())
    win_chrome_v116_user_agent = [f"--user-agent={util_def.USER_USER_AGENT_WINDOWS_CHROME}"]
    browser = loop.run_until_complete(p.chromium.launch(headless=True, args=win_chrome_v116_user_agent))

    fetch_thread = threading.Thread(target=run_fetch_openphish_feeds)
    fetch_thread.start()
    
    loop.run_until_complete(process_feeds_from_queue(args.folder_name, browser))

    fetch_thread.join()  
    loop.run_until_complete(browser.close())
    loop.run_until_complete(cleanup_playwright_object_browser(p))
    