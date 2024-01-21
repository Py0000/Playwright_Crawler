import argparse
import cssutils
import warnings
import logging
from bs4 import BeautifulSoup
import os
import zipfile

cssutils.log.setLevel(logging.CRITICAL)

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
                    return True
    return False


def check_if_css_renders_blank(soup, network_resp_path):
    inline_body_css = soup.find('style').string if soup.find('style') else ''
    is_blank_by_inline_css = css_hide_content(inline_body_css)

    is_blank_by_external_css = external_css_hide_content(network_resp_path)

    return is_blank_by_inline_css or is_blank_by_external_css


# only checks html_script after js execution
def check_dataset_for_blank(main_directory):
    consolidated_results = {}
    blank_page_dataset = []
    extraction_path = main_directory.replace('.zip', '')
    date = extraction_path.split('_')[-1]
    
    with zipfile.ZipFile(main_directory, 'r') as zip_ref:
        print("Extracting zip folder ...")
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

        for sub_dir in os.listdir(current_dataset_dir):
            current_dataset_ref_dir = os.path.join(current_dataset_dir, sub_dir)
            current_dataset_html_file = os.path.join(current_dataset_ref_dir, 'html_script_aft.html')
            current_dataset_nw_resp_dir = os.path.join(current_dataset_dir, sub_dir, 'network_response_files')
            
            html_content = read_html_script(current_dataset_html_file)
            soup = BeautifulSoup(html_content, 'html.parser')
            is_blank_by_html = detect_blank_page_html_script(soup)

            if is_blank_by_html:
                consolidated_results[f"{current_dataset} {sub_dir}"] = "Html script (after) renders blank"
                blank_page_dataset.append(current_dataset)
            
            is_blank_by_css = check_if_css_renders_blank(soup , current_dataset_nw_resp_dir)
            if is_blank_by_css:
                consolidated_results[f"{current_dataset} {sub_dir}"] = "Css scripts renders blank"
                blank_page_dataset.append(current_dataset)

            consolidated_results[f"{current_dataset} {sub_dir}"] = "Not blank"
            print(consolidated_results) 

            break



# Possible to handle Javascript that causes a page to be blank?


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    args = parser.parse_args()

    check_dataset_for_blank(args.folder_path)



