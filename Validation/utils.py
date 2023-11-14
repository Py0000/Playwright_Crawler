import os
import csv

def generate_csv_report(validation_data_dict, file_name):
    print("Generating CSV Report....")
    data_list = [v for _, v in validation_data_dict.items()]
    headers = data_list[0].keys()

    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)


def generate_file_path(parent_directory, data_folder, file_type):
    REF_FOLDER = 'self_ref'
    file_path = os.path.join(parent_directory, data_folder, REF_FOLDER, file_type)
    if not os.path.exists(file_path):
        file_path = os.path.join(parent_directory, data_folder, os.path.basename(data_folder) , REF_FOLDER, file_type)
    
    return file_path
