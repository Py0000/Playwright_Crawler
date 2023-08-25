from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Navigate to the webpage you want to analyze
    page.goto('https://www.google.com')

    # Get server-side script (HTML source)
    server_side_script = page.content()

    # Get client-side scripts
    client_side_scripts = page.evaluate('''() => {
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
    }''')

    # print('Server-side script:', server_side_script)
    # Format client-side scripts for better readability
    # Create a dictionary to store the client-side script data
    script_data = {}
    for index, script in enumerate(client_side_scripts):
        script_data[f'script_{index + 1}'] = script

    page.screenshot(path="screenshot.png", full_page=True)

    # Save data to a JSON file
    with open('scripts_data.json', 'w') as json_file:
        json.dump(script_data, json_file, indent=4)

    with open('server_scripts_data.json', 'w') as json_file:
        json.dump(server_side_script, json_file, indent=4)

    browser.close()
