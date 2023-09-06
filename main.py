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


def crawl_desktop_user_config(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=True, url_list=seed_url_list)
    
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=False, url_list=seed_url_list)

    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=False, url_list=seed_url_list)

    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=True, url_list=seed_url_list)
    

def analyze_desktop_user_config_data():
    print("\n\n---ANALYZING DATA FOR DESKTOP USER CONFIG---")
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=True, act_flag=True)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=False, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=True, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=False, act_flag=True)





def crawl_desktop_bot_config(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True, url_list=seed_url_list)

    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False, url_list=seed_url_list)
    
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False, url_list=seed_url_list)

    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True, url_list=seed_url_list)


def analyze_desktop_bot_config_data():
    print("\n\n---ANALYZING DATA FOR DESKTOP BOT CONFIG---")
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True)



import time
def start_program(seed_url_list):
    start = time.time()
    #crawl_desktop_user_config(seed_url_list)
    #crawl_desktop_bot_config(seed_url_list)
    end = time.time()
    
    #analyze_desktop_user_config_data()
    analyze_desktop_bot_config_data()
    print("Time to crawl one url: ", end-start)


#feeds = read_feeds_from_file("feeds_benign.txt")
start_program(["https://www.google.com"])