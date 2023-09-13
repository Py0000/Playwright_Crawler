import os

import crawler_actions
import crawler_support
import util

def wait_for_page_to_load(page, act_flag):
    if act_flag:
        crawler_actions.move_mouse_smoothly_top_left_bottom_right(page)
    try:
        # Wait for the page to load completely (wait for the load event)
        page.wait_for_load_state('domcontentloaded')
    except:
        pass

    try:
        page.wait_for_load_state('networkidle')
    except:
        pass


def check_and_execute_user_actions(device_conf, act_flag, page):
    if not act_flag:
        pass
    else:
        crawler_actions.desktop_user_mouse_movement(page)


def check_and_execute_scroll(page, act_flag):
    if act_flag:
        crawler_actions.page_scroll(page)
    else:
        pass


def get_screenshot(page, folder_path, file_name):
    path = os.path.join(folder_path, file_name)
    crawler_support.save_screenshot(page, path)
    print("Screenshot Captured...")


# Get client-side scripts
client_side_scripts_injection_code = '''() => {
    const scripts = [];
    const scriptElements = document.querySelectorAll('script');
    scriptElements.forEach(script => {
        if (script.src) {
            scripts.push(script.src);
        } else {
            scripts.push(script.innerText);
        }
    });
    return scripts;
}'''

"""
def get_click_through_injection_code(url):
    click_through_injection_code = f'''() => {{
            let a = document.createElement('a');
            a.href = "{url}";
            a.textContent = "Url";
            a.id = "urlId";  
            document.body.appendChild(a);
        }}'''
    
    return click_through_injection_code
"""