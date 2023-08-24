import pandas as pd
import json
import os

def extract_file_name(file_path):
    # Get the filename without path and extension
    filename_without_path_extension = os.path.splitext(os.path.basename(file_path))[0]

    return filename_without_path_extension

def compare_excel_sheets(file1_path, file2_path, output_path):
    # Read Excel sheets into DataFrames
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # Compare the two DataFrames and create a new DataFrame for differences
    differences = (df1 != df2).applymap(lambda x: "Different" if x else "")

    # Save the differences to a new Excel file
    differences.to_excel(f"{output_path}.xlsx", index=False)


def compare_and_save_json(file1_path, file2_path, output_json_path):
    # Read Excel sheets into DataFrames
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    df1_name = extract_file_name(file1_path)
    df2_name = extract_file_name(file2_path)

    # Compare the two DataFrames and find differences
    differences = df1.compare(df2)

    # Convert integer and boolean values to strings
    differences = differences.applymap(lambda x: str(x) if isinstance(x, (int, bool)) else x)

    # Create a dictionary to store combined column differences
    combined_column_differences = {}

    is_column_seen = False
    # Iterate through columns and store their combined differences
    for column in differences.columns:
        column_diff = differences[column]
        different_cells = column_diff[column_diff.notna()]
        column_name = column[0]  # Extract the column name

        if column_name not in combined_column_differences:
            combined_column_differences[column_name] = {}

        #sub_column = column[1]  # Extract the sub-column name
        
        if is_column_seen:
            sub_column = df2_name
            is_column_seen = False
        else:
            sub_column = df1_name
            is_column_seen = True

        if not different_cells.empty:
            combined_column_differences[column_name][sub_column] = different_cells.iloc[0]
        else:
            combined_column_differences[column_name][sub_column] = None

    # Save the combined column differences to a JSON file with formatting
    with open(f"{output_json_path}.json", 'w') as json_file:
        json.dump(combined_column_differences, json_file, indent=4)
    

file1_path = 'comparison\\phishing_desktop_bot_no_ref_user.xlsx'
file2_path = 'comparison\\phishing_desktop_bot_no_ref_user_before.xlsx'

output_path = "comparison\\phishing_desktop_bot_no_ref_user_before_features"
#compare_excel_sheets(file1_path, file2_path, output_path)
compare_and_save_json(file1_path, file2_path, output_path)