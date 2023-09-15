import os

import os

def rename_files_in_folder(folder_path, start_number):
    renamed_prefixes = set()  # to keep track of already renamed prefixes
    existing_files = set(os.listdir(folder_path))

    for filename in sorted(os.listdir(folder_path)):  # sorting to ensure a consistent order
        if filename.endswith('.xlsx') or filename.endswith('.json'):
            # Split the filename into its number prefix and the rest of the name
            prefix, *rest = filename.split('_')
            if prefix.isdigit():
                # If this prefix has not been renamed yet, assign the next start_number
                if prefix not in renamed_prefixes:
                    renamed_prefixes.add(prefix)
                    current_rename_number = start_number
                    start_number += 1
                else:
                    current_rename_number = start_number - 1  # Use the last used start_number

                # Form the new filename with the updated number
                new_filename = str(current_rename_number) + '_' + '_'.join(rest)
                

                os.rename(
                    os.path.join(folder_path, filename),
                    os.path.join(folder_path, new_filename)
                )


# Set the directory path
dir_path = 'dataset'

for sub_folder in os.listdir(dir_path):
    print(sub_folder)
    
    # Check if the item is actually a directory
    if os.path.isdir(os.path.join(dir_path, sub_folder)):
        folder_names = [name for name in os.listdir(os.path.join(dir_path, sub_folder)) if os.path.isdir(os.path.join(dir_path, sub_folder, name))]
        folder_names.sort(key=int)  # this ensures that '10' comes after '9'

        start_number = 30

        # Rename the folders
        for name in folder_names:
            new_name = str(start_number)
            os.rename(os.path.join(dir_path, sub_folder, name), os.path.join(dir_path, sub_folder, new_name))
            
            # Rename files in the renamed folder
            rename_files_in_folder(os.path.join(dir_path, sub_folder), start_number)

            start_number += 1
