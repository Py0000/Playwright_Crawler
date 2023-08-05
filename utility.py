import datetime 
import os

from bs4 import BeautifulSoup
from urllib.parse import urljoin


CRAWLED_DATA_IDENTIFIER = "crawled_dataset"
CRAWLED_HTML_SCRIPT_FOLDER = "crawled_html_scripts"
CRAWLED_EMBEDDED_LINK_FOLDER = "crawled_embedded_links"

DESKTOP_BOT_AGENT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
DESKTOP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

FACEBOOK_REFERRER = "https://www.facebook.com/"
GOOGLE_REFERRER = "https://www.google.com/"


def format_index_base_file_name(index):
    return f"{index:08}"


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

def get_links_in_anchor(soup, file, url, added_url_set):
    for a in soup.find_all("a"):
        added_url_set = save_unique_embedded_url(file, a, url, added_url_set)
    
    return added_url_set

def get_links_in_iframe(soup, file, url, page, added_url_set):
    for iframe in soup.find_all('iframe'):
        iframe_src = iframe.get('src')  # Load the iframe URL in the WebDriver
        if not iframe_src:
            continue

        page.goto(iframe_src)
        iframe_soup = BeautifulSoup(page.page_source, 'lxml')

        for a in iframe_soup.find_all('a'):
            added_url_set = save_unique_embedded_url(file, a, url, added_url_set)

def get_embedded_links(base_folder_name, soup, page, url):   
    file_date = datetime.date.today().strftime("%Y%m%d")
    file_time = datetime.datetime.now().time().strftime("%H%M%S")
    file_name = f"embedded_links_{file_date}_{file_time}.txt"

    path = os.path.join(os.getcwd(), base_folder_name, CRAWLED_EMBEDDED_LINK_FOLDER, file_name)

    added_url_set = set()
    added_url_set.add(url)

    added_url_set = get_links_in_anchor(soup, path, url, added_url_set)
    get_links_in_iframe(soup, path, url, page, added_url_set)

    return path



def save_html_script(base_folder_name, text, name):
    file_name = name + ".html"
    file = os.path.join(os.getcwd(), base_folder_name, CRAWLED_HTML_SCRIPT_FOLDER, file_name)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
    
