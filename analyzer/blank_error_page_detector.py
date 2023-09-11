import json
import os
from bs4 import BeautifulSoup
import util_def

def determine_error_type(html_script):
    title_tag = html_script.title
    if title_tag:
        title = title_tag.text.lower() 
    
        if "404" in title or "not found" in title:
            return util_def.ERROR_TYPE_404
        
        elif "403" in title or "forbidden" in title:
            return util_def.ERROR_TYPE_403
        
        elif "unavailable" in title:
            return util_def.ERROR_TYPE_UNAVAILABLE

        elif "error" in title:
            return util_def.ERROR_TYPE_ERROR
        
        else:
            return None
    else:
        return None


def is_page_blank_or_error(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if content.startswith("Error occurred for url: "):
        return True, util_def.ERROR_TYPE_CONNECTION
    
    html_script = BeautifulSoup(content, 'lxml')
    has_error_type = determine_error_type(html_script)
    if (has_error_type != None):
        return True, has_error_type
    
    # Remove script and style content as they don't affect visual representation
    # Avoids false negative
    for script in html_script(["script", "style"]):
        script.extract()
    
    # Check for text content
    if html_script.get_text(strip=True):
        return False, None
    
    # Check for tags other than html, head, and body
    significant_tags = [tag for tag in html_script.find_all(True) if tag.name not in ['html', 'head', 'body']]
    if significant_tags:
        return False, None

    return True, util_def.ERROR_TYPE_BLANK


def detect_blank_page(main_folder_path):
    # Get a list of all items in the main_folder
    config_folders = os.listdir(main_folder_path)
    problem_html = {config: {} for config in config_folders}


    # Iterate through each item
    for config_folder in problem_html.keys():
        config_folder_path = os.path.join(main_folder_path, config_folder)
        url_index_folders = os.listdir(config_folder_path)
        url_index_folders.sort(key=int)

        for url_index_folder in url_index_folders:
            url_index_folder_path = os.path.join(config_folder_path, url_index_folder)
            html_file_path = os.path.join(url_index_folder_path, util_def.HTML_SCRIPT_FILE)

            if (os.path.exists(html_file_path)):
                result, type = is_page_blank_or_error(html_file_path)
                if (result):
                    problem_html[config_folder].update({url_index_folder: type})
    
    with open(os.path.join(util_def.COMPARISON_FOLDER, util_def.BLANK_ERROR_HTML_FILE), "w", encoding="utf-8") as f:
        json.dump(problem_html, f, ensure_ascii=False, indent=4)
        




detect_blank_page("dataset_phishing")