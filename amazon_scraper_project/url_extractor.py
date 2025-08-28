import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]
BASE_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}
BASE_URL = "https://www.amazon.in/s"

import time
import random
def get_soup(url, params=None, retries=3):
    import random
    for attempt in range(retries):
        try:
            headers = BASE_HEADERS.copy()
            headers["User-Agent"] = random.choice(USER_AGENTS)
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(random.uniform(1, 3))  # polite delay
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request failed ({url}): {e}. Attempt {attempt+1}/{retries}")
            time.sleep(random.uniform(2, 5))
    return None

def extract_product_urls(search_query, total_pages=2):
    urls = []
    for page in range(1, total_pages + 1):
        print(f"📄 Scraping Amazon page {page}/{total_pages}...")
        params = {"k": search_query, "page": page}
        soup = get_soup(BASE_URL, params=params)
        if not soup:
            print(f"⚠️ Failed to get soup for page {page}")
            continue
        product_cards = soup.find_all("a", class_="a-link-normal s-no-outline")
        for card in product_cards:
            href = card.get("href")
            if href:
                urls.append("https://www.amazon.in" + href)
        time.sleep(random.uniform(2, 5))  # short delay between pages
    return urls
