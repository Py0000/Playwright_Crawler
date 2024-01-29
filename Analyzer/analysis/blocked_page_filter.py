import argparse
import json
import os
import shutil
import zipfile

def get_seperate_list_of_blocked_data(txt_file):
    with open(txt_file, 'r') as file:
        data = json.load(file)
    
    both = []
    self_ref = []
    no_ref = []

    for key, value in data.items():
        self_ref_value = value.get('self_ref')
        no_ref_value = value.get('no_ref')

        if self_ref_value != 200 and no_ref_value != 200:
            both.append(key)
        elif self_ref_value != 200:
            self_ref.append(key)
        elif no_ref_value != 200:
            no_ref.append(key)
    
    blocked_lists_dict = {
        "both": both,
        "self_ref": self_ref, 
        "no_ref": no_ref
    }

    return blocked_lists_dict


def filter_blocked_page_by_category(date, parent_path, blocked_dir, cat, blocked_list):
    status = []

    blocked_sub_dir = os.path.join(blocked_dir, cat)
    if not os.path.exists(blocked_sub_dir):
        os.makedirs(blocked_sub_dir)
    
    for folder in blocked_list:
        zip_dataset_path = os.path.join(parent_path, folder)
        if (os.path.exists(zip_dataset_path)):
            shutil.move(zip_dataset_path, blocked_sub_dir)
        else:
            status.append(folder)
    
    output_path = f"{date}_blocked_page_cat_failed.json"
    with open(output_path, 'w') as f:
        for item in status:
            f.write(str(item) + '\n')


def filter_blocked_page_main(main_directory):
    
    if "zip" in main_directory:
        extraction_path = main_directory.replace('.zip', '')
        date = (extraction_path.split('_')[-1])
        with zipfile.ZipFile(main_directory, 'r') as zip_ref:
            print("\nExtracting zip folder ...")
            zip_ref.extractall(extraction_path)
        txt_parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', 'filter_logs')
        parent_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
        
    else:
        date = (main_directory.split('_')[-1])
        txt_parent_folder_path = os.path.join(main_directory, f'dataset_{date}', 'filter_logs')
        parent_path = os.path.join(main_directory, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')

    blocked_dataset_txt_file_path = os.path.join(txt_parent_folder_path, f"{date}_response_non_200_status.json")
    blocked_lists_dict = get_seperate_list_of_blocked_data(blocked_dataset_txt_file_path)
    
    blocked_page_dir = os.path.join(parent_path, "blocked")
    if not os.path.exists(blocked_page_dir):
        os.makedirs(blocked_page_dir)
    
    blocked_cats = ["both", "self_ref", "no_ref"]
    for cat in blocked_cats:
        print(f"Filtering based on {cat}...")
        filter_blocked_page_by_category(date, parent_path, blocked_page_dir, cat, blocked_lists_dict.get(cat))
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    args = parser.parse_args()

    filter_blocked_page_main(args.folder_path)