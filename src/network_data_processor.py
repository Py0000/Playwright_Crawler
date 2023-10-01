import json
import os
import shutil

import util
import util_def

# Checks if har log file exists in the initial folder 
# If else, obtain all the request and response details from it and return
def obtain_file_details_from_har_log(har_file_path):
    response_file_to_entry_map = None 
    request_file_to_entry_map = None

    if os.path.exists(har_file_path):
        with open(har_file_path, 'r') as f:
            har_data = json.load(f)
            response_file_to_entry_map = {entry['response']['content'].get('_file'): entry for entry in har_data['log']['entries'] if '_file' in entry['response']['content']}
            request_file_to_entry_map = {entry['request']['content'].get('_file'): entry for entry in har_data['log']['entries'] if '_file' in entry['request'].get('content', {})}
        f.close()

    return response_file_to_entry_map, request_file_to_entry_map


def cleanup_initial_data_folder(initial_network_data_path, har_file_path, ref_specific_dataset_path, sub_folder):
    # Move the har log path out of initial_network_data folder
    main_url_folder = os.path.join(ref_specific_dataset_path, sub_folder)            
    shutil.move(har_file_path, main_url_folder)

    # Delete the initial_network_data folder
    shutil.rmtree(initial_network_data_path)


def move_file(response_data_path, request_data_path, response_file_to_entry_map, ind_data_file_path, ind_data_filename):
    # Check if it is a response datafile
    # If it is move the file to the network_response_data_folder
    response_matched_entry = response_file_to_entry_map.get(ind_data_filename)
    if response_matched_entry:
        shutil.move(ind_data_file_path, os.path.join(response_data_path, ind_data_filename))
    
    # Otherwise, it is network request related datafile, move it to network_request_data_folder
    else:
        shutil.move(ind_data_file_path, os.path.join(request_data_path, ind_data_filename))


def process_network_data(ref_specific_dataset_path):
    print("\nProcessing network data")
    # Get all the sub-folders in the dataset/self_ref or dataset/no_ref folders
    # Each sub_folder contains information for each url link
    sub_folders = [d for d in os.listdir(ref_specific_dataset_path) if os.path.isdir(os.path.join(ref_specific_dataset_path, d))]

    # loop through each sub folders (i.e. 0, 1, 2, 3, ... )
    for sub_folder in sub_folders:
        # Get the path of the folder that contains all the network data initially. This folder is to be removed after processing the network data.
        network_data_path = os.path.join(ref_specific_dataset_path, sub_folder, util_def.FOLDER_NETWORK_FRAGMENTS)

        # Generate the paths to restore the request data and response data respectively after processing
        response_data_path = os.path.join(ref_specific_dataset_path, sub_folder, util_def.FOLDER_NETWORK_RESPONSE_FRAGMENTS)
        request_data_path = os.path.join(ref_specific_dataset_path, sub_folder, util_def.FOLDER_NETWORK_REQUEST_FRAGMENTS)

        # Checks that the initial folder (i.e. initial_network_data) exists
        if os.path.exists(network_data_path):
            # Get the har log file path
            har_file_path = os.path.join(network_data_path, util_def.FILE_NETWORK_HAR)
            response_file_to_entry_map, request_file_to_entry_map = obtain_file_details_from_har_log(har_file_path)

            # Loop through each file in initial_network_data folder
            for ind_data_filename in os.listdir(network_data_path):
                # Get the filepath for each datafile in the folder    
                ind_data_file_path = os.path.join(network_data_path, ind_data_filename)

                # Skip processing the har log file
                if ind_data_file_path == har_file_path:
                    continue
                
                move_file(response_data_path, request_data_path, response_file_to_entry_map, ind_data_file_path, ind_data_filename)
                

            cleanup_initial_data_folder(network_data_path, har_file_path, ref_specific_dataset_path, sub_folder)

    print("Done processing network data")



def start_network_processing(dataset_folder):
    ref_specific_path = os.path.join(dataset_folder, util.get_crawled_dataset_base_folder_name(True))
    process_network_data(ref_specific_path)
    no_ref_specific_path = os.path.join(dataset_folder, util.get_crawled_dataset_base_folder_name(False))
    process_network_data(no_ref_specific_path)
