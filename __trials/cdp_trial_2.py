import json
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    # Create a CDP session for the page
    client = page.context.new_cdp_session(page)

    # Enable the Network domain to receive network-related events
    client.send("Network.enable")

    captured_events = []  # List to store the captured events

    # Use this flag to prevent concurrent calls to capture_request
    #capturing = False

    # Set up an event listener for requestWillBeSent
    def capture_request(payload):
        """
        global capturing
        if capturing:
            return
        capturing = True
        """
        captured_event = payload

        cookies = client.send("Network.getCookies", {"requestId": payload["requestId"]})
        captured_event["cookies"] = cookies
        
        captured_events.append(captured_event)
        #capturing = False

    client.on("Network.requestWillBeSent", capture_request)

    # Navigate to a website (for demonstration purposes)
    page.goto("https://www.google.com")
    page.wait_for_load_state('networkidle')

    # Close the browser after ensuring all requests are captured
    client.detach()  # Detach the CDP session
    page.close()     # Close the page
    browser.close()

    # Save the captured events to a JSON file
    with open('output.json', 'w') as file:
        json.dump(captured_events, file, indent=4)
