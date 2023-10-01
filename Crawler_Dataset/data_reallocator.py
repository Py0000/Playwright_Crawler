import shutil
import os
import threading
import time

import network_data_processor

def zip_folder(dest_folder, folder):
    try:
        output_filename = os.path.join(dest_folder, folder)
        shutil.make_archive(output_filename, "zip", dest_folder, folder) # Zip the folder
        shutil.rmtree(os.path.join(dest_folder, folder)) # Remove the orginal folder
        print(f"Successfully zipped {folder}")
    except Exception as e:
        print(f"Error occurred when zipping {folder}: {e}")




def move_folder(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
    if not os.path.exists(src_folder):
        print("Src Folder not exist")
        pass

    for folder in os.listdir(src_folder):
        src = os.path.join(src_folder, folder)
        if os.path.exists(src):
            semaphore_lock_file = os.path.join(src, ".completed")
            if os.path.exists(semaphore_lock_file):
                try:
                    os.remove(semaphore_lock_file)
                    shutil.move(src, dest_folder)
                    network_data_processor.process_network_data(dest_folder)
                    print(f"Done moving folder: {folder}")

                except Exception as e:
                    print(f"Error occured for {src}: ", e)
                
                finally:
                    zip_folder(dest_folder, folder)
                        
                        
                    
                    
def shift_data_from_Playwright_Crawler_folder(src_dataset_folder_name, phishing_or_benign_tag):
    src_folder = os.path.join("..", "Playwright_Crawler", f"dataset_{src_dataset_folder_name}")
    dest_folder = os.path.join(phishing_or_benign_tag, "dataset")

    src_self_ref_folder = os.path.join(src_folder, "self_ref")
    src_no_ref_folder = os.path.join(src_folder, "no_ref")
    dest_self_ref_folder = os.path.join(dest_folder, "self_ref")
    dest_no_ref_folder = os.path.join(dest_folder, "no_ref")

    self_ref_thread = threading.Thread(target=move_folder, args=(src_self_ref_folder, dest_self_ref_folder))
    no_ref_thread = threading.Thread(target=move_folder, args=(src_no_ref_folder, dest_no_ref_folder))

    # Start the threads
    self_ref_thread.start()
    no_ref_thread.start()

    # Wait for both threads to complete
    self_ref_thread.join()
    no_ref_thread.join()

