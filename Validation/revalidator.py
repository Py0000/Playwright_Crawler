import argparse
import requests
import time
import csv

# Read the VirusTotal API key from a txt file
def read_virus_total_api_key(key_file):
    with open(key_file, 'r') as file:
        api_key = file.readline().strip()
    
    return api_key


def read_urls_for_rescanning(url_file):
    with open(url_file, 'r') as file:
        urls = file.readlines()

    urls = [url.strip() for url in urls]

    return urls


def rescan_url(url_lists, api_key):
    consolidate_data = {}
    headers = {'x-apikey': api_key}

    count = 1
    for url in url_lists:
        print(f"\nRe-Analyzing Url #{count}...")
        print(f"Url: {url}")
        response = requests.post('https://www.virustotal.com/api/v3/urls', headers=headers, data={'url': url})

        if response.status_code == 200:
            # Extract the analysis ID from the rescan response
            url_id = response.json()['data']['id']

            reanalyze_response = requests.post(
                f'https://www.virustotal.com/api/v3/urls/{url_id}/analyse',
                headers=headers
            )

            if reanalyze_response.status_code == 200:
                url_id = reanalyze_response.json()['data']['id']
                vendors_flagged_red, vendor_of_interest_status = get_reanalyzed_report(url_id, api_key)

                current_data = {
                    "Website URL": url,
                    "# Vendors Flagged Red": vendors_flagged_red,
                    "OpenPhish": vendor_of_interest_status["OpenPhish"],
                    "Google Safebrowsing": vendor_of_interest_status["Google Safebrowsing"],
                    "Kaspersky": vendor_of_interest_status["Kaspersky"],
                    "Trustwave": vendor_of_interest_status["Trustwave"]
                }

                consolidate_data[url] = current_data

            else:
                print(f"URL: {url} - Error: {reanalyze_response.text}")
                consolidate_data[hash] = f"Error: {reanalyze_response.text}"
        else:
            print(f"Request for reanalysis failed. Error: {response.text}")

        count = count + 1

    return consolidate_data


def get_reanalyzed_report(url_id, api_key):
    max_attempt = 5
    report_url = f'https://www.virustotal.com/api/v3/analyses/{url_id}'
    for attempt in range(max_attempt):
        response = requests.get(report_url, headers={'x-apikey': api_key})
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


def generate_csv_report(validation_data_dict, date):
    print("Generating CSV Report....")
    data_list = [v for _, v in validation_data_dict.items()]
    headers = data_list[0].keys()

    with open(f"{date}_revalidation.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("url_file", help="Name of the original dataset folder path")
    parser.add_argument("date", help="Date of dataset")
    args = parser.parse_args()

    api_key_file = 'virus_total_api_key.txt'
    api_key = read_virus_total_api_key(api_key_file)

    url_lists = read_urls_for_rescanning(args.url_file)

    data = rescan_url(url_lists, api_key)
    generate_csv_report(data, args.date)


