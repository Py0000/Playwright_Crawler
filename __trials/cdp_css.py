from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        # Connecting to the page.
        page = context.new_page()
        page.goto('https://example.com')  # Replace with your desired URL

        # Starting the CDPSession
        client = context.new_cdp_session(page)

        # Enable necessary domains for the CDP client.
        client.send("DOM.enable")
        client.send("CSS.enable")

        # Get all document style sheets.
        style_sheets = client.send("CSS.getAllStyleSheets")
        
        # Filtering out only external stylesheets
        external_style_sheets = [ss for ss in style_sheets['headers'] if ss['origin'] != "injected" and ss['origin'] != "user-agent" and ss["sourceURL"]]
        
        # Print out the external stylesheets info
        for ss in external_style_sheets:
            print(ss)

        browser.close()

main()
