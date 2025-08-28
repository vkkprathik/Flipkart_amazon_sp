import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}
BASE_URL = "https://www.flipkart.com/search"

def get_soup(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_product_urls(search_query, total_pages=2):
    urls = []
    for page in range(1, total_pages + 1):
        params = {"q": search_query, "page": page}
        soup = get_soup(BASE_URL, params=params)
        product_cards = soup.find_all("a", class_="CGtC98")
        for card in product_cards:
            urls.append("https://www.flipkart.com" + card["href"])
    return urls
