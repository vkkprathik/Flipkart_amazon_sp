import requests
from bs4 import BeautifulSoup
import random

HEADERS = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"}
]

def extract_product_data(url):
    """Extract product details from an Amazon product page"""
    try:
        response = requests.get(url, headers=random.choice(HEADERS), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # --- Title ---
        title = soup.select_one("#productTitle")

        # --- Current Price ---
        price = soup.select_one(".a-price .a-offscreen")

        # --- Actual/Original Price (strikethrough) ---
        actual_price = soup.select_one("span.a-text-price .a-offscreen")

        # --- Rating ---
        rating = soup.select_one("span[data-asin][aria-label]")

        # --- Discount ---
        discount = soup.select_one("span.savingPriceOverride, span.savingsPercentage")

        # --- Brand (usually in product details table or top section) ---
        brand = None
        brand_tag = soup.find("a", {"id": "bylineInfo"})
        if not brand_tag:  # Sometimes in product details
            brand_row = soup.find("th", string="Brand")
            if brand_row:
                td = brand_row.find_next("td")
                if td:
                    brand = td.get_text(strip=True)
        else:
            brand = brand_tag.get_text(strip=True)

        return {
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "actual_price": actual_price.get_text(strip=True) if actual_price else None,
            "rating": rating.get_text(strip=True) if rating else None,
            "discount": discount.get_text(strip=True) if discount else None,
            "brand": brand,
            "url": url
        }

    except Exception as e:
        print(f"⚠️ Failed to extract {url}: {e}")
        return None
