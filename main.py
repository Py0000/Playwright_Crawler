import crawler
import analyzer
import util_def

# Configurations: 
### User-Agent: Desktop User
### Referrer: Google 
### User interaction: Enabled
def crawl_with_desktop_user_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=True, act_flag=True)


# Configurations: 
### User-Agent: Desktop User
### Referrer: None 
### User interaction: Not Enabled
def crawl_with_desktop_user_no_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=False, act_flag=False)


# Configurations: 
### User-Agent: Desktop User
### Referrer: Google 
### User interaction: Not Enabled
def crawl_with_desktop_user_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=True, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=True, act_flag=False)


# Configurations: 
### User-Agent: Desktop User
### Referrer: None 
### User interaction: Enabled
def crawl_with_desktop_user_no_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_USER, ref_flag=False, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_USER, ref_flag=False, act_flag=True)





# Configurations: 
### User-Agent: Desktop Bot
### Referrer: Google 
### User interaction: Enabled
def crawl_with_desktop_bot_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=True, act_flag=True)


# Configurations: 
### User-Agent: Desktop Bot
### Referrer: None 
### User interaction: Not Enabled
def crawl_with_desktop_bot_no_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=False, act_flag=False)


# Configurations: 
### User-Agent: Desktop Bot
### Referrer: Google 
### User interaction: Not Enabled
def crawl_with_desktop_bot_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=True, act_flag=False)


# Configurations: 
### User-Agent: Desktop Bot
### Referrer: None 
### User interaction: Enabled
def crawl_with_desktop_bot_no_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Desktop Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.DESKTOP_BOT, ref_flag=False, act_flag=True)





# Configurations: 
### User-Agent: Mobile User
### Referrer: Google 
### User interaction: Enabled
def crawl_with_mobile_user_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile User\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.MOBILE_USER, ref_flag=True, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_USER, ref_flag=True, act_flag=True)


# Configurations: 
### User-Agent: Mobile User
### Referrer: None 
### User interaction: Not Enabled
def crawl_with_mobile_user_no_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile User\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.MOBILE_USER, ref_flag=False, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_USER, ref_flag=False, act_flag=False)


# Configurations: 
### User-Agent: Mobile User
### Referrer: Google 
### User interaction: Not Enabled
def crawl_with_mobile_user_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.MOBILE_USER, ref_flag=True, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_USER, ref_flag=True, act_flag=False)


# Configurations: 
### User-Agent: Mobile User
### Referrer: None 
### User interaction: Enabled
def crawl_with_mobile_user_no_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile User\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.MOBILE_USER, ref_flag=False, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_USER, ref_flag=False, act_flag=True)






# Configurations: 
### User-Agent: Mobile Bot
### Referrer: Google 
### User interaction: Enabled
def crawl_with_mobile_bot_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile Bot\nReferrer: Google\nUser interaction: Enabled")
    crawler.crawl(util_def.MOBILE_BOT, ref_flag=True, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_BOT, ref_flag=True, act_flag=True)


# Configurations: 
### User-Agent: Mobile Bot
### Referrer: None 
### User interaction: Not Enabled
def crawl_with_mobile_bot_no_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile Bot\nReferrer: None\nUser interaction: Not Enabled")
    crawler.crawl(util_def.MOBILE_BOT, ref_flag=False, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_BOT, ref_flag=False, act_flag=False)


# Configurations: 
### User-Agent: Mobile Bot
### Referrer: Google 
### User interaction: Not Enabled
def crawl_with_mobile_bot_referrer_no_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.MOBILE_BOT, ref_flag=True, act_flag=False, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_BOT, ref_flag=True, act_flag=False)


# Configurations: 
### User-Agent: Mobile Bot
### Referrer: None 
### User interaction: Enabled
def crawl_with_mobile_bot_no_referrer_action(seed_url_list):
    print("\nConfigurations:\nUser-Agent: Mobile Bot\nReferrer: Google\nUser interaction: Not Enabled")
    crawler.crawl(util_def.MOBILE_BOT, ref_flag=False, act_flag=True, url_list=seed_url_list)
    analyzer.extract_and_analyse(util_def.MOBILE_BOT, ref_flag=False, act_flag=True)


def start_program(seed_url_list):
    #crawl_with_desktop_user_referrer_action(seed_url_list)
    #crawl_with_desktop_bot_referrer_action(seed_url_list)
    crawl_with_mobile_user_referrer_action(seed_url_list)
    #crawl_with_mobile_bot_referrer_action(seed_url_list)
    """
    crawl_with_desktop_user_referrer_no_action(seed_url_list)
    crawl_with_desktop_bot_referrer_no_action(seed_url_list)
    crawl_with_mobile_user_referrer_no_action(seed_url_list)
    crawl_with_mobile_bot_referrer_no_action(seed_url_list)
    
    crawl_with_desktop_user_no_referrer_action(seed_url_list)
    crawl_with_desktop_bot_no_referrer_action(seed_url_list)
    crawl_with_mobile_user_no_referrer_action(seed_url_list)
    crawl_with_mobile_bot_no_referrer_action(seed_url_list)

    crawl_with_desktop_user_no_referrer_no_action(seed_url_list)
    crawl_with_desktop_bot_no_referrer_no_action(seed_url_list)
    crawl_with_mobile_user_no_referrer_no_action(seed_url_list)
    crawl_with_mobile_bot_no_referrer_no_action(seed_url_list)
    """

start_program(["https://www.google.com"])