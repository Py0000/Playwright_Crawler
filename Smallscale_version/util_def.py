##### Related to configurations #####
MAC = "mac"
WINDOWS = "win"
BOT = "bot"

GOOGLE_REF = "g_ref"
FACEBOOK_REF = "fb_ref"
TWITTER_REF = "t_ref"
SELF_REF = "self_ref"
NO_REF = "no_ref"

MOUSE_CLICK_LEFT = "left_click"
MOUSE_CLICK_RIGHT = "right_click"
MOUSE_MOVEMENT = "move"
PAGE_SCROLL = "scroll"
NO_USER_ACT_SET = "no_act"


###### Related to user-agents & Referrer ######
USER_USER_AGENT_WINDOWS_CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
USER_USER_AGENT_MAC_CHROME = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
DESKTOP_BOT_AGENT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/116.0.0.0 Safari/537.36"

DESKTOP_USER_AGENT_MAP = {
    MAC: [f"--user-agent={USER_USER_AGENT_MAC_CHROME}"],
    WINDOWS: [f"--user-agent={USER_USER_AGENT_WINDOWS_CHROME}"],
    BOT: [f"--user-agent={DESKTOP_BOT_AGENT}"]
}

GOOGLE_REFERRER = "https://www.google.com"
FACEBOOK_REFERRER = "https://www.facebook.com"
TWITTER_REFERRER = "https://www.twitter.com"

REFERRER_MAP = {
    GOOGLE_REF: GOOGLE_REFERRER,
    FACEBOOK_REF: FACEBOOK_REFERRER,
    TWITTER_REF: TWITTER_REFERRER,
}

###### Related to file names ######
NETWORK_FILE_BEFORE = "network.har"
DETAILED_NETWORK_FILE = "detailed_network.json"
SCREENSHOT_FILE = "screenshot_aft.png"
SCREENSHOT_BEF_FILE = "screenshot_bef.png"
REDIRECTION_FILE = "redirect.json"
VISITED_URL_FILE = "url.txt"
EMBEDDED_URL_FILE = "embedded.txt"
HTML_TAG_FILE = "html_tag_aft.txt"
HTML_TAG_BEF_FILE = "html_tag_bef.txt"
HTML_SCRIPT_FILE = "html_script_aft.html"
HTML_SCRIPT_BEF_FILE = "html_script_before.html"
CLIENT_SIDE_SCRIPT_FILE = "client_scripts.json"
TLS_CERT_FILE = "certificate.json"
DNS_FILE = "dns_records.json"
NETWORK_RESPONSE_FOLDER = "resp_data"


FEATURES_EXCEL = "features_excel_aft.xlsx"
FEATURES_BEF_EXCEL = "features_excel_bef.xlsx"
FEATURES_JSON = "features_json_aft.json"
FEATURES_BEF_JSON = "features_json_bef.json"
DNS_EXCEL = "dns_excel.xlsx"
DNS_CONSOLIDATED_EXCEL = "dns_consolidated_excel.xlsx"
CERT_CONSOLIDATED_EXCEL = "certs_consolidated_excel.xlsx"
CERT_CONSOLIDATED_JSON = "certs_consolidated_json.json"

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
DATA_FOLDER = "dataset"
ANALYSIS_FOLDER = "analysis"