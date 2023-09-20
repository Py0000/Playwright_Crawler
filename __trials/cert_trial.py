import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Start a CDP session
        client = await page.context.new_cdp_session(page)

        # Enable the necessary CDP domains
        await client.send("Network.enable")

        security_details_list = []
        params_list = []  # List to store all the params

        # Handle the SecurityDetails event
        def print_security_details(params):
            print(params)
            params_list.append(params)  # Save the params to the list
            if 'securityDetails' in params:
                details = params['securityDetails']
                security_details_list.append(details)

        client.on("Network.responseReceived", print_security_details)

        # Navigate to a HTTPS page
        await page.goto("https://www.google.com")

        # Save the security details to a JSON file
        with open("security_details.json", "w") as outfile:
            json.dump(security_details_list, outfile, indent=4)

        # Save the params to a separate JSON file
        with open("params.json", "w") as outfile:
            json.dump(params_list, outfile, indent=4)

        # Close the browser after your tasks
        await browser.close()

asyncio.run(main())
