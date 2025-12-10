import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website(base_url, max_pages=10):
    """
    Crawls a website and returns a list of all internal URLs found.
    """
    visited_urls = set()
    urls_to_visit = [base_url]
    found_links = []
    
    base_domain = urlparse(base_url).netloc
    
    # Add base_url first so we scan the homepage too
    found_links.append(base_url)
    visited_urls.add(base_url)

    print(f"🕷️ Spider started on: {base_url}")
    
    while urls_to_visit and len(found_links) < max_pages:
        current_url = urls_to_visit.pop(0)
        
        try:
            response = requests.get(current_url, timeout=3)
            
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(base_url, href)
                    
                    if urlparse(full_url).netloc == base_domain:
                        if full_url not in visited_urls:
                            visited_urls.add(full_url)
                            found_links.append(full_url)
                            urls_to_visit.append(full_url)
                            
        except Exception:
            pass # Ignore errors for now

    return list(set(found_links)) # Return unique links