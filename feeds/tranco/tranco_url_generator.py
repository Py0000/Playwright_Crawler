from tranco import Tranco
import requests
import pandas as pd

def get_full_url(domain):
    try:
        https_url = f"https://www.{domain}"
        response = requests.head(https_url, timeout=1, allow_redirects=True)
        response.raise_for_status()
        return https_url
    except requests.RequestException:
        try:
            http_url = f"http://www.{domain}"
            response = requests.head(http_url, timeout=1, allow_redirects=True)
            response.raise_for_status()
            return http_url
        except requests.RequestException:
            return "Error"

t = Tranco(cache=True, cache_dir='.tranco')


#latest_list = t.list()
tranco_list_path = "feeds/tranco/.tranco/K27VW-DEFAULT.csv"
df = pd.read_csv(tranco_list_path, header=None)
top_10K = df.iloc[:10000, 1].tolist()


for domain in top_10K:
    full_url = get_full_url(domain)
    with open('feeds/tranco/top_10K_with_error_list.txt', 'a') as file:
        file.write(full_url + '\n')

    with open('feeds/tranco/top_10K.txt', 'a') as file:
        if full_url == "Error":
            full_url = f"https://www.{domain}"
        file.write(full_url + '\n')
    
