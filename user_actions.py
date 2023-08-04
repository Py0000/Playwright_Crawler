import time
import random


def save_screenshot(page, save_file_loc):
    page.screenshot(path=save_file_loc)


def move_mouse_smoothly_top_left_bottom_right(page):
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