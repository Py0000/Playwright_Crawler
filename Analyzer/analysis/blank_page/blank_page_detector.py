import argparse
from bs4 import BeautifulSoup
import os
import zipfile
import shutil
import json

import blank_page_util 
from blank_page_secondary_detector import css_hide_content
from image_analysis import is_screenshot_blank


def read_html_script(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return html_content


def detect_blank_page_html_script(soup):
    # Analyze the body 
    body_content = soup.body.get_text(strip=True)

    inline_body_css = soup.find('style').string if soup.find('style') else ''
    is_inline_html_css_blank = css_hide_content(inline_body_css)

    # Check if content of <body> is empty
    # And check if there are any child (direct) tags inside <body>
    if not body_content and len(soup.body.find_all(recursive=False)) == 0 and not is_inline_html_css_blank:
        return True
    else:
        return False


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
                
                current_dataset_ss_aft = os.path.join(current_dataset_ref_dir, 'screenshot_aft.png')
                current_dataset_ss_bef = os.path.join(current_dataset_ref_dir, 'screenshot_bef.png')

                html_content_bef = read_html_script(current_dataset_html_file_bef)
                soup_bef = BeautifulSoup(html_content_bef, 'html.parser')
                is_blank_by_html_bef = detect_blank_page_html_script(soup_bef)
                
                html_content_aft = read_html_script(current_dataset_html_file_aft)
                soup_aft = BeautifulSoup(html_content_aft, 'html.parser')
                is_blank_by_html_aft = detect_blank_page_html_script(soup_aft)
                
                is_ss_aft_blank, ss_aft_stats = is_screenshot_blank(current_dataset_ss_aft)
                is_ss_bef_blank, ss_bef_stats = is_screenshot_blank(current_dataset_ss_bef)

                status = {
                    "Html Script (Before)": "Blank" if is_blank_by_html_bef else "Not Blank",
                    "Html Script (After)": "Blank" if is_blank_by_html_aft else "Not Blank",
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
    
    base_output_dir = f"blank_page/blank_page_logs/{date}"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    consolidated_output = os.path.join(base_output_dir, f"{date}_blank_consolidation.json")
    ss_stats_output = os.path.join(base_output_dir, f"{date}_ss_stats.json")
    
    with open(consolidated_output, 'w', encoding='utf-8') as f:
        json.dump(consolidated_results, f, ensure_ascii=False, indent=4)
    
    with open(ss_stats_output, 'w', encoding='utf-8') as f:
        json.dump(ss_stats, f, ensure_ascii=False, indent=4)
    
    shutil.rmtree(extraction_path)
    return consolidated_output



def get_error_logs(consolidated_log_file_path, date, base_output_dir):
    print("\nGenerating error logs...")
    errors = []

    error_output = os.path.join(base_output_dir, f"{date}_error.txt")

    with open(consolidated_log_file_path, 'r') as file:
        data = json.load(file)
    
    for folder_name, content in data.items():
        if (isinstance(content['self_ref'], str) or isinstance(content['no_ref'], str)):
            errors.append(folder_name)
    
    blank_page_util.export_data_as_txt_file(error_output, errors)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    args = parser.parse_args()

    consolidated_output = check_dataset_for_blank(args.folder_path)
    date = (args.folder_path.split('_')[-1]).split('.')[0]

    base_output_dir = os.path.join("blank_page", "primary_logs", date)
    blank_page_util.split_log_files(consolidated_output, date, ["html", "ss_aft", "ss_bef"], base_output_dir)
    get_error_logs(consolidated_output, date, base_output_dir)



