from bs4 import BeautifulSoup, Tag
import utility as util

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
        for s_child, c_child in zip(server_node.children, client_node.children):
            traverse(s_child, c_child, differences, level+1)


def compare_dom(server_file_name, client_file_name):
    server_html = util.get_html_content(server_file_name)
    client_html = util.get_html_content(client_file_name)

    server_soup = BeautifulSoup(server_html, 'lxml')
    client_soup = BeautifulSoup(client_html, 'lxml')

    differences = {}
    traverse(server_soup, client_soup, differences)
    sorted_differences = dict(sorted(differences.items(), key=lambda item: int(item[0].split()[1])))
    
    return sorted_differences


compare_dom("html_script_before.html", "html_script_aft.html")
