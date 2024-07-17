import requests
from bs4 import BeautifulSoup
import time
import logging

logger = logging.getLogger(__name__)

def crawl_website(url: str, depth: int = 5):
    logger.info(f"Starting crawl on {url} with depth {depth}")
    visited = set()
    data = []

    def crawl(url: str, depth: int):
        if depth == 0 or url in visited:
            logger.debug(f"Skipping URL: {url}, Depth: {depth}")
            return
        visited.add(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            data.append(soup.text)
            logger.info(f"Crawled URL: {url}")
            for link in soup.find_all('a', href=True):
                next_url = link['href']
                if next_url.startswith('/'):
                    next_url = url + next_url
                if next_url.startswith('http'):
                    time.sleep(1)  # To avoid overloading the server
                    crawl(next_url, depth - 1)
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")

    crawl(url, depth)
    return ' '.join(data)