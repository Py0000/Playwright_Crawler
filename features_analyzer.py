import json
import os
import pandas as pd

import utility as util


def analyze_column(df, column, consolidated_counts):
    counts = df[column].value_counts()
    # Convert the Pandas Series to a dictionary before saving
    counts_dict = counts.to_dict()
    consolidated_counts[column] = counts_dict



def analyze_features_df(base_folder_name):
    print("Analysing Features Data...")

    folder_name = f"{base_folder_name}/{util.OUTPUT_PATH_EXCEL_FEATURES}"
    directory = os.path.join(os.getcwd(), folder_name)

    for file in sorted(os.listdir(directory)):
        file_name = util.get_file_name_without_ext(file)

        consolidated_counts = {}
        consolidated_counts["File Name"] = file_name

        df = pd.read_excel(os.path.join(directory, file))

        for column in df.columns:
            isTitle = column == "Webpage Title"
            if isTitle:
                continue

            analyze_column(df, column, consolidated_counts)
    
    output_file = f"{base_folder_name}/{util.OUTPUT_PATH_ANALYSIS_FEATURES}{file_name}_analysis.json"
    with open(output_file, 'w') as json_file:
            json.dump(consolidated_counts, json_file, indent=4)

    print("Done analysing Features Data...")    