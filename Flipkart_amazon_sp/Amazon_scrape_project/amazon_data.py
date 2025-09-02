import asyncio
import sqlite3
import pandas as pd
import random
import time
from playwright.async_api import async_playwright

DB_FILE = "products.db"
INPUT_FILE = "amazon_urls.csv"
OUTPUT_FILE = "amazon_products.csv"

# -------------------- SQLite Setup --------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS amazon_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            brand TEXT,
            price TEXT,
            mrp TEXT,
            rating TEXT,
            reviews TEXT,
            discount TEXT
        )
    """)
    conn.commit()
    return conn

# -------------------- Helper Functions --------------------
def clean_value(value):
    if not value or str(value).strip() == "":
        return "N/A"
    val = str(value).strip()
    if "MRP" in val:
        return "N/A"
    return val

async def get_first_valid_text(locator):
    count = await locator.count()
    for i in range(count):
        try:
            text = (await locator.nth(i).inner_text()).strip()
            if text:
                return text
        except:
            continue
    return "N/A"

def calculate_discount(price, mrp):
    try:
        price_num = float(price.replace(',', '').replace('₹','').strip())
        mrp_num = float(mrp.replace(',', '').replace('₹','').strip())
        if mrp_num > price_num:
            return f"{round((mrp_num - price_num)/mrp_num*100, 2)}%"
        return "0%"
    except:
        return "N/A"

# -------------------- Scraping Function --------------------
async def extract_product_data(page, url):
    try:
        await page.goto(url, timeout=120000)
        await page.wait_for_timeout(2000)

        # Scraping with multiple fallbacks
        title = await get_first_valid_text(page.locator("span#productTitle"))
        brand = await get_first_valid_text(page.locator("a#bylineInfo, tr.po-brand td.a-span9 span"))
        price = await get_first_valid_text(page.locator(
            "span.a-price-whole, span#corePrice_feature_div span.a-price-whole, span#priceblock_ourprice"))
        mrp = await get_first_valid_text(page.locator(
            "span.a-text-price span, span#priceblock_listprice, span.priceBlockStrikePriceString"))
        rating = await get_first_valid_text(page.locator(
            "span.a-icon-alt, span[data-hook='rating-out-of-text']"))
        reviews = await get_first_valid_text(page.locator(
            "span#acrCustomerReviewText, span[data-hook='total-review-count']"))

        discount = calculate_discount(price, mrp)

        # Clean values
        return {
            "title": clean_value(title),
            "url": url,
            "brand": clean_value(brand),
            "price": clean_value(price),
            "mrp": clean_value(mrp),
            "rating": clean_value(rating),
            "reviews": clean_value(reviews),
            "discount": clean_value(discount)
        }

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

# -------------------- Main Runner --------------------
async def main():
    df_urls = pd.read_csv(INPUT_FILE)
    urls = df_urls["url"].tolist()

    conn = init_db()
    cur = conn.cursor()

    all_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for idx, url in enumerate(urls, 1):
            print(f"📄 [{idx}/{len(urls)}] Scraping {url}")
            data = await extract_product_data(page, url)
            if data:
                all_data.append(data)

                # Insert into DB
                cur.execute("""
                    INSERT INTO amazon_products (title, url, brand, price, mrp, rating, reviews, discount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["title"], data["url"], data["brand"], data["price"],
                    data["mrp"], data["rating"], data["reviews"], data["discount"]
                ))
                conn.commit()

            await asyncio.sleep(random.uniform(1, 2))

        await browser.close()

    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    conn.close()
    print(f"✅ Scraping finished. Saved {len(df)} products to CSV & SQLite")

# -------------------- Run --------------------
if __name__ == "__main__":
    asyncio.run(main())
