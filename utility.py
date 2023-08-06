import os
from urllib.parse import urlparse

ERROR_URL_FLAG = "ERROR_URL"

CONFIG_DESKTOP_USER = "desktop_user"
CONFIG_DESKTOP_BOT = "desktop_bot"
CONFIG_MOBILE_USER = "mobile_user"
CONFIG_MOBILE_BOT = "mobile_bot"

CRAWLED_DATA_IDENTIFIER = "crawled_dataset"
CRAWLED_HTML_SCRIPT_FOLDER = "crawled_html_scripts"
CRAWLED_EMBEDDED_LINK_FOLDER = "crawled_embedded_links"
CRAWLED_PAGE_SCREENSHOT_FOLDER = "crawled_screenshots"
CRAWLED_URL_FOLDER = "crawled_urls"
CRAWLED_HTML_TAG_FOLDER = "crawled_html_tags"
CRAWLED_REDIRECTION_FOLDER = "crawled_redirected_url"
CRAWLED_URL_FILE_NAME = "urls.txt"

OUTPUT_PATH_EXCEL_FEATURES = "Features/Excelsheet/"
OUTPUT_PATH_JSON_FEATURES = "Features/Json/"
OUTPUT_PATH_EXCEL_CERTS = "Certificates/Excelsheet/"
OUTPUT_PATH_JSON_CERTS = "Certificates/Json/"
OUTPUT_PATH_DNS = "DNS/"


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



def format_index_base_file_name(index):
    return f"{index:08}"


def read_urls_from_file(base_folder):
    # Specify the folder and file path
    folder_path = CRAWLED_URL_FOLDER
    file_name = CRAWLED_URL_FILE_NAME
    file_path = os.path.join(base_folder, folder_path, file_name)

    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls


def extract_hostname(website_url):
    parsed_url = urlparse(website_url)
    hostname = parsed_url.hostname
    return hostname


def generate_extractor_analysis_folder(base_folder_name):
    sub_folder_lists = ['Certificates', 'DNS', 'Features']
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