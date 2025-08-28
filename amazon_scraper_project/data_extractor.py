import pandas as pd
import time
import random
from url_extractor import extract_product_urls
from product_extractor import extract_product_data

def run_extraction(search_query, output_file, total_pages=5):
    all_data = []

    # Get all product URLs
    urls = extract_product_urls(search_query, total_pages=total_pages)
    print(f"🔗 Found {len(urls)} product URLs")

    # Loop through URLs and extract data
    for idx, url in enumerate(urls, 1):
        print(f"📄 [{idx}/{len(urls)}] Extracting {url}")
        try:
            data = extract_product_data(url)
            if data:
                all_data.append(data)
        except Exception as e:
            print(f"⚠️ Failed to scrape {url}: {e}")
            continue

        # Polite delay
        time.sleep(random.uniform(1, 3))

    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Scraping finished. Saved {len(df)} products to {output_file}")
