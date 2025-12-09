
import requests
from bs4 import BeautifulSoup

def crawl_website(url, limit=10):
    found_urls = []
    try:
        # Add headers to look like a real browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=3)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                found_urls.append(href)
                if len(found_urls) >= limit:
                    break
        return found_urls
    except Exception as e:
        return [f"Error crawling: {str(e)}"]