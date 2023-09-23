import os
from urllib.parse import urlparse

import util_def



def extract_hostname(website_url):
    parsed_url = urlparse(website_url)
    hostname = parsed_url.hostname
    return hostname



def generate_crawling_base_folders(device_conf, ref_flag, act_flag):
    ref = util_def.REF_SET if ref_flag else util_def.NO_REF_SET
    act = util_def.USER_ACT_SET if act_flag else util_def.NO_USER_ACT_SET
    folder = f"{device_conf}_{ref}_{act}"
        
    if not os.path.exists(util_def.DATA_FOLDER):
        os.mkdir(util_def.DATA_FOLDER)

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



def get_analysis_folder_path(dataset_folder_path):
    # Splitting path into components
    parts = os.path.normpath(dataset_folder_path).split(os.sep)

    # Extracting the last two components
    sub_folder_path = os.path.join(parts[-2], parts[-1])

    output_path = os.path.join(util_def.ANALYSIS_FOLDER, sub_folder_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    return output_path