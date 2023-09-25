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



async def start_crawling(seed_url_list):
    print("Crawling in progress...\n")
    for url in seed_url_list:
        url_index = str(seed_url_list.index(url))
        time.sleep(random.randint(6, 12))

        print(f"------------------------------\nConfiguration: Referrer set\nUrl: {url}\n-----------------------------")
        await crawler.crawl(url, url_index, ref_flag=True)

        print(f"------------------------------\nConfiguration: No Referrer set\nUrl: {url}\n-----------------------------")
        await crawler.crawl(url, url_index, ref_flag=False)
    print("\nCrawling done...")



def start_analysing():
    analyzer.extract_and_analyse(ref_flag=True)
    analyzer.extract_and_analyse(ref_flag=False)
    analyzer.analysis_page_for_differences(util_def.FOLDER_DATASET_BASE)
    return



async def main(feeds_path):
    feeds = read_feeds_from_file(feeds_path)
    await start_crawling(feeds)
    start_analysing()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply path to feeds file.")
    parser.add_argument("file_path", help="Path to the feeds file")

    args = parser.parse_args()
    asyncio.run(main(args.file_path))