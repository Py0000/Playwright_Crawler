import os
import base64
import hashlib
from playwright.sync_api import sync_playwright

# Directory to save downloaded files
DOWNLOAD_DIR = "downloaded_files"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Connect to Chrome DevTools Protocol
        client = page.context.new_cdp_session(page)

        # Enable the necessary CDP domains
        client.send("Network.enable")

        responses = {}  # Initialize this at the beginning

        def handle_response(params):
            print(f"Response URL: {params['response']['url']}")
            requestId = params["requestId"]

            # Store response details
            responses[requestId] = {
                "params": params,
                "responseReceived": True,
                "loadingFinished": False
            }

        def handle_loading_finished(params):
            requestId = params["requestId"]
            if requestId not in responses:
                # If for some reason the responseReceived event was missed
                return
            responses[requestId]["loadingFinished"] = True
            
            # Now check if both responseReceived and loadingFinished are True for this requestId
            if responses[requestId]["responseReceived"] and responses[requestId]["loadingFinished"]:
                save_response_content(requestId)

        # Capture request data
        def handle_request(params):
            url = params['request']['url']
            print(f"Request URL: {url}")

        # Capture and download response data
        def save_response_content(requestId):
            params = responses[requestId]["params"]
            url = params['response']['url']
            print(f"Response URL: {url}")

            # Check for HTTP status codes that don't carry content.
            if params['response']['status'] in [204, 304]:
                print("Encountered 204 or 304")
                return

            # Introduce a small delay
            page.wait_for_timeout(500)  # Or any other suitable delay
            
            # Get response body using CDP
            response_body = client.send("Network.getResponseBody", {"requestId": params['requestId']})

            mime_type = params['response']['mimeType']
            file_name = os.path.join(DOWNLOAD_DIR, f"{hashlib.sha256(url.encode()).hexdigest()}")
            
            # Decode base64 if needed
            if response_body['base64Encoded']:
                decoded_data = base64.b64decode(response_body['body'])
            else:
                decoded_data = response_body['body']

            # Save as text or binary based on MIME type
            if "html" in mime_type:
                 with open(file_name + ".html", "w", encoding="utf-8") as f:
                    f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
            elif "xml" in mime_type:
                 with open(file_name + ".xml", "w", encoding="utf-8") as f:
                    f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
            elif "json" in mime_type:
                with open(file_name + ".json", "w", encoding="utf-8") as f:
                    f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
            elif "javascript" in mime_type:
                with open(file_name + ".js", "w", encoding="utf-8") as f:
                    f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
            elif "css" in mime_type:
                with open(file_name + ".css", "w", encoding="utf-8") as f:
                    f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
            elif "image" in mime_type:
                with open(file_name + ".png", "wb") as f:
                    f.write(decoded_data)
            elif "audio" in mime_type:
                with open(file_name + ".mp3", "wb") as f:
                    f.write(decoded_data)
            elif "font/woff2" in mime_type:
                with open(file_name + ".woff2", "wb") as f:
                    f.write(decoded_data)
            elif "text" in mime_type:
                with open(file_name + ".txt", "w", encoding="utf-8") as f:
                    f.write(decoded_data if isinstance(decoded_data, str) else decoded_data.decode('utf-8'))
            else:
                # Default: save as binary
                with open(file_name + ".bin", "wb") as f:
                    f.write(decoded_data)

        # Set the listeners
        client.on("Network.requestWillBeSent", handle_request)
        client.on("Network.responseReceived", handle_response)
        client.on("Network.loadingFinished", handle_loading_finished)

        # Navigate to the desired URL
        page.goto("https://www.google.com/")

        # Do other stuff or wait as necessary
        page.wait_for_timeout(5000)

        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()
