import json
import os
import shutil

import util
import util_def

def start_network_processing(dataset_folder):
    ref_specific_path = os.path.join(dataset_folder, util.get_crawled_dataset_base_folder_name(True))
    process_network_data(ref_specific_path)
    no_ref_specific_path = os.path.join(dataset_folder, util.get_crawled_dataset_base_folder_name(False))
    process_network_data(no_ref_specific_path)

def process_network_data(ref_specific_dataset_path):
    print("Processing network data")
    # Get all the sub-folders in the dataset/self_ref or dataset/no_ref folders
    # Each sub_folder contains information for each url link
    sub_folders = [d for d in os.listdir(ref_specific_dataset_path) if os.path.isdir(os.path.join(ref_specific_dataset_path, d))]

    for sub_folder in sub_folders:
        network_data_path = os.path.join(ref_specific_dataset_path, sub_folder, util_def.FOLDER_NETWORK_FRAGMENTS)
        response_fragment_path = os.path.join(ref_specific_dataset_path, sub_folder, util_def.FOLDER_NETWORK_RESPONSE_FRAGMENTS)
        request_fragment_path = os.path.join(ref_specific_dataset_path, sub_folder, util_def.FOLDER_NETWORK_REQUEST_FRAGMENTS)
        if os.path.exists(network_data_path):
            har_file_path = os.path.join(network_data_path, util_def.FILE_NETWORK_HAR)
            if os.path.exists(har_file_path):
                with open(har_file_path, 'r') as f:
                    har_data = json.load(f)

                    response_file_to_entry_map = {entry['response']['content'].get('_file'): entry for entry in har_data['log']['entries'] if '_file' in entry['response']['content']}
                    request_file_to_entry_map = {entry['request']['content'].get('_file'): entry for entry in har_data['log']['entries'] if '_file' in entry['request'].get('content', {})}

                    for network_data_filename in os.listdir(network_data_path):
                        network_data_file_path = os.path.join(network_data_path, network_data_filename)

                        if network_data_file_path == har_file_path:
                            continue

                        response_matched_entry = response_file_to_entry_map.get(network_data_filename)
                        if response_matched_entry:
                            shutil.move(network_data_file_path, os.path.join(response_fragment_path, network_data_filename))

                        else:
                            shutil.move(network_data_file_path, os.path.join(request_fragment_path, network_data_filename))

                f.close()
                shutil.move(har_file_path, os.path.join(ref_specific_dataset_path, sub_folder))

            shutil.rmtree(network_data_path)
    print("Done processing network data")
