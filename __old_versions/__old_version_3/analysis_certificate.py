import json
import os

import pandas as pd

import util_def

def extract_data_from_json(json_data):
    data = {
        "Website": json_data.get("website url"),
        "Hostname": json_data.get("hostname"),
        "Certificate Subject (Common Name)": json_data.get("subject", {}).get("commonName", ""),
        "Certificate Subject (Organization)": json_data.get("subject", {}).get("organizationName", ""),
        "Certificate Subject (Locality or City)": json_data.get("subject", {}).get("localityName", ""),
        "Certificate Subject (State or Province)": json_data.get("subject", {}).get('stateOrProvinceName', ''),
        "Certificate Subject (Country)": json_data.get("subject", {}).get("countryName", ""),
        "Certificate Subject (Business Category)": json_data.get("subject", {}).get("businessCategory", ""),
        "Certificate Subject (Serial No.)": json_data.get("subject", {}).get("serialNumber", ""),
        "Certificate Subject (Jurisdiction State)": json_data.get("subject", {}).get("jurisdictionState", ""),
        "Certificate Subject (Jurisdiction Locality)": json_data.get("subject", {}).get("jurisdictionLocality", ""),
        "Certificate Issuer (Country Name)": json_data.get("issuer", {}).get("countryName", ""),
        "Certificate Issuer (Organization Name)": json_data.get("issuer", {}).get("organizationName", ""),
        "Certificate Issuer (Organizational Unit Name)": json_data.get("issuer", {}).get("organizationalUnitName", ""),
        "Certificate Issuer (Common Name)": json_data.get("issuer", {}).get("commonName", ""),
        "Certificate Version": json_data.get("version", ""),
        "Certificate Valid From": json_data.get("not_before", ""),
        "Certificate Valid Until": json_data.get("not_after", ""),
        "Certificate Valid Duration": json_data.get("period", ""),
        "Certificate Serial Number": json_data.get("serial_number", ""),
        "Certificate Signature Algorithm": json_data.get("signature_algo", ""),
        "SSL/TLS Protocol Version": json_data.get("protocol_version", ""),
    }

    return pd.DataFrame([data])    

def consolidate_cert_from_json_to_excel(device_conf, ref_flag, act_flag):
    ref = util_def.REF_SET if ref_flag else util_def.NO_REF_SET
    act = util_def.USER_ACT_SET if act_flag else util_def.NO_USER_ACT_SET

    group_data = {}

    base_folder = os.path.join(util_def.DATA_FOLDER, f"{device_conf}_{ref}_{act}")
    for dirpath, _, filenames in os.walk(base_folder):
        if util_def.TLS_CERT_FILE in filenames:
            group_prefix = dirpath.split(os.sep)[-1].split('-')[0] # Extract prefix like 0, 1, etc.
            file_path = os.path.join(dirpath, util_def.TLS_CERT_FILE)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            current_df = extract_data_from_json(data)
            
            if group_prefix not in group_data:
                group_data[group_prefix] = pd.DataFrame()
            group_data[group_prefix] = pd.concat([group_data[group_prefix], current_df], ignore_index=True)

    
    output_folder = os.path.join(util_def.ANALYSIS_FOLDER, f"{device_conf}_{ref}_{act}")
    for group, df in group_data.items():
        output_filename = f"{group}_{util_def.CERT_CONSOLIDATED_EXCEL}"
        df.drop_duplicates(subset=["Website"], keep="first", inplace=True)
        df.to_excel(os.path.join(output_folder, output_filename), index=False)
    



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


def analyze_certificate_df(device_conf, ref_flag, act_flag):
    print("Analysing Certificate Data...")

    consolidate_cert_from_json_to_excel(device_conf, ref_flag, act_flag)

    consolidated_counts = {}

    ref = util_def.REF_SET if ref_flag else util_def.NO_REF_SET
    act = util_def.USER_ACT_SET if act_flag else util_def.NO_USER_ACT_SET
    directory = os.path.join(util_def.ANALYSIS_FOLDER, f"{device_conf}_{ref}_{act}")
    
    for file in os.listdir(directory):
        if file.endswith(util_def.CERT_CONSOLIDATED_EXCEL):
            consolidated_counts = {}
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

            group_prefix = file.split("_")[0]
            output_file_path = os.path.join(directory, f"{group_prefix}_{util_def.CERT_CONSOLIDATED_JSON}")
            with open(output_file_path, 'w') as json_file:
                json.dump(consolidated_counts, json_file, indent=4)
    
    print("Done analysing Certificate Data...")


#analyze_certificate_df(util_def.DESKTOP_USER, util_def.REF_SET, util_def.USER_ACT_SET)