from playwright.sync_api import sync_playwright
import json

def intercept_api_calls(route, request):
    # Handle intercepted API requests
    print("Intercepted request:", request.url)
    route.continue_()  # Continue the request as usual



with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    console_msg_details = {}
    def handle_console_message(console_message):
        index = len(console_msg_details)
        console_msg_details[index] = console_message.text  

    # Attach a listener to the page's console messages
    page.on('console', handle_console_message)

    # JavaScript code to set up MutationObserver
    mutation_observer_script = """
        const rootNode = document.body;
        const observerConfig = { childList: true, attributes: true, characterData: true, subtree: true };

        function mutationCallback(mutationsList, observer) {
            for (const mutation of mutationsList) {
                console.log('Mutation type:', mutation.type);
            }
        }

        const observer = new MutationObserver(mutationCallback);
        observer.observe(rootNode, observerConfig);
    """

    tracking_script = """
        // Create a Proxy to intercept function calls
        window = new Proxy(window, {
            get(target, propKey, receiver) {
                const originalMethod = target[propKey];
                if (typeof originalMethod === 'function') {
                    return function (...args) {
                        const functionName = propKey.toString();
                        console.log('Function called:', functionName, 'with args:', args); // Log function name and args
                        const result = originalMethod.apply(this, args);
                        return result;
                    };
                }
                return originalMethod;
            },
        });
    """

    # Set up request interception
    page.route('**/api/**', intercept_api_calls)

    # Enable request interception
    def request_handler(route, request):
        route.continue_()
    page.route('**', request_handler)
    
    overall_request_details = {}  # Dictionary to store request details with index as key
    overall_response_details = {}  # Dictionary to store response details with index as key

    # Listen for network requests
    def request_listener(request):
        request_details = {}
        request_details["Request Url"] = request.url
        request_details["Request Method"] = request.method
        request_details["Request Headers"] = dict(request.headers)
        request_details["Request Resource Type"] = request.resource_type # type of the resource being requested
        request_details['Request Frame'] = request.frame.url if request.frame else None # The frame associated with the request.
        
        # Information about request failure (if applicable).
        request_details["Request Failure"] = {
            "errorText": request.failure.error_text,
            "errorCode": request.failure.error_code
        } if request.failure else None 

        
        # Add the request details to the dictionary using the index as key
        index = len(overall_request_details)
        overall_request_details[index] = request_details

    page.on('request', request_listener)

    

    # Listen for network responses
    def response_listener(response):
        response_details = {}
        response_details["Response Url"] = response.url
        response_details["Response Status"] = f"{response.status} {response.status_text}" 
        response_details["Response Headers"] = dict(response.headers)
        response_details["Response Frame"] = response.frame.url if response.frame else None # The frame associated with the response
        response_details["Corresponding Request"] = response.request.url 

        # Add the request details to the dictionary using the index as key
        index = len(overall_response_details)
        overall_response_details[index] = response_details

    page.on('response', response_listener)

    # Inject the MutationObserver setup code and the tracking script
    #combined_script = mutation_observer_script + tracking_script
    #page.evaluate(combined_script)

    
    # Execute the MutationObserver setup code
    page.evaluate(mutation_observer_script)

    # Inject the tracking script
    page.evaluate(tracking_script)
    

    # Navigate to the webpage
    page.goto('https://www.google.com/')


    # Continue with your crawling logic
    # ...

    with open('request_details.json', 'w') as json_file:
        json.dump(overall_request_details, json_file, indent=4)
    
    with open('response_details.json', 'w') as json_file:
        json.dump(overall_response_details, json_file, indent=4)
    
    with open('console_messages.json', 'w') as json_file:
        json.dump(console_msg_details, json_file, indent=4)

    browser.close()