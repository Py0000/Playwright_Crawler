import time
import random


def save_screenshot(page, save_file_loc):
    try: 
        page.screenshot(path=save_file_loc)
    except:
        print("UNABLE TO SAVE SCREENSHOT...")



def mouse_click(page, direction):
    try:
        # Perform right-click at the current mouse position
        page.mouse.down(button=direction)
        page.mouse.up(button=direction)
        print(f"Mouse {direction} click successful...")
    except:
        print(f"MOUSE {direction} CLICK UNSUCCESSFUL")
    


def move_mouse_smoothly_top_left_bottom_right(page):
    try:
        steps = 100

        start_x = 0
        start_y = 0

        # Get the size of the page
        page_size = page.evaluate('''() => ({ width: document.documentElement.clientWidth, height: document.documentElement.clientHeight })''')
        end_x, end_y = page_size['width'], page_size['height']

        step_size_x = (end_x - start_x) / steps
        step_size_y = (end_y - start_y) / steps

        for i in range(steps + 1):
            x = start_x + step_size_x * i
            y = start_y + step_size_y * i

            # Move the mouse to the calculated coordinates
            page.mouse.move(x, y)

            # Add a small delay to simulate smooth movement (adjust the time for your desired smoothness)
            time.sleep(random.uniform(0.005, 0.01))

            print("Mouse moved: ", i)
    except:
        print("ERROR MOVING MOUSE...")
    

def page_scroll_helper(page, current_height):
    page_height = page.evaluate('() => document.documentElement.scrollHeight')

    while True:
        # randomly break the scoll to make it more like human scrolling
        rand_scoll_divider = random.randint(3,10)
        scroll_distance = page_height / rand_scoll_divider

        # scroll to selected portion of page with random small delays
        page.evaluate(f'window.scrollTo(0, {current_height + scroll_distance});')
        time.sleep(random.uniform(0.5, 1.0))

        current_height += scroll_distance
        if (current_height >= page_height):
            break
    
    return current_height


def page_scroll(page):
    last_height = page.evaluate('() => document.documentElement.scrollHeight')

    try:
        current_height = 0
        while True:

            # Scoll to end of current displayed page 
            current_height = page_scroll_helper(page, current_height)

            # Check whether if it is still possible to scroll
            # Continue while loop to scroll if possible
            # Otherwise stop scrolling
            new_height = page.evaluate('() => document.documentElement.scrollHeight')
            if (new_height == last_height):
                break

            last_height = new_height

        print("Page Scroll Success...")
    
    except Exception as e:
        print("PAGE SCROLL FAILED...")
        print(e)
    

def dismiss_js_alert(page):
    try:
        page.on("dialog", lambda dialog: dialog.accept())
        print("Alert dismissed successfully...")
    except:
        print("ALERT NOT DISMISSED...")