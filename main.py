import time
import random

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
    print("------------------------------\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=True, url=seed_url, index=url_index)

    print("------------------------------\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True, url=seed_url, index=url_index)



def crawl_no_ref_no_act(seed_url, url_index):
    print("------------------------------\nConfigurations:\nUser-Agent: Desktop User\nReferrer: None\nUser interaction: Not Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=False, url=seed_url, index=url_index)

    print("------------------------------\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: None\nUser interaction: Not Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False, url=seed_url, index=url_index)



def crawl_ref_no_act(seed_url, url_index):
    print("------------------------------\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=False, url=seed_url, index=url_index)   

    print("------------------------------\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False, url=seed_url, index=url_index)



def crawl_no_ref_act(seed_url, url_index):
    print("------------------------------\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=True, url=seed_url, index=url_index)

    print("------------------------------\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled\n------------------------------")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True, url=seed_url, index=url_index)




def analyze_desktop_user_config_data():
    print("\n------------------------------\nAnalyzing data for user configurations\n------------------------------")
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=True, act_flag=True)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=False, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=True, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=False, act_flag=True)



def analyze_desktop_bot_config_data():
    print("\n------------------------------\nAnalyzing data for bot configurations\n------------------------------")
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True)




def start_program(seed_url_list):
    print("Crawling in progress...\n")
    for url in seed_url_list:
        url_index = str(seed_url_list.index(url))

        if url_index != "0":
            time.sleep(random.randint(10, 15))

        crawl_ref_act(url, url_index)
        crawl_no_ref_no_act(url, url_index)
        crawl_ref_no_act(url, url_index)
        crawl_no_ref_act(url, url_index)

    print("\nCrawling done...")

    analyze_desktop_user_config_data()
    analyze_desktop_bot_config_data()


feeds = read_feeds_from_file("feeds_benign.txt")
start_program(feeds)