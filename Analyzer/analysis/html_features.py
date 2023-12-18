from urllib.parse import urlparse
import tldextract



#--------------------------------- Deals with title ---------------------------------
def has_title(soup):
    try: 
        return len(soup.title.next) > 0
    except:
        return False
    

def get_title(soup):
    if (has_title(soup)):
        return soup.title.get_text()
    else:
        return "NULL"
    

def length_of_title(soup):
    try:
        return len(soup.title.text)
    except:
        return 0 


def is_url_domain_in_title(soup, url):
    domain = tldextract.extract(url).domain
    try:
        return domain.lower() in soup.title.text.lower()
    except:
        return False 



#--------------------------------- Deals with forms & inputs ---------------------------------
def num_of_forms(soup):
    forms = soup.find_all('form')
    return len(forms) 

def num_of_forms_with_inputs(soup):
    forms = soup.find_all('form')
    count = 0
    for form in forms:
        if form.find('input'):
            count += 1
    return count 

def get_names_of_forms_with_inputs(soup):
    forms = soup.find_all('form')
    names = []
    for form in forms:
        inputs = form.find_all('input')
        for input in inputs:
            try:
                if 'name' in input:
                    names.append(str(input['name']))
            except:
                continue
    return names

def num_of_forms_with_dropdowns(soup):
    forms = soup.find_all('form')
    count = 0
    for form in forms:
        if form.find('select'):
            count += 1
    return count 

def get_names_of_forms_with_dropdowns(soup):
    forms = soup.find_all('form')
    names = []
    for form in forms:
        dropdowns = form.find_all('select')
        for dropdown in dropdowns:
            try:
                if 'name' in dropdown:
                    names.append(str(dropdown['name']))
            except:
                continue
    return names

def num_of_forms_with_textareas(soup):
    forms = soup.find_all('form')
    count = 0
    for form in forms:
        if form.find('textareas'):
            count += 1
    return count 

def get_names_of_forms_with_textareas(soup):
    forms = soup.find_all('form')
    names = []
    for form in forms:
        textareas = form.find_all('textareas')
        for textarea in textareas:
            try:
                if 'name' in textarea:
                    names.append(str(textarea['name']))
            except:
                continue
    return names


def get_list_of_buttons(soup):
    # Find all <button> elements
    button_tags = soup.find_all('button')  

    # Find <input> elements with type="button", "submit", or "reset"
    input_buttons = soup.find_all('input', {'type': 'button'})
    input_submits = soup.find_all('input', {'type': 'submit'})
    input_resets = soup.find_all('input', {'type': 'reset'})

    all_buttons = button_tags + input_buttons + input_submits + input_resets
    return all_buttons

def num_of_buttons(soup):
    buttons = get_list_of_buttons(soup)
    return len(buttons)


def num_of_disabled_buttons(soup):
    buttons = get_list_of_buttons(soup)
    count = 0
    for button in buttons:
        try:
            if str(button.attrs['disabled'])=='disabled':
                count += 1
        except:
            continue
    return count



#--------------------------------- Deals with links ---------------------------------
def num_of_anchor_url(soup):
    links = soup.find_all('a', href=True)
    return len(links)

def num_of_internal_external_links(soup, url):
    main_domain = tldextract.extract(url).domain
    links = soup.find_all('a', href=True)
    internal = 0
    external = 0

    for link in links:
        try:
            if "http" in link:
                domain = tldextract.extract(link).domain
                if str(domain) == main_domain:
                    internal += 1
                else:
                    external += 1
            else:
                # relative url (internal)
                internal += 1
        except:
            continue
    
    return [internal, external]

def num_of_empty_links(soup):
    links = soup.find_all('a')
    empty_count = 0

    def is_empty_link(link):
        empty_indicator = {"", "#", "#javascript::void(0)", "#content", "#skip", "javascript:;", "javascript::void(0);", "javascript::void(0)"}
        href_attr = link['href'].strip()
        return href_attr in empty_indicator

    for link in links:
        if not link.get('href') or is_empty_link(link):
            empty_count += 1
    
    return empty_count
    


#--------------------------------- Deals with iframes ---------------------------------
def num_of_iframes(soup):
    return len(soup.find_all("iframe"))

# width, height and frameborder attribute are all 0
# Or styles that make an iframe invisible
def num_of_invisible_iframes(soup):
    iframes = soup.find_all('iframe')
    count = 0
    for iframe in iframes:
        style = iframe.get('style', '').lower()
        hasNoWidth = iframe.get('width') == '0'
        hasNoHeight = iframe.get('height') == '0'
        hasNoFrameBorder = iframe.get('frameborder') == '0'
        if (hasNoWidth and hasNoHeight and hasNoFrameBorder):
            count += 1
        elif ('display: none' in style or 'visibility: hidden' in style):
            count += 1 
    
    return count

# atleast one of (width, height, frameborder) is 0
def num_of_semi_invisible_iframes(soup):
    iframes = soup.find_all('iframe')
    count = 0
    for iframe in iframes:
        hasNoWidth = iframe.get('width') == '0'
        hasNoHeight = iframe.get('height') == '0'
        hasNoFrameBorder = iframe.get('frameborder') == '0'
        if (hasNoWidth or hasNoHeight or hasNoFrameBorder):
            count += 1
    
    return count

# Check function
def num_of_visible_iframes(soup):
    iframes = soup.find_all('iframe')
    count = 0
    for iframe in iframes:
        hasWidth = iframe.get('width') != '0'
        hasHeight = iframe.get('height') != '0'
        hasFrameBorder = iframe.get('frameborder') != '0'
        if (hasWidth and hasHeight and hasFrameBorder):
            count += 1
    
    return count


# Get an external re-direction link that is present in the iframe if any
def iframe_src_analysis(soup):
    iframes = soup.find_all('iframe')
    src_attributes = []
    for iframe in iframes:
        src = iframe.get('src')
        if src:
            src_attributes.append(src)
    
    return src_attributes


# Get an external re-direction link that is present in the iframe if any
def iframe_src_analysis(soup):
    iframes = soup.find_all('iframe')
    src_attributes = []
    for iframe in iframes:
        src = iframe.get('src')
        if src:
            src_attributes.append(src)
    
    return src_attributes
    


#--------------------------------- Deals with auto redirects/refreshes ---------------------------------
def num_of_auto_redirect(soup):
    meta_refresh = soup.find_all('meta', {'http-equiv': 'refresh'})
    return len(meta_refresh)

# Content is typically = "time;url=target_url".
def auto_redirect_url(soup):
    meta_refresh = soup.find_all('meta', {'http-equiv': 'refresh'})
    urls = []

    for meta in meta_refresh:
        content = meta.get('content')
        if content:
            parts = content.split(';')
            for part in parts:
                if part.strip().lower().startswith('url='):
                    # Extract the URL part
                    url = part.strip()[4:]
                    urls.append(url)

    return urls
    


#--------------------------------- Deals with pop-up window ---------------------------------
def num_of_pop_up(soup):
    scripts = soup.find_all('script')
    pop_up = 0
    for script in scripts:
        try:
            if('alert' in str(script.contents)) or ('window.open' in str(script.contents)):
                pop_up += 1
        except:
            continue
    
    return pop_up
