from bs4 import BeautifulSoup

def is_page_blank(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        
        # Remove script and style content as they don't affect visual representation
        # Avoids false negative
        for script in soup(["script", "style"]):
            script.extract()
        
        # Check for text content
        if soup.get_text(strip=True):
            return False
        
        # Check for tags other than html, head, and body
        significant_tags = [tag for tag in soup.find_all(True) if tag.name not in ['html', 'head', 'body']]
        if significant_tags:
            return False

    return True

file_path = "html_script_aft.html"
if is_page_blank(file_path):
    print(f"{file_path} is effectively blank.")
else:
    print(f"{file_path} is not blank.")
