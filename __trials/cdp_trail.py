from playwright.sync_api import sync_playwright


def visit_page_with_custom_settings():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Create a new context with the custom user-agent
        iphone_x = p.devices["iPhone X"]
        context = browser.new_context(
            **iphone_x,
            user_agent="Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.75 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        )

        # Use the custom referrer when navigating to a page
        page = context.new_page()
        # Set the referrer using extra HTTP headers
        page.set_extra_http_headers({
            'Referer': 'https://www.google.com'
        })
        page.goto('https://www.example.com')

        # ... rest of your code ...
        # Print out the user-agent and referrer from within the page
        print("User-Agent:", page.evaluate("() => navigator.userAgent"))
        print("Referrer:", page.evaluate("() => document.referrer"))

        browser.close()



def visit_page_with_cdp():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Attach a CDPSession to the page
        client = context.new_cdp_session(page)

        # Set the custom user-agent
        client.send("Network.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"})

        # Navigate to the page with a custom referrer
        client.send("Page.navigate", {"url": "https://www.example.com", "referrer": "https://www.google.com"})


        # ... rest of your code ...
        # Print out the user-agent and referrer from within the page
        print("User-Agent:", page.evaluate("() => navigator.userAgent"))
        print("Referrer:", page.evaluate("() => document.referrer"))


        browser.close()



visit_page_with_custom_settings()
visit_page_with_cdp()
