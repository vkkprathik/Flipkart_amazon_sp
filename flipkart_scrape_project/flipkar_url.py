# url.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

BASE_URL = "https://www.flipkart.com/search"

def get_soup(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_product_urls(search_query, total_pages=50):
    urls = []
    for page in range(1, total_pages + 1):
        print(f"🔗 Extracting page {page}/{total_pages}")
        params = {"q": search_query, "page": page}
        soup = get_soup(BASE_URL, params=params)

        # Flipkart product links container
        product_cards = soup.find_all("a", class_="CGtC98")  # class may change
        for card in product_cards:
            url = "https://www.flipkart.com" + card.get("href")
            urls.append(url)
        time.sleep(random.uniform(1, 2))  # polite delay

    return urls

if __name__ == "__main__":
    search_query = "washing machine"
    output_file = "flipkart_urls.csv"
    urls = extract_product_urls(search_query, total_pages=50)

    df = pd.DataFrame({"url": urls})
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Saved {len(urls)} URLs to {output_file}")
