import argparse

import utils
import url_scanner

def read_url_from_file(txt_file):
    with open(txt_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("txt_file", help="Name of the txt file that contains urls to validate")
    parser.add_argument("date", help="Date of dataset")
    args = parser.parse_args()

    api_key_file = 'virus_total_api_key.txt'
    api_key = utils.read_virus_total_api_key(api_key_file)

    urls_list = read_url_from_file(args.txt_file)
    url_scanner.url_scanner(args.original_dataset_folder_path, args.date, api_key)
    

