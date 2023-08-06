import certificate_analyzer as ca
import dns_analyzer as da
import features_analyzer as fa
import utility as util

def analyze_extracted_data(base_folder_name):
    print("Analyzing Data ... \n")

    fa.analyze_features_df(base_folder_name)
    ca.analyze_certificate_df(base_folder_name)
    da.analyze_DNS_df(base_folder_name)

    print("Analysis Done ... \n")