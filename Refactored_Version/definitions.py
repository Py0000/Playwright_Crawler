
##### Related to Configurations #####
CONFIG_DESKTOP_USER = "d_user"
CONFIG_DESKTOP_BOT = "d_bot"
CONFIG_MOBILE_USER = "m_user"
CONFIG_MOBILE_BOT = "m_bot"

CONFIG_REFERRER_SET = "ref"
CONFIG_NO_REFERRER_SET = "no_ref"
CONFIG_USER_ACTION_ENABLED = "user_act"
CONFIG_USER_ACTION_NOT_ENABLED = "no_user_act"

DESKTOP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
DESKTOP_BOT_AGENT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/115.0.0.0 Safari/537.36"
MOBILE_BOT_AGENT = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.75 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

GOOGLE_SEARCH_QUERY_REFERRER = "https://www.google.com.sg/search?q="

##### Related to crawling folders #####
MAIN_CRAWLING_FOLDER = "crawled"
SUBFOLDER_BEFORE = "before"
SUBFOLDER_AFTER = "after"

CRAWLED_HTML_SCRIPT_FOLDER = "html_scripts" # Has before and after subfolder
CRAWLED_HTML_TAG_FOLDER = "html_tags" # Has before and after subfolder
CRAWLED_URL_FOLDER = "url" # Has before and after subfolder
CRAWLED_SCREENSHOT_FOLDER = "screenshots" # Has before and after subfolder
CRAWLED_FULL_SCREENSHOT_FOLDER = "ss_full" # Has before and after subfolder
CRAWLED_EMBEDDED_LINK_FOLDER = "embedded_links"
CRAWLED_REDIRECTION_FOLDER = "redirected_url"
CRAWLED_NETWORK_LOGS_FOLDER = "network_logs" # Has before and after subfolder
CRAWLED_CLIENT_SIDE_SCRIPT_FOLDER = "client_script"

NETWORK_LOGS_REQUEST_FILE = "request.json"
NETWORK_LOGS_RESPONSE_FILE = "response.json"
NETWORK_LOGS_DOM_FUNCTION_FILE = "dom_func.json"

##### Related to HTML Tags #####
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



##### MISCELLANEOUS #####
ERROR_URL_FLAG = "ERROR_URL"