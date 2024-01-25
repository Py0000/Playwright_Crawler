import argparse
import time
import cssutils
import warnings
import logging
from bs4 import BeautifulSoup
import os
import zipfile
import shutil
import json
import re

from image_analysis import is_screenshot_blank

cssutils.log.setLevel(logging.CRITICAL)

def export_data_as_txt_file(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(str(item) + '\n')

def read_html_script(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return html_content


def detect_blank_page_html_script(soup):
    # Analyze the body 
    body_content = soup.body.get_text(strip=True)

    # Check if content of <body> is empty
    # And check if there are any child (direct) tags inside <body>
    if not body_content and len(soup.body.find_all(recursive=False)) == 0:
        return True
    else:
        return False
    

# Check for css styles that renders the webpage blank
def css_hide_content(css_content):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        sheet = cssutils.parseString(css_content)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                if 'body' in rule.selectorText or 'html' in rule.selectorText:
                    for property in rule.style:
                        if property.name == 'display' and property.value == 'none':
                            return True
    return False

# Recursively check external css scripts that renders the webpage blank
def external_css_hide_content(network_resp_path):
    for filename in os.listdir(network_resp_path):
        if filename.endswith('.css'):
            with open(os.path.join(network_resp_path, filename), 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                if css_hide_content(css_content):
                    print("CSS File that has potential blank element: ", filename)
                    return True
    return False


def check_if_css_renders_blank(soup, network_resp_path):
    inline_body_css = soup.find('style').string if soup.find('style') else ''
    is_blank_by_inline_css = css_hide_content(inline_body_css)

    is_blank_by_external_css = external_css_hide_content(network_resp_path)

    return is_blank_by_inline_css or is_blank_by_external_css


def js_hide_content(js_content):
    # Patterns that might indicate a blank page
    patterns = [
        re.compile(r'\bdocument\.body\.innerHTML\s*=\s*["\']\s*["\']', re.IGNORECASE),
        re.compile(r'\bdocument\.body\.style\.display\s*=\s*["\']none["\']', re.IGNORECASE),
        re.compile(r'\bdocument\.body\.style\.visibility\s*=\s*["\']hidden["\']', re.IGNORECASE),
        re.compile(r'\bdocument\.write\s*\(\s*["\']\s*["\']\s*\)', re.IGNORECASE),
        re.compile(r'\bdocument\.body\.outerHTML\s*=\s*["\']\s*["\']', re.IGNORECASE),
        re.compile(r'\bwhile\s*\(document\.body\.firstChild\)\s*document\.body\.removeChild\(document\.body\.firstChild\)', re.IGNORECASE),
    ]

    for pattern in patterns:
        if pattern.search(js_content):
            return True
    return False


def external_js_hide_content(network_resp_path):
    is_blank = False
    potential_files = []

    for filename in os.listdir(network_resp_path):
        if filename.endswith('.js'):
            with open(os.path.join(network_resp_path, filename), 'r', encoding='utf-8') as js_file:
                js_content = js_file.read()
                if js_hide_content(js_content):
                    print("JavaScript file that potentially renders the page blank: ", filename)
                    potential_files.append(filename)
                    is_blank = True

    return is_blank, potential_files

# Categorises html as blank if html_script_aft.html is blank
# CSS and JS are being detected as backup measures (As the detection is not accurate)
def check_dataset_for_blank(main_directory):
    consolidated_results = {}
    ss_stats = {}

    extraction_path = main_directory.replace('.zip', '')
    date = extraction_path.split('_')[-1]
    
    with zipfile.ZipFile(main_directory, 'r') as zip_ref:
        print("\nExtracting zip folder ...")
        zip_ref.extractall(extraction_path)
    
    parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    for dir in os.listdir(parent_folder_path):
        current_dataset = dir.replace('.zip', '')
        current_dataset_dir = os.path.join(parent_folder_path, dir)
        
        with zipfile.ZipFile(current_dataset_dir, 'r') as zip_ref:
            zip_extraction_path = current_dataset_dir.replace('.zip', '')
            print(f"Extracting inner zip folder {dir}...")
            zip_ref.extractall(zip_extraction_path)
            current_dataset_dir = os.path.join(zip_extraction_path, current_dataset)

        dataset_status = {}
        ss_sub_stats = {}
        for sub_dir in os.listdir(current_dataset_dir):
            try:
                current_dataset_ref_dir = os.path.join(current_dataset_dir, sub_dir)
                current_dataset_html_file_aft = os.path.join(current_dataset_ref_dir, 'html_script_aft.html')
                current_dataset_html_file_bef = os.path.join(current_dataset_ref_dir, 'html_script_aft.html')
                current_dataset_nw_resp_dir = os.path.join(current_dataset_dir, sub_dir, 'network_response_files')
                current_dataset_ss_aft = os.path.join(current_dataset_ref_dir, 'screenshot_aft.png')
                current_dataset_ss_bef = os.path.join(current_dataset_ref_dir, 'screenshot_bef.png')

                html_content_bef = read_html_script(current_dataset_html_file_bef)
                soup_bef = BeautifulSoup(html_content_bef, 'html.parser')
                is_blank_by_html_bef = detect_blank_page_html_script(soup_bef)
                
                html_content_aft = read_html_script(current_dataset_html_file_aft)
                soup_aft = BeautifulSoup(html_content_aft, 'html.parser')
                is_blank_by_html_aft = detect_blank_page_html_script(soup_aft)
                is_blank_by_css = check_if_css_renders_blank(soup_aft , current_dataset_nw_resp_dir)
                is_blank_by_js, potential_blank_js = external_js_hide_content(current_dataset_nw_resp_dir)
                is_ss_aft_blank, ss_aft_stats = is_screenshot_blank(current_dataset_ss_aft)
                is_ss_bef_blank, ss_bef_stats = is_screenshot_blank(current_dataset_ss_bef)

                status = {
                    "Html Script (Before)": "Blank" if is_blank_by_html_bef else "Not Blank",
                    "Html Script (After)": "Blank" if is_blank_by_html_aft else "Not Blank",
                    "CSS Style/Sheet": "Blank" if is_blank_by_css else "Not Blank",
                    "Js": "Blank" if is_blank_by_js else "Not Blank",
                    "Potentially Blank Js File": potential_blank_js if is_blank_by_js else [],
                    "Screenshot (After) result":  "Blank" if is_ss_aft_blank else "Not Blank",
                    "Screenshot (Before) result":  "Blank" if is_ss_bef_blank else "Not Blank",
                }
                dataset_status[sub_dir] = status

                screenshot_stats = {
                    "After": ss_aft_stats,
                    "Before": ss_bef_stats
                }
                ss_sub_stats[sub_dir] = screenshot_stats
            except:
                dataset_status[sub_dir] = "Error encountered while processing dataset folder"
                ss_sub_stats[sub_dir] = "Error encountered while processing dataset folder"
        
        consolidated_results[current_dataset] = dataset_status
        ss_stats[current_dataset] = ss_sub_stats   
    
    base_output_dir = f"blank_page_logs/{date}"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    consolidated_output = os.path.join(base_output_dir, f"{date}_blank_consolidation.json")
    ss_stats_output = os.path.join(base_output_dir, f"{date}_ss_stats.json")
    
    with open(consolidated_output, 'w', encoding='utf-8') as f:
        json.dump(consolidated_results, f, ensure_ascii=False, indent=4)
    
    with open(ss_stats_output, 'w', encoding='utf-8') as f:
        json.dump(ss_stats, f, ensure_ascii=False, indent=4)
    
    #shutil.rmtree(extraction_path)
    return consolidated_output


def log_files_get_dict_key_and_output_file(date, type):
    TYPE_MAP = {
        "html": "Html Script (After)",
        "css": "CSS Style/Sheet",
        "js": "Js",
        "ss_aft": "Screenshot (After) result",
        "ss_bef": "Screenshot (After) result",
    }

    base_output_dir = f"blank_page_logs/{date}"
    output_file_map = {
        "html": os.path.join(base_output_dir, f"{date}_html_blank"),
        "css": os.path.join(base_output_dir, f"{date}_css_blank"),
        "js": os.path.join(base_output_dir, f"{date}_js_blank"),
        "ss_aft": os.path.join(base_output_dir, f"{date}_ss_aft_blank"),
        "ss_bef": os.path.join(base_output_dir, f"{date}_ss_bef_blank"),
    }

    return TYPE_MAP[type], output_file_map[type]


def spilt_log_files_by_type(consolidated_log_file_path, type, date):
    both = []
    self_ref = []
    no_ref = []

    base_output_dir = f"blank_page_logs/{date}"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    dict_key, output_file_name = log_files_get_dict_key_and_output_file(date, type)

    with open(consolidated_log_file_path, 'r') as file:
        data = json.load(file)
    
    for folder_name, content in data.items():
        if (isinstance(content['self_ref'], dict) and isinstance(content['no_ref'], dict)):
            is_self_ref_blank = False
            is_no_ref_blank = False

            if content['self_ref'].get(dict_key) == "Blank":
                is_self_ref_blank = True
            if content['no_ref'].get(dict_key) == "Blank":
                is_no_ref_blank = True

            if is_self_ref_blank and is_no_ref_blank:
                both.append(folder_name)
            elif is_self_ref_blank:
                self_ref.append(folder_name)
            elif is_no_ref_blank:
                no_ref.append(folder_name)
        
    
    both_output_file = f"{output_file_name}_both.txt"
    self_ref_output_file = f"{output_file_name}_self_ref.txt"
    no_ref_output_file = f"{output_file_name}_no_ref.txt"       

    export_data_as_txt_file(both_output_file, both)
    export_data_as_txt_file(self_ref_output_file, self_ref)    
    export_data_as_txt_file(no_ref_output_file, no_ref)         


def get_error_logs(consolidated_log_file_path, date):
    print("\nGenerating error logs...")
    errors = []

    base_output_dir = f"blank_page_logs/{date}"
    error_output = os.path.join(base_output_dir, f"{date}_error.txt")

    with open(consolidated_log_file_path, 'r') as file:
        data = json.load(file)
    
    for folder_name, content in data.items():
        if (isinstance(content['self_ref'], str) or isinstance(content['no_ref'], str)):
            errors.append(folder_name)
    
    export_data_as_txt_file(error_output, errors)


def split_log_files(consolidated_log_file_path, date):
    print("\nGenerating more concise log files...")
    TYPE = ["html", "css", "js", "ss_aft", "ss_bef"]

    for type in TYPE:
        print(f"Generating concise log file based on {type}...")
        spilt_log_files_by_type(consolidated_log_file_path, type, date)
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    args = parser.parse_args()

    consolidated_output = check_dataset_for_blank(args.folder_path)
    date = (args.folder_path.split('_')[-1]).split('.')[0]
    split_log_files(consolidated_output, date)
    get_error_logs(consolidated_output, date)



