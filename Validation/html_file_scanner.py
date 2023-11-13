import os
import requests
import time
import json
import csv

def get_html_files_for_scanning(original_dataset_path):
    html_data = {}

    folders = os.listdir(original_dataset_path)
    for folder in folders:
        # Account for different zipping and unzipping structure
        html_file_path = os.path.join(original_dataset_path, folder, 'self_ref', 'html_script_aft.html')
        if not os.path.exists(html_file_path):
            html_file_path = os.path.join(original_dataset_path, folder, os.path.basename(folder) , 'self_ref', 'html_script_aft.html')


        with open(html_file_path, 'rb') as file:
            html_content = file.read()
        
        files = {
            'file': ('filename.html', html_content)
        }

        html_data[os.path.basename(folder)] = files

    return html_data


def scan_html_file(html_data_list, api_key):
    consolidate_data = {}
    headers = {'x-apikey': api_key}

    count = 1
    for hash, file in html_data_list.items():
        print(f"\nScanning File #{count}...")
        # Send each url for scanning on VirusTotal
        response = requests.post(
            'https://www.virustotal.com/api/v3/files', 
            headers=headers, 
            files=file
        )

        print(response.status_code)
        if response.status_code == 200:
            analysis_id = response.json()['data']['id']
            vendors_flagged_red = get_html_analysis_report(analysis_id, api_key)

            current_data = {
                "Direct HTML Script Analysis by VirusTotal": vendors_flagged_red
            }

            consolidate_data[hash] = current_data
        
        else:
            print(f"Error: {response.text}")
        
        count += 1

    return consolidate_data



def get_html_analysis_report(analysis_id, api_key):
    max_attempt = 5
    for attempt in range(max_attempt):
        response = requests.get(
            f'https://www.virustotal.com/api/v3/analyses/{analysis_id}',
            headers={'x-apikey': api_key}
        )

        report = response.json()
        is_ready = report.get('data', {}).get('attributes', {}).get('status', 'unknown') == 'completed'
        if is_ready:
            return extract_total_value(report)
        else:
            time.sleep((attempt + 2) * 3)


def extract_total_value(report):
    # Contains the status of each security vendor for the submitted url
    results = report["data"]["attributes"]["results"]
    num_of_vendors = len(results)

    flagged_count = 0
    for vendor in results.values():
        if vendor['result'] != None:
            flagged_count += 1
    
    vendors_flagged_red = f'="{flagged_count}/{num_of_vendors}"'
    print(vendors_flagged_red)
    return vendors_flagged_red

"""
def generate_csv_report(validation_data_dict, date):
    print("Generating CSV Report....")
    data_list = [v for _, v in validation_data_dict.items()]
    headers = data_list[0].keys()

    with open(f"{date}_html_validation.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)
"""

def html_file_scanner(original_dataset_folder_path, date, api_key):
    html_data_list = get_html_files_for_scanning(original_dataset_folder_path)
    validation_data = scan_html_file(html_data_list, api_key)
    # generate_csv_report(validation_data, date)
    return validation_data