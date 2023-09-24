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

    # Modify the data for easy consolidation
    combined_df = pd.concat([df1, df2, differences], axis=0)
    transposed_data = combined_df.transpose()

    # Save the differences to a new Excel file
    transposed_data.to_excel(f"{output_path}.xlsx", index=False)


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



desktop_user_path = "comparison\\excelsheet_data\\desktop\\user"
desktop_bot_path = "comparison\\excelsheet_data\\desktop\\bot"
mobile_user_path = "comparison\\excelsheet_data\\mobile\\user"
mobile_bot_path = "comparison\\excelsheet_data\\mobile\\bot"

ref_user_sub_path = "ref_user"
no_ref_no_user_sub_path = "no_ref_no_user"
ref_no_user_sub_path = "ref_no_user"
no_ref_user_sub_path = "no_ref_user"

main_path = [
    desktop_user_path, 
    desktop_bot_path, 
    mobile_user_path, 
    mobile_bot_path
]

sub_path = [
    ref_user_sub_path,
    no_ref_no_user_sub_path,
    ref_no_user_sub_path,
    no_ref_user_sub_path
]

## Change lines 95, 96, 97 and 101 
selected_main_path = main_path[3]
selected_sub_path = sub_path[1]
file_name_1 = "p1_features_after"
file_name_2 = "wise_features_before"

output_name_id = "_".join(selected_main_path.split("\\")[2:])
output_name_setting = selected_sub_path
additional_output_name = "_with_p2_dns"



file1_path = f"{selected_main_path}\\{selected_sub_path}\\{file_name_1}.xlsx"
file2_path = f"{selected_main_path}\\{selected_sub_path}\\{file_name_2}.xlsx"
output_path = f"comparison\\{output_name_id}_{output_name_setting}_{additional_output_name}"


"""
special_file1_path = f"comparison\\excelsheet_data\\mobile\\user\\ref_user\\{file_name_1}.xlsx"
special_file2_path = f"comparison\\excelsheet_data\\mobile\\user\\no_ref_no_user\\{file_name_1}.xlsx"
special_file3_path = f"comparison\\excelsheet_data\\mobile\\user\\ref_no_user\\{file_name_1}.xlsx"
special_file4_path = f"comparison\\excelsheet_data\\mobile\\user\\no_ref_user\\{file_name_1}.xlsx"
compare_excel_sheets(special_file1_path, special_file2_path, f"comparison\\test")
"""

"""
before_after_path11 = f"comparison\\excelsheet_data\\mobile\\user\\ref_user\\{file_name_1}.xlsx"
before_after_path12 = f"comparison\\excelsheet_data\\mobile\\user\\ref_user\\{file_name_2}.xlsx"
before_after_path21 = f"comparison\\excelsheet_data\\desktop\\user\\no_ref_no_user\\{file_name_1}.xlsx"
before_after_path22 = f"comparison\\excelsheet_data\\desktop\\user\\no_ref_no_user\\{file_name_2}.xlsx"
before_after_path31 = f"comparison\\excelsheet_data\\desktop\\user\\ref_no_user\\{file_name_1}.xlsx"
before_after_path32 = f"comparison\\excelsheet_data\\desktop\\user\\ref_no_user\\{file_name_2}.xlsx"
before_after_path41 = f"comparison\\excelsheet_data\\desktop\\user\\no_ref_user\\{file_name_1}.xlsx"
before_after_path42 = f"comparison\\excelsheet_data\\desktop\\user\\no_ref_user\\{file_name_2}.xlsx"
compare_excel_sheets(before_after_path11, before_after_path12, f"comparison\\before_after")
"""

ua1 = f"comparison\\excelsheet_data\\desktop\\user\\no_ref_no_user\\{file_name_1}.xlsx"
ua2 = f"comparison\\excelsheet_data\\desktop\\bot\\no_ref_no_user\\{file_name_1}.xlsx"
ua3 = f"comparison\\excelsheet_data\\mobile\\user\\no_ref_no_user\\{file_name_1}.xlsx"
ua4 = f"comparison\\excelsheet_data\\mobile\\bot\\no_ref_no_user\\{file_name_1}.xlsx"
compare_excel_sheets(ua1, ua3, f"comparison\\ua")

#compare_excel_sheets(file1_path, file2_path, output_path)
#compare_and_save_json(file1_path, file2_path, output_path)


