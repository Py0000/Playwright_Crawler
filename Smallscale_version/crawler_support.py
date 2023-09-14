import json
import os
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import util_def


def save_crawled_url(folder_path, url):
    path = os.path.join(os.getcwd(), folder_path, util_def.VISITED_URL_FILE)
    
    with open(path, "a") as f:
        f.write(url + '\n')


def detect_redirection(folder_path, visited_url, provided_url):
    file_name = util_def.REDIRECTION_FILE
    path = os.path.join(os.getcwd(), folder_path, file_name)

    data = {
        "Visited Url": visited_url,
        "Provided Url": provided_url,
        "Has Changed?": visited_url != provided_url
    }
    
    with open(path, "a") as j_file:
        json.dump(data, j_file, indent=4)


def save_screenshot(page, save_loc):
    try: 
        page.screenshot(path=save_loc, full_page=True)
    except:
        print("UNABLE TO SAVE SCREENSHOT...")


def save_html_script(folder_path, file_name, text):
    file_path = os.path.join(os.getcwd(), folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


def get_all_html_tags(folder_path, soup, file_name):
    file_path = os.path.join(os.getcwd(), folder_path, file_name)

    set = {tag.name for tag in soup.find_all()}
    initial_diff = set.difference(util_def.CURRENT_COVERED_TAG_SET)
    diff = initial_diff.difference(util_def.CURRENT_KNOWN_EXCLUEDED_TAG_SET)

    if len(diff) == 0:
        diff = ""

    with open(file_path, "a") as f:
        f.write(str(diff))


def extract_links(folder_path, soup, page, base_url):
    file_path = os.path.join(os.getcwd(), folder_path, util_def.EMBEDDED_URL_FILE)

    # Extract links from anchor tags
    added_url_set = get_link_in_anchor(file_path, soup, set(), base_url)

    # Extract links from iframes and nested iframes
    get_link_in_iframe(file_path, soup, page, added_url_set, base_url)

    return file_path


def get_link_in_anchor(file_path, soup, added_url_set, base_url):
    for a in soup.find_all("a"):
        url = a.get("href")
        added_url_set = save_embedded_url(file_path, url, base_url, added_url_set)
    return added_url_set


def get_link_in_iframe(file_path, soup, page, added_url_set, base_url):
    for iframe in soup.find_all('iframe'):
        iframe_src = iframe.attrs.get('src')  # Load the iframe 
        
        if not iframe_src:
            continue

        # Checks if the iframe contains legitimate url
        parsed_url = urlparse(iframe_src)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            continue

        added_url_set = save_embedded_url(file_path, iframe_src, base_url, added_url_set)
        page.goto(iframe_src)
        iframe_soup = BeautifulSoup(page.content(), 'lxml')
        added_url_set = handle_nested_iframes(iframe_soup, file_path, page, added_url_set, base_url)


def handle_nested_iframes(iframe_soup, file_path, page, added_url_set, base_url):
    for a in iframe_soup.find_all('a'):
        url = a.get("href")
        added_url_set = save_embedded_url(file_path, url, base_url, added_url_set)
    
    added_url_set = get_link_in_iframe(file_path, iframe_soup, page, added_url_set, base_url)
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


def get_level_one_embedded_link(file_path):
    url_list = []
    
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            url_list.append(url)
           
    return url_list


def save_more_detailed_network_logs(folder_path, data):
    print("Saving more detailed network logs...\n")
    file_dir = os.path.join(folder_path, util_def.DETAILED_NETWORK_FILE)
    with open(file_dir, 'w') as file:
        json.dump(data, file, indent=4)


def get_detailed_network_response_data_path(folder_path):
    data_folder_path = os.path.join(folder_path, util_def.NETWORK_RESPONSE_FOLDER)
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)
    
    return data_folder_path


def save_decoded_file_data(file, decoded_data):
    with open(file, "w", encoding="utf-8") as f:
        f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
    
