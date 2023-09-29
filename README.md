# Playwright_Crawler

## Brief Description
A web crawler designed using Playwright in Python. It is to be used for a FYP project for a comprehensive study of the chracteristics of current phishing ecosystem. 
<br>

The crawler runs on 2 main configuration: 
* Having no referrer 
* Having referrer set to its own web-domain url.
<br>

In additon to the 2 main configurations, these are the other configurations:
* User-agent: `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"`
* User mouse movement mimicked. 
<br>

What data this crawler obtain?
* HTML script (Server-Side & Client-Side)
* Webpage Screenshot (Server-Side & Client-Side)
* TLS/SSL Certificate information of the web domain
* DNS Records information of the web domain 
* All embedded url links in the HTML script
* Network details (including detailed network information)
* Network responses data (Downloaded them from the server) 
* Client-Side scripts/requests found in the HTML script

<br>

## How to run the Crawler Script on remote VM?


### Method 1: `tmux`
1. `ssh` into the remote VM designated for this research purpose.
2. `sudo -s` to elevate to root privileges if required to change the remote VM configurations. 
3. `cd Desktop/Playwright_Crawler` to get to the path where the script is hosted.
4. Ensure all the required libraries are installed. (See `dependency.txt`)
5. Start a session using `tmux`.
6. Start the script running in the tmux session using: `python3 src/main.py [saved-data-folder-tag] > [log-filename].txt`
7. `Ctrl B` + `D` to detach from the tmux session.
8. Exit the ssh session if you wish to. The script will still run after exiting.

Returning to the ssh session:
1. `tmux attach` to get back the existing tmux session where the script is running.


### Method 2: `nohup`
1. `ssh` into the remote VM designated for this research purpose.
2. `sudo -s` to elevate to root privileges if required to change the remote VM configurations. 
3. `cd Desktop/Playwright_Crawler` to get to the path where the script is hosted.
4. Ensure all the required libraries are installed. (See `dependency.txt`)
5. `nohup python3 src/main.py [folder_name_to_save] > [log_filename].txt 2>&1 &`
  * Will return the background process id running the script 
6. Exit the ssh session if you wish to. The script will still run after exiting.

Returning to the ssh session:
1. ps -p `[process_id]` to check on its progress


### Final Phase 
* The crawled data will be stored in the folder `dataset_[folder_name_to_save]`. 
* The analyzed data using the crawled data will be stored in the folder `d_analysis_[folder_name_to_save]`
* The logs generated while crawling will be stored in the file `[log_filename].txt`.


## How to run the dataset transfer script (i.e. transfer to a private github repo)
### Method 1: `tmux`
1. `ssh` into the remote VM designated for this research purpose.
2. `cd Desktop/Crawler_Dataset` to get to the path where the script is hosted.
3. Ensure all the required libraries are installed. (See `dependency.txt`)
4. Start a session using `tmux`.
5. Start the script running in the tmux session using: `python3 src/automated_git_push.py [folder_name_to_save (input when running crawler)] [Phishing/Benign]> [log-filename].txt`
6. `Ctrl B` + `D` to detach from the tmux session.
7. Exit the ssh session if you wish to. The script will still run after exiting.

Returning to the ssh session:
1. `tmux attach` to get back the existing tmux session where the script is running.