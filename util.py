import os
from urllib.parse import urlparse

import definitions

def format_index_base_file_name(index):
    return f"{index:08}"


def read_urls_from_file(base_folder, before_after_folder):
    # Specify the folder and file path
    folder_path = definitions.CRAWLED_URL_FOLDER
    file_name = definitions.CRAWLED_URL_FILE_NAME
    file_path = os.path.join(base_folder, folder_path, before_after_folder, file_name)

    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls


def get_file_name_without_ext(file):
    file_name = os.path.basename(file)
    file_name_without_extension = os.path.splitext(file_name)[0]

    return file_name_without_extension


def extract_hostname(website_url):
    parsed_url = urlparse(website_url)
    hostname = parsed_url.hostname
    return hostname



def generate_folder_for_crawling(base_folder_name, sub_folder_lists):
    sub_sub_folder_lists = [definitions.SUBFOLDER_BEFORE, definitions.SUBFOLDER_AFTER]
    
    if not os.path.exists(base_folder_name):
        os.makedirs(base_folder_name)
    
    for sub_folder in sub_folder_lists:
        sub_folder_path = os.path.join(base_folder_name, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)

        
        not_to_generate_sub_sub_folder = [definitions.CRAWLED_EMBEDDED_LINK_FOLDER, definitions.CRAWLED_CLIENT_SIDE_SCRIPT_FOLDER, definitions.CRAWLED_REDIRECTION_FOLDER]
        if sub_folder not in not_to_generate_sub_sub_folder:
            for sub_sub_folder in sub_sub_folder_lists:
                sub_sub_folder_path = os.path.join(sub_folder_path, sub_sub_folder)
                if not os.path.exists(sub_sub_folder_path):
                    os.mkdir(sub_sub_folder_path)



def generate_extractor_analysis_folder(base_folder_name):
    sub_folder_lists = ['Certificates', 'DNS', 'Features_Before', 'Features_After']
    sub_sub_folder_lists = ['Analysis', 'Excelsheet', 'Json']

    if not os.path.exists(base_folder_name):
        os.makedirs(base_folder_name)
    
    for sub_folder in sub_folder_lists:
        sub_folder_path = os.path.join(base_folder_name, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)
        if sub_folder != 'DNS':
            for sub_sub_folder in sub_sub_folder_lists:
                sub_sub_folder_path = os.path.join(sub_folder_path, sub_sub_folder)
                if not os.path.exists(sub_sub_folder_path):
                    os.mkdir(sub_sub_folder_path)