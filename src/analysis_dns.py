import json
import os

import pandas as pd

import util
import util_def

NO_RECORDS_FLAG = "No records found"
DNS_EXCEPTION = "DNS Exception occurred"
ERROR_RESULTS = [[NO_RECORDS_FLAG], [DNS_EXCEPTION]]

def extract_data_from_json(json_data, dirpath):
    domain = json_data.get("Domain", "")
    has_A_records = True if json_data.get("A") not in ERROR_RESULTS else False
    has_AAAA_records = True if json_data.get("AAAA") not in ERROR_RESULTS else False
    has_CAA_records = True if json_data.get("CAA") not in ERROR_RESULTS else False
    has_CNAME_records = True if json_data.get("CNAME") not in ERROR_RESULTS else False
    has_MX_records = True if json_data.get("MX") not in ERROR_RESULTS else False
    has_NS_records = True if json_data.get("NS") not in ERROR_RESULTS else False
    has_SOA_records = True if json_data.get("SOA") not in ERROR_RESULTS else False
    has_TXT_records = True if json_data.get("TXT") not in ERROR_RESULTS else False

    data = {
        "Domain": [domain],
        "has_A_records": [has_A_records],
        "has_AAAA_records": [has_AAAA_records],
        "has_CAA_records": [has_CAA_records],
        "has_CNAME_records": [has_CNAME_records],
        "has_MX_records": [has_MX_records],
        "has_NS_records": [has_NS_records],
        "has_SOA_records": [has_SOA_records],
        "has_TXT_records": [has_TXT_records],
    }

    output_folder = util.get_analysis_folder_path(dirpath)
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(output_folder, util_def.EXCEL_DNS), index=False)



def analyse_individual_dns_data(ref_flag):
    ref = util.get_crawled_dataset_base_folder_name(ref_flag)
    base_folder = os.path.join(util_def.FOLDER_DATASET_BASE, ref)
    for dirpath, _, filenames in os.walk(base_folder):
        if util_def.FILE_DNS in filenames:
            file_path = os.path.join(dirpath, util_def.FILE_DNS)
            with open(file_path, "r") as f:
                data = json.load(f)
                extract_data_from_json(data, dirpath)


def consolidate_dns_data(ref):
    group_data = {}

    base_folder = os.path.join(util_def.FOLDER_ANALYSIS_BASE, ref)
    for dirpath, _, filenames in os.walk(base_folder):
        if util_def.EXCEL_DNS in filenames:
            group_prefix = dirpath.split(os.sep)[-1].split('-')[0] # Extract prefix like 0, 1, etc.
            file_path = os.path.join(dirpath, util_def.EXCEL_DNS)
            current_df = pd.read_excel(file_path)
        
            if group_prefix not in group_data:
                group_data[group_prefix] = current_df
            group_data[group_prefix] = pd.concat([group_data[group_prefix], current_df], ignore_index=True)
        
    output_folder = os.path.join(util_def.FOLDER_ANALYSIS_BASE, ref)
    for group, df in group_data.items():
        output_filename = f"{group}_{util_def.EXCEL_DNS_CONSOLIDATED}"
        df.drop_duplicates(subset=["Domain"], keep="first", inplace=True)
        df.to_excel(os.path.join(output_folder, output_filename), index=False)



def get_true_false_count_DNS(df):
    true_counts = []
    false_counts = []

    for column in df.columns:
        if column == "Domain":
            true_counts.append("True Count:")
            false_counts.append("False Count:")
            continue

        true_count = df[column].eq("True").sum()
        false_count = df[column].eq("False").sum()
        true_counts.append(true_count)
        false_counts.append(false_count)
    
    return true_counts, false_counts


def analyze_DNS_df(ref_flag):
    print("Analysing DNS Data...")
    ref = util.get_crawled_dataset_base_folder_name(ref_flag)
    base_folder = os.path.join(util_def.FOLDER_ANALYSIS_BASE, ref)

    consolidate_dns_data(ref)

    for file in os.listdir(base_folder):
        if file.endswith(util_def.EXCEL_DNS_CONSOLIDATED):
            df = pd.read_excel(os.path.join(base_folder, file), dtype=str)
            true_counts, false_counts = get_true_false_count_DNS(df)
            counts_df = pd.DataFrame([true_counts, false_counts], columns=df.columns)
            df = pd.concat([df, counts_df], ignore_index=True)
            df.to_excel(os.path.join(base_folder, file), index=False)
    
    print("Done analysing Certificate Data...")
    