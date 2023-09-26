import time
import random
import asyncio
import argparse

import analyzer
import crawler_main as crawler
import util_def

def read_feeds_from_file(feed_path):
    urls = []
    with open(feed_path, "r") as f:
        for line in f:
            urls.append(line.strip())
    return urls



async def start_crawling(seed_url_list, folder_name):
    print("Crawling in progress...\n")
    for url in seed_url_list:
        url_index = str(seed_url_list.index(url))
        if url_index != "0":
            time.sleep(random.randint(6, 12))

        print(f"------------------------------\nConfiguration: Referrer set\nUrl: {url}\n-----------------------------")
        await crawler.crawl(url, url_index, folder_name, ref_flag=True)

        print(f"------------------------------\nConfiguration: No Referrer set\nUrl: {url}\n-----------------------------")
        await crawler.crawl(url, url_index, folder_name, ref_flag=False)
    print("\nCrawling done...")



def start_analysing(folder_name):
    analyzer.extract_and_analyse(folder_name, ref_flag=True)
    analyzer.extract_and_analyse(folder_name, ref_flag=False)
    analyzer.analysis_page_for_differences(f"{util_def.FOLDER_DATASET_BASE}_{folder_name}")
    return



async def main(feeds_path, folder_name):
    feeds = read_feeds_from_file(feeds_path)
    await start_crawling(feeds, folder_name)
    start_analysing(folder_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply path to feeds file.")
    parser.add_argument("feeds_path", help="Path to the feeds file")
    parser.add_argument("folder_name", help="Name of the folder")

    args = parser.parse_args()
    asyncio.run(main(args.feeds_path, args.folder_name))