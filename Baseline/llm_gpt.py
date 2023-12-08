import argparse
import openai
import base64
import requests

def get_api_key(key_file):
    with open(key_file, 'r') as file:
        api_key = file.readline().strip()
    
    return api_key


def get_phishing_page_urls(url_file):
    with open(url_file, 'r') as file:
        visited = file.readline().strip()
        provided = file.readline().strip()
        
    return visited, provided


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def gpt_analysis(image_path, url_path):
    api_key = get_api_key("api_key.txt")
    encoded_image =  encode_image_to_base64(image_path)
    page_visited_url, page_provided_url = get_phishing_page_urls(url_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Determine if this website is a phishing website given the webpage screenshot and webpage URLs. Give your output in this format: 1. Targeted Brand, 2. User Credential fields (if any), 3. Phishing Indicators (if phishing), 4. Assessments (i.e. reason why it is phishing or why it isn't), 5. Conclusion"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                },
                {
                    "type": "text",
                    "text": page_visited_url
                },
                {
                    "type": "text",
                    "text": page_provided_url
                },
            ]
            }
        ],
        "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("image_path", help="Name of the image file")
    parser.add_argument("url_path", help="Name of the url file")
    args = parser.parse_args()

    """
    Got some error: {'error': {'message': 'The model `gpt-4-vision-preview` does not exist or you do not have access to it. Learn more: https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4.', 'type': 'invalid_request_error', 'param': None, 'code': 'model_not_found'}}
    """
    gpt_analysis(args.image_path, args.url_path)