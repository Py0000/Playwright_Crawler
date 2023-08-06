import json
import os
import pandas as pd

import utility as util


def analyze_cert_duration_column(df, column, counts_dict):
    filtered_df = df.loc[df[column] != "Connection Error"]
    largest_value = filtered_df[column].max()
    smallest_value = filtered_df[column].min()
    range = str(smallest_value) + " to " + str(largest_value)
    counts_dict["Range"] = range

    return counts_dict


def analyze_other_columns(column, counts, counts_dict, consolidated_counts):
    # Find the highest count value
    max_count_value = counts.max()

    # Find all items with the highest count
    highest_count_items = counts[counts == max_count_value].index.tolist()

    if len(highest_count_items) == 1:
        highest_count_items = highest_count_items[0]
    else:
        # Convert the highest_count_items to a list of strings
        highest_count_items = [str(item) for item in highest_count_items]
        
    counts_dict["Most common item"] = highest_count_items

    # Include the highest count in the dictionary
    consolidated_counts[column] = counts_dict

    return consolidated_counts
    


def analyze_certificate_df(base_folder_name):
    print("Analysing Certificate Data...")

    folder_name = f"{base_folder_name}/{util.OUTPUT_PATH_EXCEL_CERTS}"
    directory = os.path.join(os.getcwd(), folder_name)

    for file in sorted(os.listdir(directory)):
        file_name = util.get_file_name_without_ext(file)

        consolidated_counts = {}
        consolidated_counts["File Name"] = file_name

        df = pd.read_excel(os.path.join(directory, file))

        for column in df.columns:
            isCertIssuerOrg = column == "Certificate Issuer (Organization Name)"
            isCertDuration = column == "Certificate Valid Duration"
            isCertProtocol = column == "SSL/TLS Protocol Version"
            isCertSigAlgo = column == "Certificate Signature Algorithm"
            isCertVer = column == "Certificate Version"
            isCertCommonName = column == "Certificate Subject (Common Name)"
            
            if isCertIssuerOrg or isCertDuration or isCertProtocol or isCertSigAlgo or isCertVer or isCertCommonName:
                counts = df[column].value_counts()
                # Convert the Pandas Series to a dictionary before saving
                counts_dict = counts.to_dict()
                consolidated_counts[column] = counts_dict

                if isCertDuration: 
                    analyze_cert_duration_column(df, column, counts_dict)

                else:
                    analyze_other_columns(column, counts, counts_dict, consolidated_counts)
    

    output_file = f"{base_folder_name}/{util.OUTPUT_PATH_ANALYSIS_CERTS}{file_name}_analysis.json"
    with open(output_file, 'w') as json_file:
            json.dump(consolidated_counts, json_file, indent=4)    


    print("Done analysing Certificate Data...")


