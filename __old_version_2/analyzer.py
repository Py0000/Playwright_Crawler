import certificate_analyzer 
import dns_analyzer 
import features_analyzer 
import definitions

def analyze_extracted_data(base_folder_name):
    print("Analyzing Data ... \n")

    features_analyzer.analyze_features_df(base_folder_name, definitions.OUTPUT_PATH_EXCEL_FEATURES_AFTER)
    features_analyzer.analyze_features_df(base_folder_name, definitions.OUTPUT_PATH_EXCEL_FEATURES_BEFORE)
    certificate_analyzer.analyze_certificate_df(base_folder_name)
    dns_analyzer.analyze_DNS_df(base_folder_name)

    print("Analysis Done ... \n")

