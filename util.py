import os
from urllib.parse import urlparse

import util_def



def extract_hostname(website_url):
    parsed_url = urlparse(website_url)
    hostname = parsed_url.hostname
    return hostname



def generate_crawling_base_folders():
    folders = [
        f"{util_def.DESKTOP_USER}_{util_def.REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.DESKTOP_USER}_{util_def.NO_REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.DESKTOP_USER}_{util_def.REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.DESKTOP_USER}_{util_def.NO_REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.DESKTOP_BOT}_{util_def.REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.DESKTOP_BOT}_{util_def.NO_REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.DESKTOP_BOT}_{util_def.REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.DESKTOP_BOT}_{util_def.NO_REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.MOBILE_USER}_{util_def.REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.MOBILE_USER}_{util_def.NO_REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.MOBILE_USER}_{util_def.REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.MOBILE_USER}_{util_def.NO_REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.MOBILE_BOT}_{util_def.REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.MOBILE_BOT}_{util_def.NO_REF_SET}_{util_def.USER_ACT_SET}",
        f"{util_def.MOBILE_BOT}_{util_def.REF_SET}_{util_def.NO_USER_ACT_SET}",
        f"{util_def.MOBILE_BOT}_{util_def.NO_REF_SET}_{util_def.NO_USER_ACT_SET}",
    ]

    if not os.path.exists(util_def.DATA_FOLDER):
        os.mkdir(util_def.DATA_FOLDER)

    for folder in folders:
        folder_path = os.path.join(util_def.DATA_FOLDER, folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)



def generate_crawling_folder_for_url(device_config, ref_flag, act_flag, url_index):
    ref = util_def.REF_SET if ref_flag else util_def.NO_REF_SET
    act = util_def.USER_ACT_SET if act_flag else util_def.NO_USER_ACT_SET

    base_path = os.path.join(util_def.DATA_FOLDER, f"{device_config}_{ref}_{act}")
    folder_path = os.path.join(base_path, url_index)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    return folder_path



def desktop_configuration_checker(device_config):
    isDesktopBot = util_def.DESKTOP_BOT == device_config
    isDesktopUser = util_def.DESKTOP_USER == device_config
    isDesktop = isDesktopBot or isDesktopUser
    return isDesktop


def mobile_configuration_checker(device_config):
    isMobileBot = util_def.MOBILE_BOT == device_config
    isMobileUser = util_def.MOBILE_USER == device_config
    isMobile = isMobileBot or isMobileUser
    return isMobile


def get_analysis_folder_path(dataset_folder_path):
    # Splitting path into components
    parts = os.path.normpath(dataset_folder_path).split(os.sep)

    # Extracting the last two components
    sub_folder_path = os.path.join(parts[-2], parts[-1])

    output_path = os.path.join(util_def.ANALYSIS_FOLDER, sub_folder_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    return output_path
