import json
import os 
import zipfile

import faulty_data_filter

def consolidate_reponse_status(dataset_directory, date):
    consolidated_response_status = {}
    complete_dataset_full_dir = os.path.join(dataset_directory, "complete_dataset")
    complete_datasets = os.listdir(complete_dataset_full_dir)
    for folder in complete_datasets:
        if folder.endswith(".zip"):
            zip_file_path = os.path.join(dataset_directory, folder)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                file_path = faulty_data_filter.obtain_real_file_path(zip_file, zip_file_path, folder)

                response_status = {}
                for config_folder in faulty_data_filter.CONFIG_FOLDERS:
                    log_file_path = os.path.join(file_path, config_folder, faulty_data_filter.LOG_FILE_NAME)
                    log_data = faulty_data_filter.get_log_file_data(log_file_path, zip_file)
                    if log_data != None:
                        response_status_code = log_data["Status"]
                        response_status[config_folder] = response_status_code
            
            consolidated_response_status[folder] = response_status
    
    output_path = f"{date}_response_code_status.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(consolidated_response_status, f, ensure_ascii=False, indent=4)


