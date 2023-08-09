import crawler
import extractor
import analyzer
import utility as util

# Configurations: 
# User-Agent: Desktop User
# Referrer: Google 
# User interaction: Enabled
def crawl_with_desktop_user_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Enabled")
    
    full_config = f"{util.CONFIG_DESKTOP_USER}_{util.CONFIG_REFERRER_SET}_{util.CONFIG_USER_ACTION_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=True, referrer=util.GOOGLE_SEARCH_QUERY_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)


# Configurations: 
# User-Agent: Desktop User
# Referrer: Empty 
# User interaction: Enabled
def crawl_with_desktop_user_no_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Empty\nUser interaction: Enabled")
    
    full_config = f"{util.CONFIG_DESKTOP_USER}_{util.CONFIG_NO_REFERRER_SET}_{util.CONFIG_USER_ACTION_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=True, referrer=None)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)


# Configurations: 
# User-Agent: Desktop User
# Referrer: Google 
# User interaction: Not Enabled
def crawl_with_desktop_user_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    
    full_config = f"{util.CONFIG_DESKTOP_USER}_{util.CONFIG_REFERRER_SET}_{util.CONFIG_USER_ACTION_NOT_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=False, referrer=util.GOOGLE_SEARCH_QUERY_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)


# Configurations: 
# User-Agent: Desktop Bot
# Referrer: Google 
# User interaction: Enabled
def crawl_with_desktop_bot_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Enabled")
    
    full_config = f"{util.CONFIG_DESKTOP_BOT}_{util.CONFIG_REFERRER_SET}_{util.CONFIG_USER_ACTION_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=True, referrer=util.GOOGLE_SEARCH_QUERY_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)



# Configurations: 
# User-Agent: Mobile User
# Referrer: Google 
# User interaction: Not Enabled
def crawl_with_mobile_user_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile User\nReferrer: Google\nUser interaction: Not Enabled")
    
    full_config = f"{util.CONFIG_MOBILE_USER}_{util.CONFIG_REFERRER_SET}_{util.CONFIG_USER_ACTION_NOT_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=False, referrer=util.GOOGLE_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)



# Configurations: 
# User-Agent: Mobile User
# Referrer: Google 
# User interaction: Enabled
def crawl_with_mobile_user_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile User\nReferrer: Google\nUser interaction: Enabled")
    
    full_config = f"{util.CONFIG_MOBILE_USER}_{util.CONFIG_REFERRER_SET}_{util.CONFIG_USER_ACTION_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=True, referrer=util.GOOGLE_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)



# Configurations: 
# User-Agent: Mobile Bot
# Referrer: Google 
# User interaction: Enabled
def crawl_with_mobile_bot_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile Bot\nReferrer: Google\nUser interaction: Enabled")
    
    full_config = f"{util.CONFIG_MOBILE_BOT}_{util.CONFIG_REFERRER_SET}_{util.CONFIG_USER_ACTION_ENABLED}"
    extracted_data_base_folder_name = f'data_{full_config}'

    crawler.crawl(seed_url_list, full_config, action_flag=True, referrer=util.GOOGLE_REFERRER)
    util.generate_extractor_analysis_folder(extracted_data_base_folder_name)
    extractor.extract_webpage(extracted_data_base_folder_name, full_config)
    analyzer.analyze_extracted_data(extracted_data_base_folder_name)



def start_program(seed_url_list):
    crawl_with_desktop_user_referrer_action(seed_url_list)
    #crawl_with_desktop_user_no_referrer_action(seed_url_list)
    #crawl_with_desktop_user_referrer_no_action(seed_url_list)
    crawl_with_desktop_bot_referrer_action(seed_url_list)
    #crawl_with_mobile_user_referrer_no_action(seed_url_list)
    crawl_with_mobile_user_referrer_action(seed_url_list)
    crawl_with_mobile_bot_referrer_action(seed_url_list)


start_program(["https://www.google.com.sg/"])



    




