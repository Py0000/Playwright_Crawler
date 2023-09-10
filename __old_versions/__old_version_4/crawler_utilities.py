import os

import crawler_actions
import crawler_support
import util

def wait_for_page_to_load(page):
    try:
        # Wait for the page to load completely (wait for the load event)
        page.wait_for_load_state('domcontentloaded')
    except:
        pass

    try:
        page.wait_for_load_state('networkidle')
    except:
        pass


def check_and_execute_user_actions(device_conf, act_flag, page):
    if not act_flag:
        pass
    else:
        crawler_actions.desktop_user_mouse_movement(page)


def check_and_execute_scroll(page, act_flag):
    if act_flag:
        crawler_actions.page_scroll(page)
    else:
        pass


def get_screenshot(page, folder_path, file_name):
    path = os.path.join(folder_path, file_name)
    crawler_support.save_screenshot(page, path)
    print("Screenshot Captured...")
