import crawler
import analyzer
import util_def

"""
Mobile configurations and CSS files are not crawled in this version.
"""

def read_feeds_from_file(feed_path):
    urls = []
    with open(feed_path, "r") as f:
        for line in f:
            urls.append(line.strip())
    return urls



def crawl_ref_act(seed_url, url_index):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=True, url=seed_url, index=url_index)

    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True, url=seed_url, index=url_index)



def crawl_no_ref_no_act(seed_url, url_index):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=False, url=seed_url, index=url_index)

    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False, url=seed_url, index=url_index)



def crawl_ref_no_act(seed_url, url_index):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=False, url=seed_url, index=url_index)   

    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False, url=seed_url, index=url_index)



def crawl_no_ref_act(seed_url, url_index):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=True, url=seed_url, index=url_index)

    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True, url=seed_url, index=url_index)



def start_program(seed_url_list):
    print("Crawling in progress...")
    for url in seed_url_list:
        url_index = str(seed_url_list.index(url))
        crawl_ref_act(url, url_index)
        crawl_no_ref_no_act(url, url_index)
        crawl_ref_no_act(url, url_index)
        crawl_no_ref_act(url, url_index)
    print("Crawling done...")


#feeds = read_feeds_from_file("feeds_benign.txt")
start_program(["https://www.facebook.com", "https://www.google.com"])