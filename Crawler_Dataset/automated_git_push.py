import os
import subprocess
import time
import argparse
import threading

import data_reallocator

def git_commit_and_push(commit_message="Automated commit"):
    try:
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        print("Successfully executed git pull command")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during git pull operation: {e}")
    
    try:
        subprocess.run(['git', 'add', '--all'], check=True)  # Stage all changes
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)  # Commit with a message
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)  # Push to the master branch of remote repository
        print("Successfully executed git push command")

    except subprocess.CalledProcessError as e:
        print(f"Error during git push operation: {e}")


def git_push_periodically():
    while True:
        time.sleep(3600)
        git_commit_and_push()


def shift_data_folder_periodically(folder_name, phishing_or_benign_tag):
    while True:
        time.sleep(360)
        data_reallocator.shift_data_from_Playwright_Crawler_folder(folder_name, phishing_or_benign_tag)
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Git automation script.")
    parser.add_argument("folder_name", help="Name of the folder that contains the dataset")
    parser.add_argument("phishing_or_benign_tag", help="Name of the folder to store the dataset")
    args = parser.parse_args()

    # Periodically commit and push
    data_folder_shifter_thread = threading.Thread(target=shift_data_folder_periodically, args=(args.folder_name, args.phishing_or_benign_tag))
    push_thread = threading.Thread(target=git_push_periodically)

    data_folder_shifter_thread.start()
    push_thread.start()

    data_folder_shifter_thread.join()
    push_thread.join()
