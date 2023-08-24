import definitions

def desktop_configuration_checker(base_folder_name):
    isDesktopBot = definitions.CONFIG_DESKTOP_BOT in base_folder_name 
    isDesktopUser = definitions.CONFIG_DESKTOP_USER in base_folder_name 
    isDesktop = isDesktopBot or isDesktopUser
    return isDesktop


def mobile_configuration_checker(base_folder_name):
    isMobileBot = definitions.CONFIG_MOBILE_BOT in base_folder_name
    isMobileUser = definitions.CONFIG_MOBILE_USER in base_folder_name
    isMobile = isMobileBot or isMobileUser
    return isMobile


def setup_desktop_crawler(playwright_object, config):
    # desktop_user_agent = util.DESKTOP_USER_AGENT_LIST[random.randint(1,2)]
    user_agent_map = {
        definitions.CONFIG_DESKTOP_USER: [f"--user-agent={definitions.DESKTOP_USER_AGENT}"],
        definitions.CONFIG_DESKTOP_BOT: [f"--user-agent={definitions.DESKTOP_BOT_AGENT}"],
    }

    custom_user_agent = user_agent_map.get(config)

    browser = playwright_object.chromium.launch(headless=True, slow_mo=50, args=custom_user_agent)

    # creates a new page within the browser
    page = browser.new_page()

    return browser, page


def setup_mobile_user_crawler(playwright_object):
    browser = playwright_object.webkit.launch(headless=True, slow_mo=50)
    context = browser.new_context(
        **playwright_object.devices['Pixel 5']
    )

    page = context.new_page()
    return browser, page


def setup_mobile_bot_crawler(playwright_object):
    browser = playwright_object.webkit.launch(headless=True, slow_mo=50)
    pixel_5_bot = playwright_object.devices['Pixel 5'].copy()
    pixel_5_bot['user_agent'] = definitions.MOBILE_BOT_AGENT

    context = browser.new_context(
        **pixel_5_bot
    )

    page = context.new_page()
    return browser, page


def setup_configuration(playwright_object, config):
    if definitions.CONFIG_MOBILE_USER in config:
        browser, page = setup_mobile_user_crawler(playwright_object)
    
    elif definitions.CONFIG_MOBILE_BOT in config:
        browser, page = setup_mobile_bot_crawler(playwright_object)
    
    else:
        browser, page = setup_desktop_crawler(playwright_object, config)
    
    return browser, page