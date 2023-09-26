# Playwright_Crawler


## How to run it on remote VM?


### Method 1: `tmux`
1. `ssh` into the remote VM designated for this research purpose.
2. `sudo -s` to elevate to root privileges if required to change the remote VM configurations. 
3. `cd Desktop/Playwright_Crawler` to get to the path where the script is hosted.
4. Ensure all the required libraries are installed. (See `dependency.txt`)
5. Start a session using `tmux`.
6. Start the script running in the tmux session using: `python3 src/main.py feeds/urls/[filename].txt [saved-data-folder-tag] > [log-filename].txt`
7. `Ctrl B` + `D` to detach from the tmux session.
8. Exit the ssh session if you wish to. The script will still run after exiting.

Returning to the ssh session:
1. `tmux attach` to get back the existing tmux session where the script is running.


### Method 2: `nohup`
1. `ssh` into the remote VM designated for this research purpose.
2. `sudo -s` to elevate to root privileges if required to change the remote VM configurations. 
3. `cd Desktop/Playwright_Crawler` to get to the path where the script is hosted.
4. Ensure all the required libraries are installed. (See `dependency.txt`)
5. `nohup python3 src/main.py feeds/urls/[filename].txt [folder_name_to_save] > [log_filename].txt 2>&1 &`
  * Will return the background process id running the script 
6. Exit the ssh session if you wish to. The script will still run after exiting.

Returning to the ssh session:
1. ps -p `[process_id]` to check on its progress


### Final Phase 
* The crawled data will be stored in the folder `dataset_[folder_name_to_save]`. 
* The analyzed data using the crawled data will be stored in the folder `d_analysis_[folder_name_to_save]`
* The logs generated while crawling will be stored in the file `[log_filename].txt`.
