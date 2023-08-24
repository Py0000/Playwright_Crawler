import datetime

import certificate_extraction 
import dns_extraction 
import features_extraction 
import definitions
 

def extract_webpage(base_folder_name, config):
    file_date = datetime.date.today().strftime("%Y%m%d")
    file_time = datetime.datetime.now().time().strftime("%H%M%S")
    file_name = f"{file_date}_{file_time}"
    
    config_dir = f"{definitions.MAIN_CRAWLING_FOLDER}_{config}"

    print("\nExtracting Data ...")
    features_extraction.extract_features(file_name, base_folder_name, config_dir)
    certificate_extraction.extract_certificates(file_name, base_folder_name, config_dir)
    dns_extraction.generate_dns_records(file_name, base_folder_name, config_dir)
    print("\nData Extracted ... \n")