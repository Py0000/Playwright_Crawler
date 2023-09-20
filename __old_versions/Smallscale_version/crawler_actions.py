import time
import random

async def mouse_click(page, direction):
    try:
        # Perform right-click at the current mouse position
        await page.mouse.down(button=direction)
        await page.mouse.up(button=direction)
        print(f"Mouse {direction} click successful...")
    except:
        print(f"MOUSE {direction} CLICK UNSUCCESSFUL")
    


async def move_mouse_smoothly_top_left_bottom_right(page):
    try:
        steps = random.randint(3,5)

        start_x = 0
        start_y = 0

        # Get the size of the page
        page_size = await page.evaluate('''() => ({ width: document.documentElement.clientWidth, height: document.documentElement.clientHeight })''')
        end_x, end_y = page_size['width'], page_size['height']

        step_size_x = (end_x - start_x) / steps
        step_size_y = (end_y - start_y) / steps

        for i in range(steps + 1):
            x = start_x + step_size_x * i
            y = start_y + step_size_y * i

            # Move the mouse to the calculated coordinates
            await page.mouse.move(x, y)

            # Add a small delay to simulate smooth movement (adjust the time for your desired smoothness)
            time.sleep(random.uniform(0.001, 0.003))

        print("Mouse moved sucessful...")
    except Exception as e:
        print("ERROR MOVING MOUSE: ", e)


async def page_scroll_helper(page, current_height):
    page_height = await page.evaluate('() => document.documentElement.scrollHeight')

    while True:
        # randomly break the scoll to make it more like human scrolling
        rand_scoll_divider = random.randint(6,10)
        scroll_distance = page_height / rand_scoll_divider

        # scroll to selected portion of page with random small delays
        await page.evaluate(f'window.scrollTo(0, {current_height + scroll_distance});')
        time.sleep(random.uniform(0.003, 0.005))

        current_height += scroll_distance
        if (current_height >= page_height):
            break
    
    return current_height


async def page_scroll(page):
    last_height = await page.evaluate('() => document.documentElement.scrollHeight')
    last_height = last_height/random.randint(4, 7)

    try:
        current_height = 0
        while True:

            # Scoll to end of current displayed page 
            current_height = await page_scroll_helper(page, current_height)

            # Check whether if it is still possible to scroll
            # Continue while loop to scroll if possible
            # Otherwise stop scrolling
            new_height = await page.evaluate('() => document.documentElement.scrollHeight')
            if (new_height >= last_height):
                break

            last_height = new_height

        print("Page Scroll Success...")
    
    except Exception as e:
        print("PAGE SCROLL FAILED: ", e)


async def dismiss_js_alert(page):
    try:
        await page.on("dialog", lambda dialog: dialog.accept())
        print("Alert dismissed successfully...")
    except Exception as e:
        print("ALERT NOT DISMISSED: ", e)


async def desktop_user_mouse_movement(page):
    await dismiss_js_alert(page)
    await move_mouse_smoothly_top_left_bottom_right(page)
    await mouse_click(page, 'left')
    await mouse_click(page, "right")
