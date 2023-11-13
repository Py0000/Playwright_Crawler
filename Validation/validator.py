import argparse
import csv
import os
import zipfile

import url_scanner
import html_file_scanner

# Read the VirusTotal API key from a txt file
def read_virus_total_api_key(key_file):
    with open(key_file, 'r') as file:
        api_key = file.readline().strip()
    
    return api_key


# Unzip the 10-30 dataset crawled (to be used for validation using VirusTotal)
def unzip_folder(zip_folder_path):
    if not (os.path.isfile(zip_folder_path) and zip_folder_path.endswith('.zip')):
        print("The provided path does not point to a zip file.")
    
    # Extracts the files to the same directory as the zip file
    extracted_folder_path = os.path.splitext(zip_folder_path)[0]
    with zipfile.ZipFile(zip_folder_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder_path)

    os.remove(zip_folder_path)
    return extracted_folder_path


def unzip_original_dataset_folder(original_dataset_path):
    print("Unzipping folders...")
    folders = os.listdir(original_dataset_path)
    for folder in folders:
        zipped_original_folder_path = os.path.join(original_dataset_path, folder)
        unzip_folder(zipped_original_folder_path)


def consolidate_validation_data(url_validation_data, html_validation_data):
    for hash_key, analysis_data in html_validation_data.items():
        print(f"Hash: {hash_key}. Matched? {hash_key in url_validation_data}")
        if hash_key in url_validation_data:
            url_validation_data[hash_key].update(analysis_data)
    return url_validation_data

"""
def generate_csv_report(validation_data_dict, date):
    print("Generating CSV Report....")
    data_list = [v for _, v in validation_data_dict.items()]
    headers = data_list[0].keys()

    with open(f"{date}_validation.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("original_dataset_folder_path", help="Name of the original dataset folder path")
    parser.add_argument("date", help="Date of dataset")
    args = parser.parse_args()

    api_key_file = 'virus_total_api_key.txt'
    api_key = read_virus_total_api_key(api_key_file)

    unzip_original_dataset_folder(args.original_dataset_folder_path)
    #url_scanner.url_scanner(args.original_dataset_folder_path, args.date, api_key)
    html_file_scanner.html_file_scanner(args.original_dataset_folder_path, args.date, api_key)
    #consolidate_validation_data(url_validation_data, html_validation_data)
    #generate_csv_report(url_validation_data, args.date)


