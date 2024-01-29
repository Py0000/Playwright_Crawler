import argparse
from bs4 import BeautifulSoup
import os
import zipfile

import blank_page_util 
from blank_page_secondary_detector import css_hide_content
from image_analysis import is_screenshot_blank
from Utils import file_utils

def read_html_from_zip(zip_path, html_file_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(html_file_path) as file:
            html_content = file.read()
            return html_content


def detect_blank_page_html_script(soup):
    # Analyze the body 
    body_content = soup.body.get_text(strip=True)

    inline_body_css = soup.find('style').string if soup.find('style') else ''
    is_inline_html_css_blank = css_hide_content(inline_body_css)

    # Check if content of <body> is empty
    # And check if there are any child (direct) tags inside <body>
    if not body_content and len(soup.body.find_all(recursive=False)) == 0 or is_inline_html_css_blank:
        return True
    else:
        return False


def process_individual_dataset(current_dataset_dir, dir_without_zip_extension):
    dataset_status = {}
    ss_sub_stats = {}

    for sub_dir in ["self_ref", "no_ref"]:
        try:
            current_dataset_ref_dir = os.path.join(dir_without_zip_extension, sub_dir)
        
            current_dataset_html_file_aft = os.path.join(current_dataset_ref_dir, 'html_script_aft.html')
            current_dataset_html_file_bef = os.path.join(current_dataset_ref_dir, 'html_script_bef.html')
            current_dataset_ss_aft = os.path.join(current_dataset_ref_dir, 'screenshot_aft.png')
            current_dataset_ss_bef = os.path.join(current_dataset_ref_dir, 'screenshot_bef.png')

            html_content_bef = read_html_from_zip(current_dataset_dir, current_dataset_html_file_bef)
            soup_bef = BeautifulSoup(html_content_bef, 'html.parser')
            is_blank_by_html_bef = detect_blank_page_html_script(soup_bef)

            html_content_aft = read_html_from_zip(current_dataset_dir, current_dataset_html_file_aft)
            soup_aft = BeautifulSoup(html_content_aft, 'html.parser')
            is_blank_by_html_aft = detect_blank_page_html_script(soup_aft)

            is_ss_aft_blank, ss_aft_stats = is_screenshot_blank(current_dataset_dir, current_dataset_ss_aft)
            is_ss_bef_blank, ss_bef_stats = is_screenshot_blank(current_dataset_dir, current_dataset_ss_bef)

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
    
    return dataset_status, ss_sub_stats



def check_dataset_for_blank(main_directory):
    consolidated_results = {}
    ss_stats = {}

    extraction_path = file_utils.extract_zipfile(main_directory)
    date = file_utils.extract_date_from_extracted_zipfile_name(extraction_path)
    
    parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    for dir in os.listdir(parent_folder_path):
        print(f"Processing {dir}...")
        dir_without_zip_extension = dir.replace('.zip', '')
        current_dataset_dir = os.path.join(parent_folder_path, dir)
        dataset_stats, ss_sub_stats = process_individual_dataset(current_dataset_dir, dir_without_zip_extension)
        consolidated_results[dir_without_zip_extension] = dataset_stats
        ss_stats[dir_without_zip_extension] = ss_sub_stats

    base_output_dir = f"primary_logs/{date}"
    file_utils.check_and_generate_new_dir(base_output_dir)

    consolidated_output = os.path.join(base_output_dir, f"{date}_consolidation.json")
    ss_stats_output = os.path.join(base_output_dir, f"{date}_ss_stats.json")
    file_utils.export_output_as_json_file(consolidated_output, consolidated_results)
    file_utils.export_output_as_json_file(ss_stats_output, ss_stats)
    
    file_utils.remove_extracted_folder(extraction_path)
    return consolidated_output


def get_error_logs(consolidated_log_file_path, date, base_output_dir):
    print("\nGenerating error logs...")
    errors = []

    error_output = os.path.join(base_output_dir, f"{date}_error.txt")
    data = file_utils.read_data_from_json_file(consolidated_log_file_path)
    
    for folder_name, content in data.items():
        if (isinstance(content['self_ref'], str) or isinstance(content['no_ref'], str)):
            errors.append(folder_name)
    
    file_utils.export_output_as_txt_file(error_output, errors)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    args = parser.parse_args()

    consolidated_output = check_dataset_for_blank(args.folder_path)
    date = (args.folder_path.split('_')[-1]).split('.')[0]

    base_output_dir = os.path.join("primary_logs", date)
    blank_page_util.split_log_files(consolidated_output, date, ["html", "ss_aft", "ss_bef"], base_output_dir)
    get_error_logs(consolidated_output, date, base_output_dir)
