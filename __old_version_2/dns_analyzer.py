import os
import pandas as pd

import definitions
import util


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



def analyze_DNS_df(base_folder_name):
    print("Analysing DNS Data...")

    directory = os.path.join(os.getcwd(), base_folder_name, definitions.OUTPUT_PATH_DNS)

    for file in sorted(os.listdir(directory)):
        # Only process excel files
        if file.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(directory, file), dtype=str)
            true_counts, false_counts = get_true_false_count_DNS(df)
            counts_df = pd.DataFrame([true_counts, false_counts], columns=df.columns)
            df = pd.concat([df, counts_df], ignore_index=True)
            df.to_excel(os.path.join(directory, file), index=False)
    
    print("Done analysing DNS Data...")