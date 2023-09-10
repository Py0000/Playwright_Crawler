from bs4 import BeautifulSoup
import utility as util

def detect_suspicious_scripts(html_file_name):
    html_content = util.get_html_content(html_file_name)
    soup = BeautifulSoup(html_content, 'lxml')
    
    suspicious_scripts = []

    for script in soup.find_all('script'):
        # Check if it's an inline script
        if not script.attrs.get('src'):
            content = script.string
            if content:
                # Check for common obfuscation techniques
                if 'eval(' in content or 'String.fromCharCode(' in content:
                    suspicious_scripts.append(content)
                
    
    return suspicious_scripts