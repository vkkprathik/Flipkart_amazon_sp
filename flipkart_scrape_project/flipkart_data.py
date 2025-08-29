import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import sqlite3
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

INPUT_FILE = "flipkart_urls.csv"
DB_FILE = "flipkart_products.db"

# -------------------- SQLite Setup --------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flipkart_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            brand TEXT,
            price TEXT,
            mrp TEXT,
            discount TEXT,
            rating TEXT,
            reviews TEXT,
            url TEXT
        )
    """)
    conn.commit()
    return conn

# -------------------- Helper Functions --------------------
def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def clean_value(val):
    return val.strip() if val else "N/A"

def calculate_discount(price, mrp):
    try:
        price_num = float(re.sub(r"[^\d.]", "", price))
        mrp_num = float(re.sub(r"[^\d.]", "", mrp))
        if mrp_num > price_num:
            return f"{round((mrp_num - price_num)/mrp_num*100, 2)}%"
        return "0%"
    except:
        return "N/A"

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

# -------------------- Main Script --------------------
if __name__ == "__main__":
    df_urls = pd.read_csv(INPUT_FILE)
    urls = df_urls["url"].tolist()

    conn = init_db()
    cur = conn.cursor()

    all_data = []
    for idx, url in enumerate(urls, 1):
        print(f"📄 [{idx}/{len(urls)}] Scraping {url}")
        data = extract_product_data(url)
        if data:
            all_data.append(data)
            cur.execute("""
                INSERT INTO flipkart_products (title, brand, price, mrp, discount, rating, reviews, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["title"], data["brand"], data["price"], data["original_price"],
                data["discount"], data["rating"], data["reviews"], data["url"]
            ))
            conn.commit()

        time.sleep(random.uniform(1, 2))

    df = pd.DataFrame(all_data)
    df.to_csv("flipkart_products.csv", index=False, encoding="utf-8-sig")
    conn.close()
    print(f"✅ Scraping finished. Saved {len(df)} products to CSV & SQLite")
