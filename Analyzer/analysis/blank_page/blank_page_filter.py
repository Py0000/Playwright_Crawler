import argparse
import os

from Utils import file_utils

def read_blank_files_as_list(txt_file):
    with open(txt_file, "r") as f: 
        blank_folder_names = f.readlines()
    
    # Remove newline characters and any whitespace
    blank_folder_list = [folder_name.strip() for folder_name in blank_folder_names]

    return blank_folder_list


def filter_out_blank_page_by_html(date, dataset_path, blank_page_list, new_dir):
    status = []

    if "zip" in dataset_path:
        extraction_path = file_utils.extract_zipfile(dataset_path)
        parent_folder_path = os.path.join(extraction_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    else:
        parent_folder_path = os.path.join(dataset_path, f'dataset_{date}', f'dataset_{date}', 'complete_dataset')
    
    # Create the new directory to hold the dataset that contains the blank webpages
    blank_page_dir = os.path.join(parent_folder_path, 'blank_pages', new_dir)
    file_utils.check_and_generate_new_dir(blank_page_dir)


    for folder in blank_page_list:
        zip_dataset_path = os.path.join(parent_folder_path, f"{folder}.zip")
        if (os.path.exists(zip_dataset_path)):
            print(folder, os.path.exists(zip_dataset_path), "moved")
            file_utils.shift_file_objects(zip_dataset_path, blank_page_dir)
        else:
            print(folder, os.path.exists(zip_dataset_path), "failed")
            status.append(folder) 
    
    log_dir = f"cat_logs/{date}"
    file_utils.check_and_generate_new_dir(log_dir)

    output_path = os.path.join(log_dir, f"{date}_{new_dir}_categorization_failed.txt")
    file_utils.export_output_as_txt_file(output_path, status)
    return output_path


def is_also_potentially_blank_by_other_files(log_dir_path, filtered_out_dataset, date, type):
    print("Cross checking that filtered files have blank screenshots...")
    status = {}

    # Cross check against logs for screenshot
    ss_aft_blank_list = read_blank_files_as_list(os.path.join(log_dir_path, f"{date}_ss_aft_blank_{type}.txt"))

    # Return a dict {dataset_name: {css: true/false, js: true/false, ss_aft: true/false}}
    for filtered in filtered_out_dataset:
        is_ss_aft_blank = False

        if filtered in ss_aft_blank_list:
            is_ss_aft_blank = True
        
        data = {
            "Is blank by ss (after)": is_ss_aft_blank
        }

        status[filtered] = data
    
    log_dir = f"cat_logs/{date}"
    output_path = os.path.join(log_dir, f"{date}_cat_cross_check_ss_{type}.json")
    file_utils.export_output_as_json_file(output_path, status)


def potentially_blank_not_filtered_yet(log_dir_path, filtered_dataset, date, type):
    print("Checking if filtered files are also potentially blank by other file types...")
    ss_aft_blank_list = read_blank_files_as_list(os.path.join(log_dir_path, f"{date}_ss_aft_blank_{type}.txt"))

    # Remove from ss_aft blank list/log files those that are already filtered
    for filtered in filtered_dataset:
        if filtered in ss_aft_blank_list:
            ss_aft_blank_list.remove(filtered)

    # Return a new log with the remaining unfiltered ones
    log_dir = f"cat_logs/{date}"
    output_file = os.path.join(log_dir, f"{date}_unfiltered_extra_ss_blank_{type}.txt")
    file_utils.export_output_as_txt_file(output_file, ss_aft_blank_list)


def shift_logs_files(date, src_dir):
    print(f"Shifting {src_dir} log files...")
    logs_dir = os.path.join(f"dataset_{date}", f"dataset_{date}", f"dataset_{date}", "complete_dataset", "blank_pages", "logs", src_dir)
    file_utils.check_and_generate_new_dir(logs_dir)
    
    for file in os.listdir(os.path.join(src_dir, date)):
        src_file_path = os.path.join(os.path.join(src_dir, date), file)
        if os.path.exists(src_file_path):
            dest_file_path = os.path.join(logs_dir, file)
            file_utils.shift_file_objects(src_file_path, dest_file_path)
        else:
            print(f"File {file} does not exist!")
    

def clean_up_logs(date):
    log_files_folder = [f'primary_logs', f'cat_logs']
    for folder in log_files_folder:
        shift_logs_files(date, folder)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("date", help="Date")
    parser.add_argument("folder_path", help="Folder name")
    parser.add_argument("blank_txt", help="Blank Page File")
    #parser.add_argument("new_dir", help="Name of dir to keep blank dataset")
    args = parser.parse_args()

    # Single
    types = ["both", "self_ref", "no_ref"]
    for t in types:
        log_dir_path = os.path.join("primary_logs", args.date)
        blank_txt_path = os.path.join(log_dir_path, f"{args.date}_{args.blank_txt}_{t}.txt")
        blank_page_list = read_blank_files_as_list(blank_txt_path)

        if t != "both":
            folder_path = args.folder_path.replace(".zip", "")
        else:
            folder_path = args.folder_path
        unsuccessful_filtered_path = filter_out_blank_page_by_html(args.date, folder_path, blank_page_list, "both")

        unsuccessful_filtered = read_blank_files_as_list(unsuccessful_filtered_path)
        filtered = [item for item in blank_page_list if item not in unsuccessful_filtered]
        is_also_potentially_blank_by_other_files(log_dir_path, filtered, args.date, "both")
        potentially_blank_not_filtered_yet(log_dir_path, filtered, args.date, "both")
    
    clean_up_logs(args.date)

