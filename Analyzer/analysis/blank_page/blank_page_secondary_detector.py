import argparse
import json
import os 
import zipfile
import shutil

import cssutils
import warnings
import logging
import re

import blank_page_util

cssutils.log.setLevel(logging.CRITICAL)

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


def check_external_css(file):
    with open(file, 'r', encoding='utf-8') as css_file:
        css_content = css_file.read()
        if css_hide_content(css_content):
            print("CSS File that has potential blank element: ", file)
            return True


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


def check_external_js(file):
    with open(file, 'r', encoding='utf-8') as js_file:
        js_content = js_file.read()
        if js_hide_content(js_content):
            print("JavaScript file that potentially renders the page blank: ", file)
            return True
        

# Recursively check external css scripts that renders the webpage blank
def check_external_files(network_resp_path):
    potential_css = []
    is_css_blank = False
    potential_js = []
    is_js_blank = False

    for filename in os.listdir(network_resp_path):
        if filename.endswith('.css'):
            filepath = os.path.join(network_resp_path, filename)
            is_potentially_css_blank = check_external_css(filepath)
            if is_potentially_css_blank:
                potential_css.append(filename)
                is_css_blank = True
        
        if filename.endswith('.js'):
            filepath = os.path.join(network_resp_path, filename)
            is_potentially_js_blank = check_external_js(filepath)
            if is_potentially_js_blank:
                potential_js.append(filename)
                is_js_blank = True

    return is_css_blank, potential_css, is_js_blank, potential_js


def check_external_resources_for_blank(main_directory):
    consolidated_results = {}

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
        for sub_dir in os.listdir(current_dataset_dir):
            try:
                current_dataset_ref_dir = os.path.join(current_dataset_dir, sub_dir)
                current_dataset_nw_resp_dir = os.path.join(current_dataset_ref_dir, 'network_response_files')
                
                is_blank_by_css, blank_css_list, is_blank_by_js, blank_js_list = check_external_files(current_dataset_nw_resp_dir)
                
                status = {
                    "CSS Style/Sheet": "Blank" if is_blank_by_css else "Not Blank",
                    "Potentially Blank CSS File": blank_css_list if is_blank_by_js else [],
                    "Js": "Blank" if is_blank_by_js else "Not Blank",
                    "Potentially Blank Js File": blank_js_list if is_blank_by_js else [],
                }

                dataset_status[sub_dir] = status
            
            except Exception as e:
                print(e)
                dataset_status[sub_dir] = "Error encountered while processing dataset folder"
            
        
        consolidated_results[current_dataset] = dataset_status
    
    base_output_dir = f"secondary_logs/{date}"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    
    consolidated_output = os.path.join(base_output_dir, f"{date}_blank_secondary.json")
    with open(consolidated_output, 'w', encoding='utf-8') as f:
        json.dump(consolidated_results, f, ensure_ascii=False, indent=4)
    
    shutil.rmtree(extraction_path)
    return consolidated_output
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    args = parser.parse_args()

    consolidated_output = check_external_resources_for_blank(args.folder_path)
    date = (args.folder_path.split('_')[-1]).split('.')[0]

    base_output_dir = os.path.join("secondary_logs", date)
    blank_page_util.split_log_files(consolidated_output, date, ["css", "js"], base_output_dir)
    