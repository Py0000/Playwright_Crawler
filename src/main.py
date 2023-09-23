import time
import random
import asyncio

import analyzer
import crawler_main as crawler

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
    return



async def main():
    feeds = read_feeds_from_file("feeds/phishing_feeds_180923.txt")
    await start_crawling(["https://www.google.com/", "https://www.facebook.com/"])
    start_analysing()


if __name__ == '__main__':
    asyncio.run(main())