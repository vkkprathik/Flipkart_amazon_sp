from bs4 import BeautifulSoup
import requests
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_product_data(url):
    try:
        soup = get_soup(url)
        title = soup.find("span", class_="VU-ZEz")
        title = title.text.strip() if title else None

        rating = soup.find("div", class_="XQDdHH")
        rating = rating.text.strip() if rating else None

        reviews = soup.find("span", class_="Wphh3N")
        reviews = reviews.text.strip() if reviews else None

        

        price = soup.find("div", class_="Nx9bqj CxhGGd")
        price = price.text.strip() if price else None

        original_price = soup.find("div", class_="yRaY8j A6+E6v")
        original_price = original_price.text.strip() if original_price else None

        discount = soup.find("div", class_="UkUFwK")
        discount = discount.text.strip() if discount else None

        #  Extract brand robustly
        brand = None
        brand_cell = soup.find("td", string=lambda text: text and "Brand" in text)
        if brand_cell:
            sibling = brand_cell.find_next_sibling("td")
            if sibling:
                brand = sibling.get_text(strip=True)

        return {
            "title": title,
            "brand": brand,
            "rating": rating,
            "reviews": reviews,
            
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "url": url
        }

    except Exception as e:
        print(f" Failed to scrape {url}: {e}")
        return None
