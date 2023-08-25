from bs4 import BeautifulSoup
import json
import os


def generateDOMTree(html_file):
    with open(html_file, "r", encoding="utf-8") as file1:
        html = html_file.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup
    



def compare_nodes(node1, node2, differences, file1, file2, traversal_level):
    print("Called @ Level", traversal_level)
    
    # Guard Clause, Might not be needed
    if node1 is None:
        if node2 is not None:
            data = {"Number of Levels": "Different"}
            differences.append(data)
        else: 
            data = {"Number of Levels": "Same"}
    
    if node2 is None:
        if node1 is not None:
            data = {"Number of Levels": "Different"}
            differences.append(data)
        else: 
            data = {"Number of Levels": "Same"}

    # Skip Doctype nodes
    if node1.name is None or node2.name is None:
        return

    # Compare node type and tag name
    if node1.name != node2.name:
        data = {
            "Tag mismatch": {
                "Tree Level": traversal_level,
                file1.name: node1.name,
                file2.name: node2.name
            }
        }
        differences.append(data)

    # Compare attributes
    if node1.attrs != node2.attrs:
        data = {
            f"Attributes mismatch for tag": {
                "Tree Level": traversal_level,
                "Different Node?": f"{node1.name != node2.name} ({node1.name}, {node2.name})",
                file1.name: node1.attrs,
                file2.name: node2.attrs
            }
        }
        differences.append(data)

    # Compare text content
    if node1.string != node2.string:
        data = {
            f"Text content mismatch for tag({node1.name})": {
                "Tree Level": traversal_level,
                "Different Node?": f"{node1.name != node2.name} ({node1.name}, {node2.name})",
                file1.name: node1.string,
                file2.name: node2.string
            }
        }
        differences.append(data)


    # Recursively compare child nodes
    for child1, child2 in zip(node1.children, node2.children):
        compare_nodes(child1, child2, differences, file1, file2, traversal_level=traversal_level+1)



desktop_user_path = "comparison\\html_script_data\\desktop\\user"
desktop_bot_path = "comparison\\html_script_data\\desktop\\bot"
mobile_user_path = "comparison\\html_script_data\\mobile\\user"
mobile_bot_path = "comparison\\html_script_data\\mobile\\bot"

ref_user_sub_path = "ref_user"
no_ref_no_user_sub_path = "no_ref_no_user"
ref_no_user_sub_path = "ref_no_user"
no_ref_user_sub_path = "no_ref_user"

main_path = [
    desktop_user_path, 
    desktop_bot_path, 
    mobile_user_path, 
    mobile_bot_path
]

sub_path = [
    ref_user_sub_path,
    no_ref_no_user_sub_path,
    ref_no_user_sub_path,
    no_ref_user_sub_path
]

## Change these lines 
selected_main_path = main_path[0]
selected_sub_path = sub_path[0]
file_name1 = ""
file_name2 = ""

output_name_id = "_".join(selected_main_path.split("\\")[2:])
output_name_setting = selected_sub_path
additional_output_name = ""



file1_path = f"{selected_main_path}\\{selected_sub_path}\\{file_name1}.xlsx"
file2_path = f"{selected_main_path}\\{selected_sub_path}\\{file_name2}.xlsx"
output_path = f"comparison\\{output_name_id}_{output_name_setting}_{additional_output_name}"


differences = []
soup1 = generateDOMTree(file1_path)
soup2 = generateDOMTree(file2_path)
compare_nodes(soup1, soup2, differences, file_name1, file_name2, traversal_level=0)


if not differences:
    print("DOM trees are equal.")
else:
    print("DOM trees are different. Saving differences to JSON file...")

with open(output_path, "w") as json_file:
    json.dump(differences, json_file, indent=4)
