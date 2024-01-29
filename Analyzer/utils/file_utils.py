import json
import os 
import shutil
import zipfile

# Unzips a zipped folder 
# Param: zip_folder (e.g. folder.zip)
# Returns: extraction_path (e.g. folder)
def extract_zipfile(zip_folder):
    extraction_path = zip_folder.replace('.zip', '')

    with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
        print("\nExtracting zip folder ...")
        zip_ref.extractall(extraction_path)
    
    return extraction_path


# Remove zip folder that was extracted previously
def remove_extracted_folder(extraction_path):
    shutil.rmtree(extraction_path)


# Returns the date of the extracted folder name (e.g. folder_date)
def extract_date_from_extracted_zipfile_name(extracted_zip_file_name):
    date = extracted_zip_file_name.split('_')[-1]
    return date


# Shift object from src to dest folder
def shift_file_objects(src_folder, dest_folder):
    shutil.move(src_folder, dest_folder)


# Checks the the new directory exists
# Otherwise create the new directory
def check_and_generate_new_dir(new_dir_path):
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)


# Reads and return the data in the json file
def read_data_from_json_file(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data


# Exports the data as a json file
def export_output_as_json_file(output_file_name, output_data):
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)


# Exports the data as a txt file
def export_output_as_txt_file(output_file_name, output_data):
    with open(output_file_name, 'w') as f:
        for item in output_data:
            f.write(str(item) + '\n')

def test():
    print("test")