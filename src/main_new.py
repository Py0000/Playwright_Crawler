import asyncio
import argparse
import aiohttp

from playwright.async_api import async_playwright

import analyzer
import crawler_main as crawler
import util_def

feeds_queue = asyncio.Queue()
OPENPHISH_FEEDS_URL = "https://opfeeds.s3-us-west-2.amazonaws.com/OPBL/phishing_blocklist.txt"



async def fetch_openphish_feeds(feeds_filename):
    print("Fetching feeds")
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(OPENPHISH_FEEDS_URL) as response:
                    if response.status == 200:
                        feeds = await response.text()
                        urls = feeds.splitlines()
                        for url in urls:  
                            await feeds_queue.put(url)
                        feeds_path = f"feeds/urls/openphish_feeds_{feeds_filename}.txt"
                        with open(feeds_path, 'a') as file:
                            file.write(feeds)
                    else:
                         print(f"Error fetching feeds. HTTP status: {response.status}")
            
            except Exception as e:
                print("Error fetching feeds from url: ", e)

            finally:
                await asyncio.sleep(300) # waits for 1 minute before the next fetch



async def start_crawling(feed, dataset_folder_name):
    seed_url = feed
    try:
        async with async_playwright() as p:
            win_chrome_v116_user_agent = [f"--user-agent={util_def.USER_USER_AGENT_WINDOWS_CHROME}"]
            browser = await p.chromium.launch(headless=True, args=win_chrome_v116_user_agent)

            print("Crawling in progress...")
            print(f"\n------------------------------\nConfiguration: Referrer set\nUrl: {seed_url}\n-----------------------------")
            await crawler.crawl(browser, seed_url, dataset_folder_name, ref_flag=True)

            print(f"\n------------------------------\nConfiguration: No Referrer set\nUrl: {seed_url}\n-----------------------------")
            await crawler.crawl(browser, seed_url, dataset_folder_name, ref_flag=False)
            print("\nCrawling done...")

            if browser:
                await browser.close()
    except Exception as e:
        print("Error with Playwright: ", e)


async def process_current_feed(feed, folder_name):
    dataset_folder_name = f"{util_def.FOLDER_DATASET_BASE}_{folder_name}"
    await start_crawling(feed, dataset_folder_name)


async def process_feeds_from_queue(folder_name):
    while True:
        print("Processing feeds")
        feed_to_process = await feeds_queue.get()
        await process_current_feed(feed_to_process, folder_name)
        feeds_queue.task_done()


async def main(folder_name):
    await asyncio.gather(
        fetch_openphish_feeds(folder_name),
        process_feeds_from_queue(folder_name)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder name.")
    parser.add_argument("folder_name", help="Name of the folder")
    args = parser.parse_args()

    asyncio.run(main(args.folder_name))