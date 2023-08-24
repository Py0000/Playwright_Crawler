import json
import os

import definitions

# Enable route interception to prevent certain requests
# If the request's resource type is a script or an XHR request, it's aborted (preventing JavaScript execution). 
# Otherwise, it continues loading other resources.
def intercept_script_xhr_requests(route, request):
    if request.resource_type in ('script', 'xhr'):
        route.abort()
    else:
        route.continue_()




console_msg_details = {} # Dictionary to store console logs with index as key
consolidated_request_details = {}  # Dictionary to store request details with index as key
consolidated_response_details = {}  # Dictionary to store response details with index as key


# JavaScript code to set up MutationObserver
# Monitors the changes in the DOM 
# Mutations related to child elements being added or removed will be tracked
# Mutations related to attribute changes will be tracked
# Mutations related to text content changes will be tracked
# Mutations within the entire subtree of the root node will be tracked
mutation_observer_script = """
    const rootNode = document;
    const observerConfig = { 
        childList: true, 
        attributes: true, 
        characterData: true, 
        subtree: true,
        attributeFilter: ['class', 'style'] 
    };

    function mutationCallback(mutationsList, observer) {
        for (const mutation of mutationsList) {
            console.log('Mutation type:', mutation.type);
        }
    }

    const observer = new MutationObserver(mutationCallback);
    observer.observe(rootNode, observerConfig);
"""



# Intercepts function calls and log information about the called functions and their arguments
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



def generate_logs_folder(base_folder_name, index):
    sub_folders = [definitions.SUBFOLDER_BEFORE, definitions.SUBFOLDER_AFTER]

    indexed_folder = os.path.join(os.getcwd(), base_folder_name, definitions.CRAWLED_NETWORK_LOGS_FOLDER, index)
    if not os.path.exists(indexed_folder):
        os.makedirs(indexed_folder)
    
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(indexed_folder, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)
    
    return indexed_folder



def intercept_api_calls(route, request):
    # Handle intercepted API requests
    print("Intercepted request:", request.url)
    route.continue_()  # Continue the request as usual




def intercept_network_request(page, base_folder_name, index, before_after_flag):
    
    def handle_console_message_listener(console_message):
        index = len(console_msg_details)
        console_msg_details[index] = console_message.text
    
    # Attach a listener to the page's console messages
    page.on('console', handle_console_message_listener)

    # Set up request interception
    page.route('**/api/**', intercept_api_calls)

    # Enable request interception
    def request_handler(route, request):
        route.continue_()

    page.route('**', request_handler)


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
        index = len(consolidated_request_details)
        consolidated_request_details[index] = request_details

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
        index = len(consolidated_response_details)
        consolidated_response_details[index] = response_details

    page.on('response', response_listener)

    # Execute the MutationObserver setup code
    page.evaluate(mutation_observer_script)

    # Inject the tracking script
    page.evaluate(tracking_script)

    logs_folder_path = generate_logs_folder(base_folder_name, index)

    request_save_loc = os.path.join(logs_folder_path, before_after_flag, definitions.NETWORK_LOGS_REQUEST_FILE)
    response_save_loc = os.path.join(logs_folder_path, before_after_flag, definitions.NETWORK_LOGS_RESPONSE_FILE)
    console_save_loc = os.path.join(logs_folder_path, before_after_flag, definitions.NETWORK_LOGS_DOM_FUNCTION_FILE)

    with open(request_save_loc, 'w') as json_file:
        json.dump(consolidated_request_details, json_file, indent=4)
    
    with open(response_save_loc, 'w') as json_file:
        json.dump(consolidated_response_details, json_file, indent=4)
    
    with open(console_save_loc, 'w') as json_file:
        json.dump(console_msg_details, json_file, indent=4)



# Get client-side scripts
client_side_scripts_injection_code = '''() => {
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
}'''