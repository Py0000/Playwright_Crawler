import cssutils
from bs4 import BeautifulSoup

def read_html_script(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return html_content


def detect_blank_page_html_script(html_file_path):
    html_content = read_html_script(html_file_path)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Analyze the body 
    body_content = soup.body.get_text(strip=True)

    # Check if content of <body> is empty
    # And check if there are any child (direct) tags inside <body>
    if not body_content and len(soup.body.find_all(recursive=False)) == 0:
        return True
    else:
        return False
    


# Possible to handle inline CSS Style + external CSS Style sheet? 
# External CSS style sheet may need to make use of network resources downloaded when crawling and match those in the html script under <link> tags with rel="stylesheet"

def inline_css_hide_content(inline_css):
    sheet = cssutils.parseString(inline_css)
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            for property in rule.style:
                if property.name == 'display' and property.value == 'none':
                    return True
    return False

# Possible to handle Javascript that causes a page to be blank?