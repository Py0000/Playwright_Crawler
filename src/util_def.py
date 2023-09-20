##### Referrer Configurations #####
REF_SET = "self_ref"
NO_REF_SET = "no_ref"


##### User-agents #####
USER_USER_AGENT_WINDOWS_CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"


##### File Names #####
FILE_HTML_SCRIPT_AFT = "html_script_aft.html"
FILE_HTML_SCRIPT_BEF = "html_script_bef.html"
FILE_HTML_TAG = "html_tag.json"
FILE_SCREENSHOT_AFT = "screenshot_aft.png"
FILE_SCREENSHOT_BEF = "screenshot_bef.png"
FILE_CRAWL_LOG_INFO = "log.json"
FILE_EMBEDDED_URL = "embedded_url.txt"
FILE_CLIENT_SIDE_SCRIPT = "client_scripts.json"
FILE_CERT = "cert.json"
FILE_DNS = "dns.json"
FILE_NETWORK_HAR = "network.har"
FILE_DETAILED_NETWORK = "detail_network.json"
FOLDER_NETWORK_RESPONSES = "network_resp_data"

FOLDER_DATASET_BASE = "dataset"
FOLDER_ANALYSIS_BASE = "analysis"

EXCEL_CERT_CONSOLIDATED = "certs_consolidated_excel.xlsx"
EXCEL_DNS = "dns_excel.xlsx"
EXCEL_FEATURES_AFT = "features_excel_aft.xlsx"
EXCEL_FEATURES_BEF = "features_excel_bef.xlsx"
EXCEL_DNS_CONSOLIDATED = "dns_consolidated_excel.xlsx"
JSON_CERT_CONSOLIDATED = "certs_consolidated_json.json"
JSON_FEATURES_AFT = "features_json_aft.json"
JSON_FEATURES_BEF = "features_json_bef.json"

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


##### Miscellaneous #####
ERROR_URL_FLAG = "ERROR_URL"
BEFORE_CLIENT_SIDE_RENDERING_INDICATOR = "Before client-side rendering"
AFTER_CLIENT_SIDE_RENDERING_INDICATOR = "After client-side rendering"