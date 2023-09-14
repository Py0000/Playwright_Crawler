import time
import random
import asyncio

import crawler_async as crawler
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


#############################
# No User-action Section
#############################
async def crawl_google_ref_no_act(seed_url, url_index):
    referrer = util_def.GOOGLE_REF
    action = util_def.NO_USER_ACT_SET
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Google\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Google\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Google\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_facebook_ref_no_act(seed_url, url_index):
    referrer = util_def.FACEBOOK_REF
    action = util_def.NO_USER_ACT_SET
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Facebook\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Facebook\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Facebook\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_twitter_ref_no_act(seed_url, url_index):
    referrer = util_def.TWITTER_REF
    action = util_def.NO_USER_ACT_SET
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Twitter\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Twitter\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Twitter\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_self_ref_no_act(seed_url, url_index):
    referrer = util_def.SELF_REF
    action = util_def.NO_USER_ACT_SET
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Self\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Self\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Self\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_no_ref_no_act(seed_url, url_index):
    referrer = util_def.NO_REF
    action = util_def.NO_USER_ACT_SET
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: None\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: None\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: None\nUser interaction: None\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)




#############################
# Mouse Movement Section
#############################
async def crawl_google_ref_move(seed_url, url_index):
    referrer = util_def.GOOGLE_REF
    action = util_def.MOUSE_MOVEMENT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Google\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Google\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Google\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_facebook_ref_move(seed_url, url_index):
    referrer = util_def.FACEBOOK_REF
    action = util_def.MOUSE_MOVEMENT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Facebook\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Facebook\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Facebook\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_twitter_ref_move(seed_url, url_index):
    referrer = util_def.TWITTER_REF
    action = util_def.MOUSE_MOVEMENT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Twitter\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Twitter\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Twitter\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_self_ref_move(seed_url, url_index):
    referrer = util_def.SELF_REF
    action = util_def.MOUSE_MOVEMENT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Self\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Self\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Self\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_no_ref_move(seed_url, url_index):
    referrer = util_def.NO_REF
    action = util_def.MOUSE_MOVEMENT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: None\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: None\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: None\nUser interaction: Mouse Move\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)




#############################
# Page Scroll Section
#############################
async def crawl_google_ref_scroll(seed_url, url_index):
    referrer = util_def.GOOGLE_REF
    action = util_def.PAGE_SCROLL
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Google\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Google\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Google\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_facebook_ref_scroll(seed_url, url_index):
    referrer = util_def.FACEBOOK_REF
    action = util_def.PAGE_SCROLL
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Facebook\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Facebook\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Facebook\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_twitter_ref_scroll(seed_url, url_index):
    referrer = util_def.TWITTER_REF
    action = util_def.PAGE_SCROLL
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Twitter\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Twitter\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Twitter\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_self_ref_scroll(seed_url, url_index):
    referrer = util_def.SELF_REF
    action = util_def.PAGE_SCROLL
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Self\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Self\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Self\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_no_ref_scroll(seed_url, url_index):
    referrer = util_def.NO_REF
    action = util_def.PAGE_SCROLL
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: None\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: None\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: None\nUser interaction: Page Scroll\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)



#############################
# Left Click Section
#############################
async def crawl_google_ref_left_click(seed_url, url_index):
    referrer = util_def.GOOGLE_REF
    action = util_def.MOUSE_CLICK_LEFT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Google\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Google\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Google\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_facebook_ref_left_click(seed_url, url_index):
    referrer = util_def.FACEBOOK_REF
    action = util_def.MOUSE_CLICK_LEFT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Facebook\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Facebook\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Facebook\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_twitter_ref_left_click(seed_url, url_index):
    referrer = util_def.TWITTER_REF
    action = util_def.MOUSE_CLICK_LEFT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Twitter\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Twitter\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Twitter\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_self_ref_left_click(seed_url, url_index):
    referrer = util_def.SELF_REF
    action = util_def.MOUSE_CLICK_LEFT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Self\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Self\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Self\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_no_ref_left_click(seed_url, url_index):
    referrer = util_def.NO_REF
    action = util_def.MOUSE_CLICK_LEFT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: None\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: None\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: None\nUser interaction: Left Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)



#############################
# Right Click Section
#############################
async def crawl_google_ref_right_click(seed_url, url_index):
    referrer = util_def.GOOGLE_REF
    action = util_def.MOUSE_CLICK_RIGHT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Google\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Google\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Google\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_facebook_ref_right_click(seed_url, url_index):
    referrer = util_def.FACEBOOK_REF
    action = util_def.MOUSE_CLICK_RIGHT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Facebook\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Facebook\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Facebook\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_twitter_ref_right_click(seed_url, url_index):
    referrer = util_def.TWITTER_REF
    action = util_def.MOUSE_CLICK_RIGHT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Twitter\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Twitter\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Twitter\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_self_ref_right_click(seed_url, url_index):
    referrer = util_def.SELF_REF
    action = util_def.MOUSE_CLICK_RIGHT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: Self\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: Self\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: Self\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)


async def crawl_no_ref_right_click(seed_url, url_index):
    referrer = util_def.NO_REF
    action = util_def.MOUSE_CLICK_RIGHT
    print(f"------------------------------\nConfigurations:\nUser-Agent: Windows User\nReferrer: None\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.WINDOWS, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: MacOS User\nReferrer: None\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.MAC, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)

    print(f"------------------------------\nConfigurations:\nUser-Agent: Bot\nReferrer: None\nUser interaction: Right Click\nCurrent Url #: {url_index}------------------------------")
    await crawler.crawl(device_conf=util_def.BOT, ref_flag=referrer, act_flag=action, url=seed_url, index=url_index)





def analyze_windows_config_data():
    print("\n------------------------------\nAnalyzing data for windows configurations\n------------------------------")
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.SELF_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.TWITTER_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.NO_REF, act_flag=util_def.NO_USER_ACT_SET)

    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_MOVEMENT)

    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.SELF_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.TWITTER_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.NO_REF, act_flag=util_def.PAGE_SCROLL)

    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_CLICK_LEFT)

    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.WINDOWS, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)




def analyze_mac_config_data():
    print("\n------------------------------\nAnalyzing data for windows configurations\n------------------------------")
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.SELF_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.TWITTER_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.NO_REF, act_flag=util_def.NO_USER_ACT_SET)

    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_MOVEMENT)

    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.SELF_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.TWITTER_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.NO_REF, act_flag=util_def.PAGE_SCROLL)

    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_CLICK_LEFT)

    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.MAC, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)




def analyze_bot_config_data():
    print("\n------------------------------\nAnalyzing data for bot configurations\n------------------------------")
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.SELF_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.TWITTER_REF, act_flag=util_def.NO_USER_ACT_SET)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.NO_REF, act_flag=util_def.NO_USER_ACT_SET)

    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_MOVEMENT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_MOVEMENT)

    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.SELF_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.TWITTER_REF, act_flag=util_def.PAGE_SCROLL)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.NO_REF, act_flag=util_def.PAGE_SCROLL)

    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_CLICK_LEFT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_CLICK_LEFT)

    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.GOOGLE_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.SELF_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.FACEBOOK_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.TWITTER_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)
    analyzer.extract_and_analyse(util_def.BOT, ref_flag=util_def.NO_REF, act_flag=util_def.MOUSE_CLICK_RIGHT)




async def start_program(seed_url_list):
    print("Crawling in progress...\n")
    #print(seed_url_list)
    
    for url in seed_url_list:
        url_index = str(seed_url_list.index(url))

        if url_index != "0":
            time.sleep(random.randint(6, 12))

        await crawl_self_ref_no_act(url, url_index)
        await crawl_google_ref_no_act(url, url_index)
        await crawl_no_ref_no_act(url, url_index)
        await crawl_facebook_ref_no_act(url, url_index)
        await crawl_twitter_ref_no_act(url, url_index)

        await crawl_self_ref_move(url, url_index)
        await crawl_google_ref_move(url, url_index)
        await crawl_no_ref_move(url, url_index)
        await crawl_facebook_ref_move(url, url_index)
        await crawl_twitter_ref_move(url, url_index)

        await crawl_self_ref_scroll(url, url_index)
        await crawl_google_ref_scroll(url, url_index)
        await crawl_no_ref_scroll(url, url_index)
        await crawl_facebook_ref_scroll(url, url_index)
        await crawl_twitter_ref_scroll(url, url_index)

        await crawl_self_ref_left_click(url, url_index)
        await crawl_google_ref_left_click(url, url_index)
        await crawl_no_ref_left_click(url, url_index)
        await crawl_facebook_ref_left_click(url, url_index)
        await crawl_twitter_ref_left_click(url, url_index)

        await crawl_self_ref_right_click(url, url_index)
        await crawl_google_ref_right_click(url, url_index)
        await crawl_no_ref_right_click(url, url_index)
        await crawl_facebook_ref_right_click(url, url_index)
        await crawl_twitter_ref_right_click(url, url_index)
        
    
    print("\nCrawling done...")
    """
    analyze_windows_config_data()
    analyze_mac_config_data()
    analyze_bot_config_data()
    """

async def main():
    feeds = read_feeds_from_file("feeds/phishing_feeds_140923.txt")
    await start_program(feeds)


if __name__ == '__main__':
    asyncio.run(main())





