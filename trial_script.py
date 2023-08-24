from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Enable route interception to prevent certain requests
    # If the request's resource type is a script or an XHR request, it's aborted (preventing JavaScript execution). 
    # Otherwise, it continues loading other resources.
    def intercept_requests(route, request):
        if request.resource_type in ('script', 'xhr'):
            route.abort()
        else:
            route.continue_()

    # Sets up route interception on the page. 
    # The '**/*' pattern matches all network requests. 
    # The intercept_requests function will be called whenever a request is made.
    page.route('**/*', intercept_requests)

    # Navigate to the URL of the webpage you want to analyze
    page.goto('https://example.com')

    # Wait for the page to load
    page.wait_for_load_state('domcontentloaded')

    # Get the content before client-side rendering
    before_render_content = page.content()

    # Disable route interception to allow JavaScript execution
    page.unroute('**/*', intercept_requests)

    # Allow time for client-side rendering to complete
    page.wait_for_timeout(3000)  # 3 seconds in this example

    # Get the content after client-side rendering
    after_render_content = page.content()

    print('Server-side rendered content:', before_render_content)
    print('Client-side rendered content:', after_render_content)

    browser.close()

