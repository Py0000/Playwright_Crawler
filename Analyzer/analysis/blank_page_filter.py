import argparse
import json
import os
import shutil 
import zipfile


def read_blank_files_as_list(txt_file):
    with open(txt_file, "r") as f: 
        blank_folder_names = f.readlines()
    
    # Remove newline characters and any whitespace
    blank_folder_list = [folder_name.strip() for folder_name in blank_folder_names]

    return blank_folder_list


def filter_out_blank_page_by_html(date, dataset_path, blank_page_list, new_dir):
    status = []

    if "zip" in dataset_path:
        extraction_path = dataset_path.replace('.zip', '')
        with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
            print("\nExtracting zip folder ...")
            zip_ref.extractall(extraction_path)
        
        parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    else:
        parent_folder_path = os.path.join(dataset_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    
    # Create the new directory to hold the dataset that contains the blank webpages
    blank_page_dir = os.path.join(parent_folder_path, 'blank_pages', new_dir)
    if not os.path.exists(blank_page_dir):
        os.makedirs(blank_page_dir)


    for folder in blank_page_list:
        zip_dataset_path = os.path.join(parent_folder_path, f"{folder}.zip")
        if (os.path.exists(zip_dataset_path)):
            print(folder, os.path.exists(zip_dataset_path), "moved")
            shutil.move(zip_dataset_path, blank_page_dir)
        else:
            print(folder, os.path.exists(zip_dataset_path), "failed")
            status.append(folder) 
    
    log_dir = f"blank_page_cat_logs/{date}"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    output_path = os.path.join(log_dir, f"{date}_blank_page_{new_dir}_categorization_failed.json")
    with open(output_path, 'w') as f:
        for item in status:
            f.write(str(item) + '\n')
    
    return output_path

def is_also_potentially_blank_by_other_files(log_dir_path, filtered_out_dataset, date, type):
    print("Checking if filtered files are also potentially blank by other file types...")
    status = {}

    # Cross check against logs for css, js and ss_aft
    css_blank_list = read_blank_files_as_list(os.path.join(log_dir_path, f"{date}_css_blank_{type}.txt"))
    js_blank_list = read_blank_files_as_list(os.path.join(log_dir_path, f"{date}_js_blank_{type}.txt"))
    ss_aft_blank_list = read_blank_files_as_list(os.path.join(log_dir_path, f"{date}_ss_aft_blank_{type}.txt"))

    # Return a dict {dataset_name: {css: true/false, js: true/false, ss_aft: true/false}}
    for filtered in filtered_out_dataset:
        is_css_blank = False
        is_js_blank = False
        is_ss_aft_blank = False

        if filtered in css_blank_list:
            is_css_blank = True
        if filtered in js_blank_list:
            is_js_blank = True
        if filtered in ss_aft_blank_list:
            is_ss_aft_blank = True
        
        data = {
            "Is blank by css": is_css_blank,
            "Is blank by js": is_js_blank,
            "Is blank by ss (after)": is_ss_aft_blank
        }

        status[filtered] = data
    
    log_dir = f"blank_page_cat_logs/{date}"
    output_path = os.path.join(log_dir, f"{date}_blank_page_others_{type}_categorization.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)


def potentially_blank_not_filtered_yet():
    # Reads the list of filtered dataset folder names
    # Remove from css, js, ss_aft blank list/log files those that are already filtered
    # Return a new log with the remaining unfiltered ones
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("date", help="Date")
    parser.add_argument("folder_path", help="Folder name")
    parser.add_argument("blank_txt", help="Blank Page File")
    parser.add_argument("new_dir", help="Name of dir to keep blank dataset")
    args = parser.parse_args()
    
    log_dir_path = os.path.join("blank_page_logs", args.date)
    blank_txt_path = os.path.join(log_dir_path, f"{args.date}_{args.blank_txt}.txt")
    blank_page_list = read_blank_files_as_list(blank_txt_path)
    unsuccessful_filtered_path = filter_out_blank_page_by_html(args.date, args.folder_path, blank_page_list, args.new_dir)

    unsuccessful_filtered = read_blank_files_as_list(unsuccessful_filtered_path)
    filtered = [item for item in blank_page_list if item not in unsuccessful_filtered]
    is_also_potentially_blank_by_other_files(log_dir_path, filtered, args.date, args.new_dir)

