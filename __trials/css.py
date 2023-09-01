import requests
from playwright.sync_api import sync_playwright

def get_css_urls(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        css_urls = []
        
        # Monitor network requests for CSS files
        def handle_request(request):
            if request.resource_type == "stylesheet":
                css_urls.append(request.url)

        #page.on("request", handle_request)

        page.goto(url, wait_until="networkidle")
        # Get all link elements that have a rel attribute of stylesheet
        
        static_css_urls = page.eval_on_selector_all("link[rel='stylesheet']", "links => links.map(link => link.href)")
        for url in static_css_urls:
            css_urls.append(url)

        browser.close()
        return css_urls

def save_css_files(css_urls):
    for i, css_url in enumerate(css_urls):
        response = requests.get(css_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create a file with a name like 'style1.css', 'style2.css', etc.
            with open(f"style{i+1}.css", 'w', encoding='utf-8') as file:
                file.write(response.text)
        else:
            print(f"Failed to download {css_url}")

if __name__ == "__main__":
    url = "https://www.youtube.com"  # Replace with your desired URL
    css_files = get_css_urls(url)
    save_css_files(css_files)
