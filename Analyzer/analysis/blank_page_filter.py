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


def filter_out_blank_page_by_html(date, dataset_path, list_of_blank_page_file, new_dir):
    status = {}
    
    extraction_path = dataset_path.replace('.zip', '')
    with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
        print("\nExtracting zip folder ...")
        zip_ref.extractall(extraction_path)
    
    parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    
    # Create the new directory to hold the dataset that contains the blank webpages
    blank_page_dir = os.path.join(parent_folder_path, new_dir)
    if not os.path.exists(blank_page_dir):
        os.makedirs(blank_page_dir)

    blank_page_list = read_blank_files_as_list(list_of_blank_page_file)
    
    for folder in blank_page_list:
        zip_dataset_path = os.path.join(parent_folder_path, f"{folder}.zip")
        if (os.path.exists(zip_dataset_path)):
            print(folder, os.path.exists(zip_dataset_path), "moved")
            shutil.move(zip_dataset_path, blank_page_dir)
        else:
            print(folder, os.path.exists(zip_dataset_path), "failed")
            status[folder] = "Failed"
    
    log_dir = f"blank_page_cat_logs/{date}"
    os.makedirs(log_dir)

    output_path = os.path.join(log_dir, f"{date}_blank_page_categorization_failed.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("date", help="Date")
    parser.add_argument("folder_path", help="Folder name")
    parser.add_argument("blank_txt", help="Blank Page File")
    parser.add_argument("new_dir", help="Name of dir to keep blank dataset")
    args = parser.parse_args()

    filter_out_blank_page_by_html(args.date, args.folder_path, args.blank_txt, args.new_dir)

