import os

import util_def



def format_index_base_file_name(index):
    return f"{index:08}"



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

    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)



def generate_crawling_folder_for_url(device_config, ref_flag, act_flag, url_index):
    ref = util_def.REF_SET if ref_flag else util_def.NO_REF_SET
    act = util_def.USER_ACT_SET if act_flag else util_def.NO_USER_ACT_SET

    base_path = f"{device_config}_{ref}_{act}"
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