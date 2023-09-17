import os 
import json
from bs4 import BeautifulSoup, Tag

html_file_name = "html_script_aft.html"
user_agents = ["mac", "win"]
referrers = ["g_ref", "self_ref", "fb_ref", "no_ref"]
actions = ["click", "move", "scroll", "no_act"]

def get_folder_name(user_agent, referrer, action, index, main_folder_path):
    return os.path.join(main_folder_path, f"{user_agent}_{referrer}_{action}", index)


def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_html_script(folder_name):
    with open(os.path.join(folder_name, html_file_name), 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        return soup


def traverse(html_1_node, html_2_node, differences, level=0):
    # If node type is different
    if type(html_1_node) != type(html_2_node):
        diff_key = f"Level {level} - Node Type Mismatch"
        differences.update({diff_key: {"server": str(html_1_node), "client": str(html_2_node)}})
        return

    # If node is a Tag, check its name and attributes
    if isinstance(html_1_node, Tag) and isinstance(html_2_node, Tag):
        if html_1_node.name != html_2_node.name:
            diff_key = f"Level {level} - Tag Name Mismatch"
            differences.update({diff_key: {"server": html_1_node.name, "client": html_2_node.name}})
        
        elif html_1_node.attrs != html_2_node.attrs:
            diff_key = f"Level {level} - Attribute Mismatch"
            differences.update({diff_key: {"server": html_1_node.attrs, "client": html_2_node.attrs}})
        
        elif html_1_node.string != html_2_node.string:
            diff_key = f"Level {level} - Textual Content Mismatch"
            differences.update({diff_key: {"server": html_1_node.string, "client": html_2_node.string}})
        
        # Continue traversal for children of the Tag
        for s_child, c_child in zip(html_1_node.children, html_2_node.children):
            traverse(s_child, c_child, differences, level+1)



def compare_mac_against_window_same_config(index, main_folder_path, output_folder):
    result = {}
    for ref in referrers:
        for act in actions:
            mac_folder = get_folder_name("mac", ref, act, index, main_folder_path)
            win_folder = get_folder_name("win", ref, act, index, main_folder_path)

            mac_html = load_html_script(mac_folder)
            win_html = load_html_script(win_folder)

            diff = {}
            traverse(mac_html, win_html, diff)
            is_same = len(diff) == 0
            result.update({f"mac-vs-win: {ref} + {act}": is_same})
            if (len(diff) == 0):
                sorted_diff = {"Message": "No difference between html DOM of the 2 files"}
            else:
                sorted_diff = dict(sorted(diff.items(), key=lambda item: int(item[0].split()[1])))
            save_to_json(os.path.join(output_folder, f"mac_vs_win_{ref}_{act}.json"), sorted_diff)

    return result


def compare_within_same_ua_same_ref_diff_act(index, main_folder_path, output_folder):
    result = {}
    for user_agent in user_agents:
        for referrer in referrers:
            for i, current_action in enumerate(actions[:-1]):
                current_folder = get_folder_name(user_agent, referrer, current_action, index, main_folder_path)

                # loop through subsequent user-actions
                for sub_action in actions[i+1:]:
                    sub_folder = get_folder_name(user_agent, referrer, sub_action, index, main_folder_path)

                    current_html = load_html_script(current_folder)
                    sub_html = load_html_script(sub_folder)

                    diff = {}
                    traverse(current_html, sub_html, diff)
                    is_same = len(diff) == 0
                    result.update({f"{user_agent}_{referrer}: {current_action} vs {sub_action}": is_same})

                    if (len(diff) == 0):
                        sorted_diff = {"Message": "No difference between html DOM of the 2 files"}
                    else:
                        sorted_diff = dict(sorted(diff.items(), key=lambda item: int(item[0].split()[1])))
                    save_to_json(os.path.join(output_folder, f"{user_agent}_{referrer}_{current_action}_vs_{sub_action}.json"), sorted_diff)
    
    return result


def compare_within_same_ua_same_act_diff_ref(index, main_folder_path, output_folder):
    result = {}
    for user_agent in user_agents:
        for action in actions:
            for i, current_referrer in enumerate(referrers[:-1]):
                current_folder = get_folder_name(user_agent, current_referrer, action, index, main_folder_path)

                for sub_referrer in referrers[i+1:]:
                    sub_folder = get_folder_name(user_agent, sub_referrer, action, index, main_folder_path)

                    current_html = load_html_script(current_folder)
                    sub_html = load_html_script(sub_folder)

                    diff = {}
                    traverse(current_html, sub_html, diff)
                    is_same = len(diff) == 0
                    result.update({f"{user_agent}_{action}: {current_referrer} vs {sub_referrer}": is_same})

                    if (len(diff) == 0):
                        sorted_diff = {"Message": "No difference between html DOM of the 2 files"}
                    else:
                        sorted_diff = dict(sorted(diff.items(), key=lambda item: int(item[0].split()[1])))
                    save_to_json(os.path.join(output_folder, f"{user_agent}_{action}_{current_referrer}_vs_{sub_referrer}.json"), sorted_diff)
    
    return result


def compare_dom(index, main_folder_path, output_folder):
    mac_against_win_result = compare_mac_against_window_same_config(index, main_folder_path, output_folder)
    same_ua_same_ref_diff_act_result = compare_within_same_ua_same_ref_diff_act(index, main_folder_path, output_folder)
    same_us_same_act_diff_ref_result = compare_within_same_ua_same_act_diff_ref(index, main_folder_path, output_folder)

    result = {
        "Mac vs Window (Same configurations)": mac_against_win_result,
        "Same User-Agent Same Referrer Different User Actions": same_ua_same_ref_diff_act_result,
        "Same User-Agent Same User Actions Different Referrer": same_us_same_act_diff_ref_result,
    }

    save_to_json(os.path.join(output_folder, f"{index}_summarized.json"), result)



def main_comparator(main_folder_path):
    config_folders = os.listdir(main_folder_path)
    indices = []
    for config_folder in config_folders:
        config_folder_path = os.path.join(main_folder_path, config_folder)
        url_index_folders = os.listdir(config_folder_path)
        url_index_folders.sort(key=int)
        for index in url_index_folders:
            indices.append(index)
        break      
    
    for index in indices:
        print(f"Comparing: {main_folder_path} {index}")
        data_index = main_folder_path.split("_")
        folder_main = "dom_diff_" + '_'.join(data_index[1:]) 
        output_folder = os.path.join(folder_main, f"{index}_dom_data")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        compare_dom(index, main_folder_path, output_folder)
    




main_comparator("dataset_170923_6")

