import datetime 
import os

from bs4 import BeautifulSoup
from urllib.parse import urljoin

ERROR_URL_FLAG = "ERROR_URL"

CRAWLED_DATA_IDENTIFIER = "crawled_dataset"
CRAWLED_HTML_SCRIPT_FOLDER = "crawled_html_scripts"
CRAWLED_EMBEDDED_LINK_FOLDER = "crawled_embedded_links"
CRAWLED_PAGE_SCREENSHOT_FOLDER = "crawled_screenshots"
CRAWLED_URL_FOLDER = "crawled_urls"
CRAWLED_HTML_TAG_FOLDER = "crawled_html_tags"
CRAWLED_REDIRECTION_FOLDER = "crawled_redirected_url"

DESKTOP_BOT_AGENT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
DESKTOP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

GOOGLE_SEARCH_QUERY_REFERRER = "https://www.google.com.sg/search?q="
FACEBOOK_REFERRER = "https://www.facebook.com/"
GOOGLE_REFERRER = "https://www.google.com/"

CURRENT_COVERED_TAG_SET = {'title', 
                           'form', 'input', 'textarea', 'button', 'select', 'output',
                           'iframe',
                           'style', 'span', 'hr',
                           'img', 'audio', 'video', 'svg', 'picture', 'source', 'track', 'map', 'canvas',
                           'a', 'link', 'nav',
                           'script', 'noscript', 'embed', 'object', 'code',
                           'ul', 'ol', 'dl', 'dt', 'dd',
                           'table',
                           'head', 'meta', 'base', 'bpdy', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'body',
                           'div', 'header', 'footer', 'main', 'section', 'article', 'aside', 'details', 'dialog', 'data',
                           'br', 'html',
                           'abbr', 'b', 'bdi', 'bdo', 'blockquote', 'cite', 'del', 'dfn', 'em', 'i', 'ins', 'kbd',
                           'mark', 'pre', 'q', 's', 'small', 'samp', 'strong', 'sup', 'sub', 'u', 'var',
                           'meter', 'progress',
                           'template',
                        }

CURRENT_KNOWN_EXCLUEDED_TAG_SET = {
    'optgroup', 'option', 'label', 'fieldset', 'legend', 'datalist', 'area', 'figcaption', 'figure', 
    'li', 'caption', 'th', 'tr', 'td', 'thead', 'tbody', 'tfoot', 'col', 'colgroup', 'summary', 'param',
}


def test_check_user_agent(page):
    user_agent = page.evaluate('''() => window.navigator.userAgent''')
    print("User-Agent:", user_agent)

def test_check_referrer(page):
    referrer = page.evaluate('''() => document.referrer''')
    print("Referrer:", referrer)



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
        iframe_soup = BeautifulSoup(page.content(), 'lxml')

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

def get_level_one_embedded_link(file_path):
    url_list = []
    
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            url_list.append(url)
           
    return url_list


def save_html_script(base_folder_name, text, name):
    file_name = name + ".html"
    file = os.path.join(os.getcwd(), base_folder_name, CRAWLED_HTML_SCRIPT_FOLDER, file_name)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
    


def save_crawled_url(base_folder_name, url):
    file_name = "urls.txt"
    file = os.path.join(os.getcwd(), base_folder_name, CRAWLED_URL_FOLDER, file_name)
    
    with open(file, "a") as f:
        f.write(url + '\n')



def get_screenshot_file_path(base_folder, file_name):
    folder_path = CRAWLED_PAGE_SCREENSHOT_FOLDER
    file_name = f"{file_name}.png"
    file_path = os.path.join(base_folder, folder_path, file_name)

    return file_path



def get_all_html_tags(base_folder_name, soup, index):
    file_name = index + ".txt"
    file = os.path.join(os.getcwd(), base_folder_name, CRAWLED_HTML_TAG_FOLDER, file_name)

    set = {tag.name for tag in soup.find_all()}
    initial_diff = set.difference(CURRENT_COVERED_TAG_SET)
    diff = initial_diff.difference(CURRENT_KNOWN_EXCLUEDED_TAG_SET)

    if len(diff) == 0:
        diff = ""

    with open(file, "a") as f:
        f.write(str(diff))


def detect_redirection(base_folder_name, current_url, actual_url):
    file_name = "redirection.txt"
    file = os.path.join(os.getcwd(), base_folder_name, CRAWLED_REDIRECTION_FOLDER, file_name)

    if current_url != actual_url:
        with open(file, "a") as f:
            text = f"--------------------------------------------------------------\nActual URL: {actual_url}\nRedirected URL: {current_url}\n-------------------------------------------------------------\n\n"
            f.write(text)