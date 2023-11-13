import requests
import os
import json
import csv
import time



# Folder will be the orginal_dataset_{date} folder used for screenshot comparision as well
def get_url_to_validate(original_dataset_path):
    print("Getting urls for scanning...")
    # Gets the url to be used for validation
    url_to_file_hash_dict = {}

    # Loop through the list of zipped dataset folders
    folders = os.listdir(original_dataset_path)
    for folder in folders:
        # Account for different zipping and unzipping structure
        log_file_path = os.path.join(original_dataset_path, folder, 'self_ref', 'log.json')
        if not os.path.exists(log_file_path):
            log_file_path = os.path.join(original_dataset_path, folder, os.path.basename(folder) , 'self_ref', 'log.json')
        
        # Get the url of the feed as well as the file hash
        with open(log_file_path, 'r') as file:
            data = json.load(file)
        url = data["Provided Url"]
        hash_value = data["Provided Url Hash (in SHA-256)"]

        url_to_file_hash_dict[url] = hash_value
    
    return url_to_file_hash_dict


# Submits url to be scan in VirusTotal
def scan_url(url_to_file_hash_dict, api_key):
    consolidate_data = {}

    # VirusTotal API key (required to use the VirusTotal API)
    headers = {'x-apikey': api_key}

    # Loop through the selected url 
    count = 1
    for url, hash in url_to_file_hash_dict.items():
        print(f"\nScanning Url #{count}...")
        print(f"Url: {url}")
        # Send each url for scanning on VirusTotal
        response = requests.post(
            'https://www.virustotal.com/api/v3/urls', 
            headers=headers, 
            data={'url': url}
        )
        
        if response.status_code == 200:
            # Get the scan report id for this url
            url_id = response.json()['data']['id']

            # Extract the information we are interested in from the scan report
            vendors_flagged_red, vendor_of_interest_status = get_url_analysis_report(url_id, api_key)

            current_data = {
                "File Hash": hash,
                "Website URL": url,
                "# Vendors Flagged Red": vendors_flagged_red,
                "OpenPhish": vendor_of_interest_status["OpenPhish"],
                "Google Safebrowsing": vendor_of_interest_status["Google Safebrowsing"],
                "Kaspersky": vendor_of_interest_status["Kaspersky"],
                "Trustwave": vendor_of_interest_status["Trustwave"]
            }
            
            consolidate_data[hash] = current_data

        else:
            print(f"URL: {url} - Error: {response.text}")
            consolidate_data[hash] = f"Error: {response.text}"
        
        count = count + 1
        
    return consolidate_data


# Get the scan analysis report
def get_url_analysis_report(url_id, api_key):
    max_attempt = 5
    for attempt in range(max_attempt):
        response = requests.get(
            f'https://www.virustotal.com/api/v3/analyses/{url_id}',
            headers={'x-apikey': api_key}
        )

        time.sleep(2)
        report = response.json()

        openphish_results = report.get("data", {}).get("attributes", {}).get("results", {}).get("OpenPhish")
        gsb_results = report.get("data", {}).get("attributes", {}).get("results", {}).get("Google Safebrowsing")
        kaspersky_results = report.get("data", {}).get("attributes", {}).get("results", {}).get("Kaspersky")
        trustwave_results = report.get("data", {}).get("attributes", {}).get("results", {}).get("Trustwave")
        is_interested_available = openphish_results is not None and gsb_results is not None and kaspersky_results is not None and trustwave_results is not None

        if is_interested_available:
            # Extracts the relevant data that we are interested in
            return extract_relevant_data_from_analysis_report(report)

        time.sleep((attempt + 1) * 3)




def extract_relevant_data_from_analysis_report(report):
    vendor_of_interest = ["OpenPhish", "Google Safebrowsing", "Kaspersky", "Trustwave"]
    
    # Contains the status of each security vendor for the submitted url
    results = report["data"]["attributes"]["results"]
    num_of_vendors = len(results)

    phishing_count = 0
    for vendor in results.values():
        if vendor['result'] == 'phishing':
            phishing_count += 1

    # Check the status of the 4 vendors we are interested in
    vendor_of_interest_status = {}
    for vendor in vendor_of_interest:
        if vendor in results:
            vendor_result = results[vendor]
            status = vendor_result['result']
            vendor_of_interest_status[vendor] = status.capitalize()

    vendors_flagged_red = f'="{phishing_count}/{num_of_vendors}"'

    print(vendors_flagged_red)
    print(vendor_of_interest_status)
    return vendors_flagged_red, vendor_of_interest_status


"""
def generate_csv_report(validation_data_dict, date):
    print("Generating CSV Report....")
    data_list = [v for _, v in validation_data_dict.items()]
    headers = data_list[0].keys()

    with open(f"{date}_url_validation.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)
"""


def url_scanner(original_dataset_folder_path, date, api_key):
    url_to_file_hash_dict = get_url_to_validate(original_dataset_folder_path)
    validation_data = scan_url(url_to_file_hash_dict, api_key)
    #generate_csv_report(validation_data, date)
    return validation_data

