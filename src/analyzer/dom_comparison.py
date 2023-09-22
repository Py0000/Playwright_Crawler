import os 
import json
from bs4 import BeautifulSoup, Tag

client_html_file_name = "html_script_aft.html"
server_html_file_name = "html_script_bef.html"
referrers = ["self_ref", "no_ref"]


def get_folder_name(referrer, url_hash, main_folder_path):
    return os.path.join(main_folder_path, f"{referrer}", url_hash)


def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_html_script(folder_name, html_file_name):
    with open(os.path.join(folder_name, html_file_name), 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        return soup


def traverse(server_node, client_node, differences, level=0):
    # If node type is different
    if type(server_node) != type(client_node):
        diff_key = f"Level {level} - Node Type Mismatch"
        differences.update({diff_key: {"server": str(server_node), "client": str(client_node)}})
        return

    # If node is a Tag, check its name and attributes
    if isinstance(server_node, Tag) and isinstance(client_node, Tag):
        if server_node.name != client_node.name:
            diff_key = f"Level {level} - Tag Name Mismatch"
            differences.update({diff_key: {"server": server_node.name, "client": client_node.name}})

        elif server_node.attrs != client_node.attrs:
            diff_key = f"Level {level} - Attribute Mismatch"
            differences.update({diff_key: {"server": server_node.attrs, "client": client_node.attrs}})
        
        elif server_node.string != client_node.string:
            diff_key = f"Level {level} - Textual Content Mismatch"
            differences.update({diff_key: {"server": server_node.string, "client": client_node.string}})

        # Continue traversal for children of the Tag
        server_node_children = list(server_node.children)
        client_node_children = list(client_node.children)
        size_of_server_node_children = len(server_node_children)
        size_of_client_node_children = len(client_node_children)

        if size_of_server_node_children != size_of_client_node_children:
            diff_key = f"Level {level} - Children Count Mismatch"
            differences.update({diff_key: {"server": size_of_server_node_children, "client": size_of_client_node_children}})

        max_length = max(size_of_server_node_children, size_of_client_node_children)
        for i in range(max_length):
            if i < size_of_server_node_children and i < size_of_client_node_children:
                traverse(server_node_children[i], client_node_children[i], differences, level+1)
            elif i >= size_of_server_node_children:
                diff_key = f"Level {level+1} - Extra Child in Client"
                differences.update({diff_key: {"client": str(client_node_children[i])}})
            else:
                diff_key = f"Level {level+1} - Extra Child in Server"
                differences.update({diff_key: {"server": str(server_node_children[i])}})


