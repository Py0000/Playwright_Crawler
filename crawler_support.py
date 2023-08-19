import datetime 
import os

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import utility as util

def test_check_user_agent(page):
    user_agent = page.evaluate('''() => window.navigator.userAgent''')
    print("User-Agent:", user_agent)

def test_check_referrer(page):
    referrer = page.evaluate('''() => document.referrer''')
    print(f"Referrer: {referrer}\n")


def generate_folder_for_crawling(base_folder_name, sub_folder_lists):
    if not os.path.exists(base_folder_name):
        os.makedirs(base_folder_name)
    
    for sub_folder in sub_folder_lists:
        sub_folder_path = os.path.join(base_folder_name, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)


def full_url_converter(url, base):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return urljoin(base, url)

def save_unique_embedded_url(file, anchor_tag, URL, added_url_set):
    try:
        url = full_url_converter(anchor_tag.get("href"), URL)
        if url not in added_url_set:
            with open(file, "a") as f:
                f.write(url + '\n')
                added_url_set.add(url)
        
    except:
        pass

    return added_url_set

def save_iframe_src(file, iframe_src, added_url_set):
    try:
        url = full_url_converter(iframe_src)
        if url not in added_url_set:
            with open(file, "a") as f:
                f.write(url + '\n')
                added_url_set.add(url)
    
    except:
        pass

    return added_url_set

def get_links_in_anchor(soup, file, url, added_url_set):
    for a in soup.find_all("a"):
        added_url_set = save_unique_embedded_url(file, a, url, added_url_set)
    return added_url_set

def handle_nested_iframes(iframe_soup, url, file, page, added_url_set):
    for a in iframe_soup.find_all('a'):
        added_url_set = save_unique_embedded_url(file, a, url, added_url_set)
    
    added_url_set = get_links_in_iframe(iframe_soup, file, url, page, added_url_set)
    return added_url_set

def get_links_in_iframe(soup, file, url, page, added_url_set):
    for iframe in soup.find_all('iframe'):
        iframe_src = iframe.get('src')  # Load the iframe URL in the WebDriver
        if not iframe_src:
            continue
        
        parsed_url = urlparse(iframe_src)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            continue

        added_url_set = save_iframe_src(file, iframe_src, added_url_set)
        page.goto(iframe_src)
        iframe_soup = BeautifulSoup(page.content(), 'lxml')
        added_url_set = handle_nested_iframes(iframe_soup, url, file, page, added_url_set)

    return added_url_set
        

def get_embedded_links(base_folder_name, soup, page, url):   
    file_date = datetime.date.today().strftime("%Y%m%d")
    file_time = datetime.datetime.now().time().strftime("%H%M%S")
    file_name = f"embedded_links_{file_date}_{file_time}.txt"

    path = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_EMBEDDED_LINK_FOLDER, file_name)

    added_url_set = set()
    added_url_set.add(url)
    added_url_set = get_links_in_anchor(soup, path, url, added_url_set)
    get_links_in_iframe(soup, path, url, page, added_url_set)

    return path

def get_level_one_embedded_link(file_path):
    url_list = []
    
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            url_list.append(url)
           
    return url_list


def save_html_script(base_folder_name, text, name):
    file_name = name + ".html"
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_HTML_SCRIPT_FOLDER, file_name)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
    
def save_html_script_before_client_side_rendering(base_folder_name, text, name):
    file_name = name + ".html"
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_HTML_SCRIPT_BEFORE_FOLDER, file_name)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

def save_crawled_url(base_folder_name, url):
    file_name = util.CRAWLED_URL_FILE_NAME
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_URL_FOLDER, file_name)
    
    with open(file, "a") as f:
        f.write(url + '\n')

def save_crawled_url_before_client_client_rendering(base_folder_name, url):
    file_name = util.CRAWLED_URL_FILE_NAME
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_URL_BEFORE_FOLDER, file_name)
    
    with open(file, "a") as f:
        f.write(url + '\n')


def get_screenshot_file_path(base_folder, file_name):
    folder_path = util.CRAWLED_PAGE_SCREENSHOT_FOLDER
    file_name = f"{file_name}.png"
    file_path = os.path.join(base_folder, folder_path, file_name)

    return file_path



def get_all_html_tags(base_folder_name, soup, index):
    file_name = index + ".txt"
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_HTML_TAG_FOLDER, file_name)

    set = {tag.name for tag in soup.find_all()}
    initial_diff = set.difference(util.CURRENT_COVERED_TAG_SET)
    diff = initial_diff.difference(util.CURRENT_KNOWN_EXCLUEDED_TAG_SET)

    if len(diff) == 0:
        diff = ""

    with open(file, "a") as f:
        f.write(str(diff))


def get_all_html_tags_before_client_side_rendering(base_folder_name, soup, index):
    file_name = index + ".txt"
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_HTML_TAG_BEFORE_FOLDER, file_name)

    set = {tag.name for tag in soup.find_all()}
    initial_diff = set.difference(util.CURRENT_COVERED_TAG_SET)
    diff = initial_diff.difference(util.CURRENT_KNOWN_EXCLUEDED_TAG_SET)

    if len(diff) == 0:
        diff = ""

    with open(file, "a") as f:
        f.write(str(diff))


def detect_redirection(base_folder_name, current_url, actual_url):
    file_name = "redirection.txt"
    file = os.path.join(os.getcwd(), base_folder_name, util.CRAWLED_REDIRECTION_FOLDER, file_name)

    if current_url != actual_url:
        with open(file, "a") as f:
            text = f"--------------------------------------------------------------\nActual URL: {actual_url}\nRedirected URL: {current_url}\n-------------------------------------------------------------\n\n"
            f.write(text)