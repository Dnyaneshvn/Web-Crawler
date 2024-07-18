# import requests
# from bs4 import BeautifulSoup
# import time
# import logging

# logger = logging.getLogger(__name__)

# def crawl_website(url: str, depth: int = 5):
#     logger.info(f"Starting crawl on {url} with depth {depth}")
#     visited = set()
#     data = []

#     def crawl(url: str, depth: int):
#         if depth == 0 or url in visited:
#             logger.debug(f"Skipping URL: {url}, Depth: {depth}")
#             return
#         visited.add(url)
#         try:
#             response = requests.get(url)
#             soup = BeautifulSoup(response.content, 'html.parser')
#             data.append(soup.text)
#             logger.info(f"Crawled URL: {url}")
#             for link in soup.find_all('a', href=True):
#                 next_url = link['href']
#                 if next_url.startswith('/'):
#                     next_url = url + next_url
#                 if next_url.startswith('http'):
#                     time.sleep(1)  # To avoid overloading the server
#                     crawl(next_url, depth - 1)
#         except Exception as e:
#             logger.error(f"Failed to crawl {url}: {e}")

#     crawl(url, depth)
#     return ' '.join(data)


import requests
from bs4 import BeautifulSoup
import time
import logging
import json
import os

logger = logging.getLogger(__name__)

def load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return json.load(f)
    return None

def save_checkpoint(data, checkpoint_file):
    with open(checkpoint_file, 'w') as f:
        json.dump(data, f)

def crawl_website(url: str, depth: int = 2, checkpoint_file='crawl_checkpoint.json'):
    logger.info(f"Starting crawl on {url} with depth {depth}")
    checkpoint = load_checkpoint(checkpoint_file)
    if checkpoint:
        visited = set(checkpoint['visited'])
        data = checkpoint['data']
        to_crawl = checkpoint['to_crawl']
        logger.info("Resuming from checkpoint")
    else:
        visited = set()
        data = []
        to_crawl = [(url, depth)]

    while to_crawl:
        current_url, current_depth = to_crawl.pop(0)
        if current_depth == 0 or current_url in visited:
            continue
        visited.add(current_url)
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            data.append({"url": current_url, "content": soup.text})
            logger.info(f"Crawled URL: {current_url} at depth {current_depth}")
            if current_depth > 1:
                for link in soup.find_all('a', href=True):
                    next_url = link['href']
                    if next_url.startswith('/'):
                        next_url = url + next_url
                    if next_url.startswith('http'):
                        to_crawl.append((next_url, current_depth - 1))
            save_checkpoint({"visited": list(visited), "data": data, "to_crawl": to_crawl}, checkpoint_file)
        except Exception as e:
            logger.error(f"Failed to crawl {current_url}: {e}")

    os.remove(checkpoint_file)  # Remove checkpoint file after successful crawl
    return data