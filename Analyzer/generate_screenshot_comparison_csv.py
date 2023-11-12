import json
import pandas as pd
import csv

def func(json_data_file, file_hash_order_txt, date):
    with open(json_data_file, 'r') as file:
        json_data = json.load(file)
    
    with open(file_hash_order_txt, 'r') as file:
        file_hash_order = [line.strip() for line in file]

    csv_data = []
    for hash_key in file_hash_order:
        if hash_key in json_data:
            row = [hash_key] + list(json_data[hash_key].values())
            csv_data.append(row)
    
    headers = ["File Hash", "(Self Ref) pHash Difference", "(Self Ref) dHash Difference", "(No Ref) pHash Difference", "(No Ref) dHash Difference"]


    with open(f'{date}_screenshot_hash_comparison.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(csv_data)


func('011123_screenshot_hashes.json', '011123_hash_order.txt', '011123')