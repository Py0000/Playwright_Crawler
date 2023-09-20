import time
import random
import asyncio

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
        time.sleep(random.randint(6, 12))
        await crawler.crawl(url, ref_flag=True)
        await crawler.crawl(url, ref_flag=False)
    print("\nCrawling done...")



def start_analysing():
    return



async def main():
    feeds = read_feeds_from_file("feeds/phishing_feeds_180923.txt")
    await start_crawling(feeds)
    #start_analysing()


if __name__ == '__main__':
    asyncio.run(main())