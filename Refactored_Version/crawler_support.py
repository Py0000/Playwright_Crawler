import datetime 
import os

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import definitions



def test_check_user_agent(page):
    user_agent = page.evaluate('''() => window.navigator.userAgent''')
    print("User-Agent:", user_agent)

def test_check_referrer(page):
    referrer = page.evaluate('''() => document.referrer''')
    print(f"Referrer: {referrer}\n")



def save_html_script(base_folder_name, text, name, flag):
    file_name = name + ".html"
    sub_folder = flag
    file = os.path.join(os.getcwd(), base_folder_name, definitions.CRAWLED_HTML_SCRIPT_FOLDER, sub_folder, file_name)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)




def get_all_html_tags(base_folder_name, soup, index, flag):
    file_name = index + ".txt"
    sub_folder = flag
    file = os.path.join(os.getcwd(), base_folder_name, definitions.CRAWLED_HTML_TAG_FOLDER, sub_folder, file_name)

    set = {tag.name for tag in soup.find_all()}
    initial_diff = set.difference(definitions.CURRENT_COVERED_TAG_SET)
    diff = initial_diff.difference(definitions.CURRENT_KNOWN_EXCLUEDED_TAG_SET)

    if len(diff) == 0:
        diff = ""

    with open(file, "a") as f:
        f.write(str(diff))



def save_crawled_url(base_folder_name, url, file_name, flag):
    file_name = file_name + ".txt"
    sub_folder = flag
    file = os.path.join(os.getcwd(), base_folder_name, definitions.CRAWLED_URL_FOLDER, sub_folder, file_name)
    
    with open(file, "a") as f:
        f.write(url + '\n')



def get_screenshot_file_path(base_folder, file_name, flag, is_full):
    folder_path = definitions.CRAWLED_SCREENSHOT_FOLDER if not is_full else definitions.CRAWLED_FULL_SCREENSHOT_FOLDER
    sub_folder_path = flag
    file_name = f"{file_name}.png"
    file_path = os.path.join(base_folder, folder_path, sub_folder_path, file_name)

    return file_path



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



def detect_redirection(base_folder_name, current_url, actual_url, file_name):
    file_name = f"{file_name}.txt"
    file = os.path.join(os.getcwd(), base_folder_name, definitions.CRAWLED_REDIRECTION_FOLDER, file_name)

    if current_url != actual_url:
        with open(file, "a") as f:
            text = f"--------------------------------------------------------------\nActual URL: {actual_url}\nRedirected URL: {current_url}\n-------------------------------------------------------------\n\n"
            f.write(text)



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



def get_embedded_links(base_folder_name, soup, page, url, file_name):   
    file_date = datetime.date.today().strftime("%Y%m%d")
    file_time = datetime.datetime.now().time().strftime("%H%M%S")
    file_name = f"{file_name}_{file_date}_{file_time}.txt"

    path = os.path.join(os.getcwd(), base_folder_name, definitions.CRAWLED_EMBEDDED_LINK_FOLDER, file_name)

    added_url_set = set()
    added_url_set.add(url)
    added_url_set = get_links_in_anchor(soup, path, url, added_url_set)
    get_links_in_iframe(soup, path, url, page, added_url_set)



def get_level_one_embedded_link(file_path):
    url_list = []
    
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            url_list.append(url)
           
    return url_list