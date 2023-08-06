import crawler
import extractor
import analyzer
import utility as util

# Configurations: 
# User-Agent: Desktop User
# Referrer: Google 
# User interaction: Enabled
def crawl_with_desktop_user_referrer_action(seed_url_list):
    print("\nCrawling and analyzing with Desktop User-Agent, referrer set and mouse movement enabled...")
    extracted_data_base_folder_name = f'data_{util.CONFIG_DESKTOP_USER}'

    # crawler.crawl(seed_url_list, util.CONFIG_DESKTOP_USER, action_flag=True, referrer=util.GOOGLE_SEARCH_QUERY_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, util.CONFIG_DESKTOP_USER)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)
    print("Done with Desktop User-Agent, referrer set and mouse movement enabled...")



def start_program(seed_url_list):
    crawl_with_desktop_user_referrer_action(seed_url_list)


start_program(["https://www.google.com.sg/"])



    




