import time
import random
import asyncio
import argparse
import aiohttp
import queue

import analyzer
import crawler_main as crawler
import network_data_processor
import util_def


async def start_crawling(seed_url_list, dataset_folder_name):
    print("Crawling in progress...")
    for url in seed_url_list:
        url_index = str(seed_url_list.index(url))
        if url_index != "0":
            time.sleep(random.randint(6, 12))

        print(f"\n------------------------------\nConfiguration: Referrer set\nUrl: {url}\n-----------------------------")
        await crawler.crawl(url, url_index, dataset_folder_name, ref_flag=True)

        print(f"\n------------------------------\nConfiguration: No Referrer set\nUrl: {url}\n-----------------------------")
        await crawler.crawl(url, url_index, dataset_folder_name, ref_flag=False)
    print("\nCrawling done...")



def start_analysing(dataset_folder_name, analyzed_data_folder_name):
    analyzer.extract_and_analyse(dataset_folder_name, analyzed_data_folder_name, ref_flag=True)
    analyzer.extract_and_analyse(dataset_folder_name, analyzed_data_folder_name, ref_flag=False)
    analyzer.analysis_page_for_differences(dataset_folder_name, analyzed_data_folder_name)
    return



OPENPHISH_FEEDS_URL = "https://opfeeds.s3-us-west-2.amazonaws.com/OPBL/phishing_blocklist.txt"
feeds_queue = queue.Queue()

async def fetch_openphish_feeds():
    async with aiohttp.ClientSession() as session:
        async with session.get(OPENPHISH_FEEDS_URL) as response:
            if response.status == 200:
                feeds = await response.text()
                feeds_queue.put(feeds)



async def process_feeds_from_queue(folder_name):
    while True:
        if not feeds_queue.empty():
            feed_to_process = feeds_queue.get()
            # assuming your main function takes feed content directly
            await process_current_feed(feed_to_process, folder_name)
            feeds_queue.task_done()
        else:
            await asyncio.sleep(300)  # Wait for 5 minute before checking the queue again




async def process_current_feed(feed, folder_name):
    dataset_folder_name = f"{util_def.FOLDER_DATASET_BASE}_{folder_name}"
    analyzed_data_folder_name = f"{util_def.FOLDER_ANALYSIS_BASE}_{folder_name}"

    await start_crawling(feed, dataset_folder_name)
    network_data_processor.start_network_processing(dataset_folder_name)
    # start_analysing(dataset_folder_name, analyzed_data_folder_name)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder name.")
    parser.add_argument("folder_name", help="Name of the folder")

    # Task to continuously fetch feeds
    fetch_task = asyncio.create_task(fetch_openphish_feeds())

    # Task to process feeds from the queue
    args = parser.parse_args()
    process_task = asyncio.create_task(process_feeds_from_queue(args.folder_name))

    # Run both tasks
    asyncio.run(asyncio.gather(fetch_task, process_task))