##### Related to configurations #####
DESKTOP_USER = "d_user"
DESKTOP_BOT = "d_bot"
MOBILE_USER = "m_user"
MOBILE_BOT = "m_bot"

REF_SET = "ref"
NO_REF_SET = "no_ref"
USER_ACT_SET = "act"
NO_USER_ACT_SET = "no_act"


###### Related to user-agents & Referrer ######
DESKTOP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
DESKTOP_BOT_AGENT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/115.0.0.0 Safari/537.36"
MOBILE_BOT_AGENT = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.75 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

DESKTOP_USER_AGENT_MAP = {
    DESKTOP_USER: [f"--user-agent={DESKTOP_USER_AGENT}"],
    DESKTOP_BOT: [f"--user-agent={DESKTOP_BOT_AGENT}"],
}

GOOGLE_REFERRER = "https://www.google.com"

###### Related to file names ######
NETWORK_FILE_BEFORE = "network.har"
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

FEATURES_EXCEL = "analysis_f_excel_aft.xlsx"
FEATURES_BEF_EXCEL = "analysis_f_excel_bef.xlsx"
FEATURES_JSON = "analysis_f_json_aft.json"
FEATURES_BEF_JSON = "analysis_f_json_bef.json"

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