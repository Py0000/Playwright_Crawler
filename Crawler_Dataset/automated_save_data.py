from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

import time
import argparse
import threading

import data_reallocator

def upload_single_file_to_gdrive_with_exponential_backoff(file_path, drive_service, drive_folder_id, max_retries=3):
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
            print(f"Uploaded {file} ({file['id']})")
        except:
            wait_time = (2 ** retry)
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retry += 1


def upload_to_google_drive(ref):
    credentials = Credentials.from_service_account_file('fyp-phishing-analysis-6d64a520d117.json')
    drive_service = build('drive', 'v3', credentials=credentials)
    drive_phishing_self_ref_folder_id = "167ySPLxM49KpIlSoHXCmw8tz75yqVt0z"
    drive_phishing_no_ref_folder_id  = "1SIzLOgcPaIiyU9bEaMRmceyvESJu14un"

    drive_folder_id = drive_phishing_self_ref_folder_id if ref else drive_phishing_no_ref_folder_id
    ref_folder = "self_ref" if ref else "no_ref"
    folder_path = os.path.join("Phishing", "dataset", ref_folder)

    for file in os.listdir(folder_path):
        if file.endswith('.zip'):
            file_path = os.path.join(folder_path, file)
            upload_single_file_to_gdrive_with_exponential_backoff(file_path, drive_service, drive_folder_id)
            


def save_to_gdrive_periodically():
    while True:
        #time.sleep(7200)
        try:
            upload_to_google_drive(ref=True)
            upload_to_google_drive(ref=False)
        except Exception as e:
            print("Error uploading to google drive: ", e)


def shift_data_folder_periodically(folder_name, phishing_or_benign_tag):
    while True:
        #time.sleep(360)
        data_reallocator.shift_data_from_Playwright_Crawler_folder(folder_name, phishing_or_benign_tag)
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Git automation script.")
    parser.add_argument("folder_name", help="Name of the folder that contains the dataset")
    parser.add_argument("phishing_or_benign_tag", help="Name of the folder to store the dataset")
    args = parser.parse_args()

    # Periodically commit and push
    data_folder_shifter_thread = threading.Thread(target=shift_data_folder_periodically, args=(args.folder_name, args.phishing_or_benign_tag))
    push_thread = threading.Thread(target=save_to_gdrive_periodically)

    data_folder_shifter_thread.start()
    push_thread.start()

    data_folder_shifter_thread.join()
    push_thread.join()
