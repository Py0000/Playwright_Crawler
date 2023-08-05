import crawler
import extractor
import utility as util

# Configurations: 
# User-Agent: Desktop User
# Referrer: Google 
# User interaction: Enabled
def crawl_with_desktop_user_referrer_action(seed_url_list):
    crawler.crawl(seed_url_list, util.CONFIG_DESKTOP_USER, action_flag=True, referrer=util.GOOGLE_SEARCH_QUERY_REFERRER)
    extractor.extract_webpage(util.CONFIG_DESKTOP_USER)


def start_program(seed_url_list):
    crawl_with_desktop_user_referrer_action(seed_url_list)


start_program(["https://www.facebook.com/"])



    




