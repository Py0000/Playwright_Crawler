from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os
import time
import threading
import argparse

import data_reallocator

def upload_single_file_to_gdrive_with_exponential_backoff(file, file_path, drive_service, drive_folder_id, max_retries=5):
    print("Adding one file to google drive...")
    retry = 0
    while retry < max_retries:
        try:
            # Create a request to upload the file
            media = MediaFileUpload(file_path, mimetype='application/zip')
            request = drive_service.files().create(
                media_body=media,
                body={
                    'name': file,
                    'parents': [drive_folder_id]
                }
            )

            # Execute the request
            file = request.execute()
            print(f"Uploaded {file}\n")

            # Remove the file after successful upload
            os.remove(file_path)
        except:
            wait_time = (2 ** retry)
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retry += 1


def upload_to_google_drive(data_folder):
    print("[Periodic] Saving to google drive...")
    credentials = Credentials.from_service_account_file(os.path.join(os.getcwd(), "src", 'drive-config.json'))
    drive_service = build('drive', 'v3', credentials=credentials)
    drive_folder_id = "1xzYT2hNdEiBqLHdp9Y-D9REDph0LE40V"

    
    if data_folder.endswith('.zip'):
        file_name = os.path.basename(data_folder)
        upload_single_file_to_gdrive_with_exponential_backoff(file_name, data_folder, drive_service, drive_folder_id)
           

"""
def save_to_gdrive_periodically():
    time.sleep(90)
    while True:
        try:
           upload_to_google_drive()
        except Exception as e:
            print("Error uploading to google drive: ", e)
        finally:
            time.sleep(3600)
"""

def shift_data_folder_periodically(folder_name, phishing_or_benign_tag):
    print("Shifting data...")
    while True:
        time.sleep(60)
        data_folder = data_reallocator.shift_data_from_Playwright_Crawler_folder(folder_name, phishing_or_benign_tag)
        upload_to_google_drive(data_folder)
        
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Google Drive automation.")
    parser.add_argument("folder_name", help="Name of the folder that contains the dataset")
    parser.add_argument("phishing_or_benign_tag", help="Name of the folder to store the dataset")
    args = parser.parse_args()

    """
    # Periodically commit and push
    data_folder_shifter_thread = threading.Thread(target=shift_data_folder_periodically, args=(args.folder_name, args.phishing_or_benign_tag))
    push_thread = threading.Thread(target=save_to_gdrive_periodically)

    data_folder_shifter_thread.start()
    push_thread.start()
    """
    

    shift_data_folder_periodically(args.folder_name, args.phishing_or_benign_tag)
