
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
