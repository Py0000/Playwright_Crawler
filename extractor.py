import datetime

import features_extraction as fe
import utility as util
 

def extract_webpage(config):
    base_folder_name = f'data_{config}'
    util.generate_extractor_analysis_folder(base_folder_name)
    
    file_date = datetime.date.today().strftime("%Y%m%d")
    file_time = datetime.datetime.now().time().strftime("%H%M%S")
    file_name = f"{file_date}_{file_time}"
    
    crawled_data_dir = f"{util.CRAWLED_DATA_IDENTIFIER}_{config}"
    crawled_urls = util.read_urls_from_file(crawled_data_dir)

    print("\nExtracting Data ...")
    fe.extract_features(file_name, base_folder_name, crawled_data_dir, crawled_urls)
    print("\nData Extracted ... \n")


extract_webpage(util.CONFIG_DESKTOP_USER)