import base64 
import hashlib
import json
import os

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import util_def

async def save_screenshot(page, folder_path, file_name):
    # Insurance code to guarantee that page is really loaded before taking screenshot
    try:
        await page.wait_for_load_state('networkidle')
    except:
        await page.wait_for_timeout(5000)

    path = os.path.join(os.getcwd(),folder_path, file_name)
    try: 
        await page.screenshot(path=path, full_page=True)
        print("Screenshot Captured...")
        status = "Success"
    except: 
        print("Unable to capture screenshot...")
        status = "Failed"
    finally:
        return status



def save_html_script(folder_path, file_name, content):
    file_path = os.path.join(os.getcwd(), folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def save_unique_html_tags(folder_path, soup, indicator):
    file_path = os.path.join(os.getcwd(), folder_path, util_def.FILE_HTML_TAG)

    set = {tag.name for tag in soup.find_all()}
    initial_diff = set.difference(util_def.CURRENT_COVERED_TAG_SET)
    diff = initial_diff.difference(util_def.CURRENT_KNOWN_EXCLUEDED_TAG_SET)

    if len(diff) == 0:
        diff = ""

    data = {
        indicator: diff
    }

    with open(file_path, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



async def extract_links(folder_path, soup, page, base_url):
    file_path = os.path.join(os.getcwd(), folder_path, util_def.EMBEDDED_URL_FILE)

    # Extract links from anchor tags
    added_url_set = get_link_in_anchor(file_path, soup, set(), base_url)

    # Extract links from iframes and nested iframes
    await get_link_in_iframe(file_path, soup, page, added_url_set, base_url)

    return file_path


def get_link_in_anchor(file_path, soup, added_url_set, base_url):
    for a in soup.find_all("a"):
        url = a.get("href")
        added_url_set = save_embedded_url(file_path, url, base_url, added_url_set)
    return added_url_set


async def get_link_in_iframe(file_path, soup, page, added_url_set, base_url):
    for iframe in soup.find_all('iframe'):
        iframe_src = iframe.attrs.get('src')  # Load the iframe 
        
        if not iframe_src:
            continue

        # Checks if the iframe contains legitimate url
        parsed_url = urlparse(iframe_src)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            continue

        added_url_set = save_embedded_url(file_path, iframe_src, base_url, added_url_set)
        await page.goto(iframe_src)
        iframe_soup = BeautifulSoup(await page.content(), 'lxml')
        added_url_set = await handle_nested_iframes(iframe_soup, file_path, page, added_url_set, base_url)


async def handle_nested_iframes(iframe_soup, file_path, page, added_url_set, base_url):
    for a in iframe_soup.find_all('a'):
        url = a.get("href")
        added_url_set = save_embedded_url(file_path, url, base_url, added_url_set)
    
    added_url_set = await get_link_in_iframe(file_path, iframe_soup, page, added_url_set, base_url)
    return added_url_set


def save_embedded_url(file_path, url, base_url, added_url_set):
    
    try: 
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            if urlparse(base_url).scheme:
                url = urljoin(base_url, url)

        if url not in added_url_set:
            with open(file_path, "a") as f:
                f.write(url + '\n')
                added_url_set.add(url)
    except:
        pass

    return added_url_set




def get_detailed_network_response_data_path(folder_path, visited_url):
    data_folder_path = os.path.join(os.getcwd(), folder_path, util_def.FOLDER_NETWORK_RESPONSES)
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)
    
    file_path = os.path.join(os.getcwd(), data_folder_path, f"{hashlib.sha256(visited_url.encode()).hexdigest()}")
    return file_path


def decode_network_response(response_body):
    if response_body['base64Encoded']:
        decoded_data = base64.b64decode(response_body['body'])
    else:
        decoded_data = response_body['body']
    
    return decoded_data


def save_decoded_file_data(file_name, mime_type, decoded_data):

    def save_utf8_files(file, data):
        with open(file, "w", encoding="utf-8") as f:
            f.write(data if isinstance(data, str) else data.decode('utf-8'))
    
    def save_binary_files(file, data):
        with open(file, "wb") as f:
            f.write(data)

    if "html" in mime_type:
        save_utf8_files(file_name + ".html", decoded_data)
    elif "xml" in mime_type:
        save_utf8_files(file_name + ".xml", decoded_data)
    elif "json" in mime_type:
        save_utf8_files(file_name + ".json", decoded_data)
    elif "javascript" in mime_type:
        save_utf8_files(file_name + ".js", decoded_data)
    elif "css" in mime_type:
        save_utf8_files(file_name + ".css", decoded_data)
    elif "image" in mime_type:
        save_binary_files(file_name + ".png", decoded_data) 
    elif "font/woff2" in mime_type:
        save_binary_files(file_name + ".woff2", decoded_data)
    elif "text" in mime_type:
        save_utf8_files(file_name + ".txt", decoded_data)
    else:
        # Default: save as binary
        save_binary_files(file_name + ".bin", decoded_data)


def save_more_detailed_network_logs(folder_path, data):
    print("Saving more detailed network logs...\n")
    try:
        file_dir = os.path.join(folder_path, util_def.FILE_DETAILED_NETWORK)
        with open(file_dir, 'w') as file:
            json.dump(data, file, indent=4)
        status = "Success"
    except:
        status = "Failed"
    finally:
        return status
    


# Get client-side scripts
client_side_scripts_injection_code = '''() => {
    const scripts = [];
    const scriptElements = document.querySelectorAll('script');
    scriptElements.forEach(script => {
        if (script.src) {
            scripts.push(script.src);
        } else {
            scripts.push(script.innerText);
        }
    });
    return scripts;
}'''


def save_client_side_script(folder_path, data):
    file = os.path.join(os.getcwd(), folder_path, util_def.CLIENT_SIDE_SCRIPT_FILE)

    # Save data to a JSON file
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

