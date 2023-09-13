import os

import crawler_actions
import crawler_support
import util
import util_def

def wait_for_page_to_load(page, act_flag):
    if act_flag == util_def.MOUSE_MOVEMENT:
        crawler_actions.move_mouse_smoothly_top_left_bottom_right(page)
    try:
        # Wait for the page to load completely (wait for the load event)
        page.wait_for_load_state('domcontentloaded')
    except:
        pass

    try:
        page.wait_for_load_state('networkidle')
    except:
        page.wait_for_timeout(3000)


def check_and_execute_user_actions(act_flag, page):
    if act_flag == util_def.NO_USER_ACT_SET:
        pass
    elif act_flag == util_def.MOUSE_CLICK_LEFT:
        crawler_actions.mouse_click(page, "left")
    elif act_flag == util_def.MOUSE_CLICK_RIGHT:
        crawler_actions.mouse_click(page, "right")
    elif act_flag == util_def.MOUSE_MOVEMENT:
        crawler_actions.move_mouse_smoothly_top_left_bottom_right(page)
    elif act_flag == util_def.PAGE_SCROLL:
        crawler_actions.page_scroll(page)
    else:
        pass

"""
def check_and_execute_scroll(page, act_flag):
    if act_flag:
        crawler_actions.page_scroll(page)
    else:
        pass
"""

def get_screenshot(page, folder_path, file_name):
    try:
        page.wait_for_load_state('networkidle')
    except:
        page.wait_for_timeout(3000)
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