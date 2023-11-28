import json
import os
import shutil 



def read_faulty_files_as_list(txt_file):
    with open(txt_file, "r") as f: 
        faulty_folder_names = f.readlines()
    
    # Remove newline characters and any whitespace
    faulty_folder_list = [folder_name.strip() for folder_name in faulty_folder_names]

    return faulty_folder_list


def categorize(date, dataset_path, both_faulty_txt, new_dir):
    status = {}

    faulty_both_path = os.path.join(dataset_path, new_dir)
    if not os.path.exists(faulty_both_path):
        os.makedirs(faulty_both_path)

    both_faulty_folder_names = read_faulty_files_as_list(both_faulty_txt)

    for folder in both_faulty_folder_names:
        zip_folder_path = os.path.join(dataset_path, folder)

        if (os.path.exists(zip_folder_path)):
            shutil.move(zip_folder_path, faulty_both_path)
            status[folder] = "Categorized"
        else:
            status[folder] = "Failed"

    output_path = f"{date}_{new_dir}_categorization_status.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)

