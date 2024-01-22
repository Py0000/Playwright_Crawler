import json
import os
import shutil
import zipfile

def read_list_of_blocked_dataset_from_file(txt_file):
    with open(txt_file, 'r') as file:
        data = json.load(file)
        folder_names = list(data.keys())

    return folder_names

def func(main_directory, new_dir):
    status = {}

    extraction_path = main_directory.replace('.zip', '')
    date = extraction_path.split('_')[-1]

    with zipfile.ZipFile(main_directory, 'r') as zip_ref:
        print("\nExtracting zip folder ...")
        zip_ref.extractall(extraction_path)

    txt_parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', 'filter_logs')
    blocked_dataset_txt_file_path = os.path.join(txt_parent_folder_path, f"{date}_response_non_200_status.json")
    blocked_list = read_list_of_blocked_dataset_from_file(blocked_dataset_txt_file_path)

    parent_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    blocked_page_dir = os.path.join(parent_path, new_dir)
    if not os.path.exists(blocked_page_dir):
        os.makedirs(blocked_page_dir)
    
    for folder in blocked_list:
        zip_dataset_path = os.path.join(parent_path, folder)
        if (os.path.exists(zip_dataset_path)):
            shutil.move(zip_dataset_path, blocked_page_dir)
        else:
            status[folder] = "Failed"
    
    output_path = f"{date}_blocked_page_categorization_failed.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)
    