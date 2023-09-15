import re
from bs4 import BeautifulSoup
import utility as util


DYNAMIC_EVAL_PATTERN = r"eval\(" # Handles the dynamic nature of JavaScript to generate code on the fly with eval
DYNAMIC_WINDOW_PATTERN = r"window\[.*\]=" # handles cases where window object is used to store or manipulate data dynamically
DYNAMIC_DOCUMENT_PATTERN = r"document\[.*\]=" # handles cases where document object is used to manipulate data dynamically
FROM_CHAR_CODE_PATTERN = r"fromCharCode\(" # Handles cases of encoding/decoding 
UNESCAPE_PATTERN = r"unescape\(" # handles cases where unescape() is used to decode string
ASCII_TO_BINARY_PATTERN = r"atob\(" # handles cases where atob() i.e. ASCII to binary decoder is used
BASE64_ENCODING_PATTERN = re.compile(r'[A-Za-z0-9+/]{30,}={0,2}') # Potentially Base64 encoded data, reason for length 30 is to avoid false positives as base64 encoded strings are generally longer than the original string.
HEX_ENCODING_PATTERN = r'\b[0-9a-fA-F]{30,}\b' # Potentially hexadecimal encoded data, similar only data of min length 30 is flagged
UNICODE_ENCODING_PATTERN = r'(\\u[0-9a-fA-F]{4}){5,}' # Potentially unicode encoded data, similar only data of min length 30 is flagged
HTML_ENTITIES_ENCODING_PATTERN = r'((&#x?[0-9a-fA-F]+;){5,})' # Potentially html entities encoded data, similar only data of min length 30 is flagged
CRYPTO_LIB_JS_PATTERN = r"CryptoJs"  # handles cases where common cypto library in JS is used for encryption and decryption
 
obfuscation_indicators = [
    DYNAMIC_EVAL_PATTERN, 
    FROM_CHAR_CODE_PATTERN, 
    UNESCAPE_PATTERN, 
    ASCII_TO_BINARY_PATTERN, 
    DYNAMIC_WINDOW_PATTERN, 
    DYNAMIC_DOCUMENT_PATTERN, 
    CRYPTO_LIB_JS_PATTERN, 
    BASE64_ENCODING_PATTERN, 
    HEX_ENCODING_PATTERN, 
    UNICODE_ENCODING_PATTERN,
    HTML_ENTITIES_ENCODING_PATTERN
]

def detect_potential_obfuscation_scripts(html_file_name):
    html_content = util.get_html_content(html_file_name)
    soup = BeautifulSoup(html_content, 'lxml')
    
    potential_obfuscation_scripts = {}

    for script in soup.find_all('script'):
        # Check if it's an inline script
        if not script.attrs.get('src'):
            content = script.string
            if content:
                # Check for common obfuscation techniques
                for indicator in obfuscation_indicators:
                    if re.search(indicator, content):
                        potential_obfuscation_scripts.update({f"Flagged due to {indicator}": content})

                
    
    return potential_obfuscation_scripts