import json

def get_html_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
