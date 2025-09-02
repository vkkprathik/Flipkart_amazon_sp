import asyncio
import pandas as pd
import random
from urllib.parse import urljoin
from playwright.async_api import async_playwright

SEARCH_QUERY = "washing machine"  # Change your search term here
MAX_PAGES = 15
OUTPUT_FILE = "amazon_urls.csv"

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
]

async def scrape_amazon_urls():
    urls = []
    q = SEARCH_QUERY.replace(" ", "+")
    base_url = f"https://www.amazon.in/s?k={q}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)  # headless=False for debugging
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": random.randint(1200, 1400), "height": random.randint(700, 900)}
        )
        page = await context.new_page()

        for p_no in range(1, MAX_PAGES + 1):
            url = base_url + f"&page={p_no}"
            print(f"[Amazon] Collecting URLs from page {p_no}...")
            try:
                await page.goto(url, timeout=120000)
                await page.wait_for_selector("div.s-main-slot")
            except Exception as e:
                print(f"⚠️ Error loading page {p_no}: {e}")
                continue

            # Scroll slowly to load lazy content
            scroll_height = await page.evaluate("document.body.scrollHeight")
            for y in range(0, scroll_height, 300):
                await page.evaluate(f"window.scrollTo(0, {y})")
                await asyncio.sleep(random.uniform(0.5, 1.5))

            # Extract product URLs from <a class="a-link-normal s-no-outline">
            link_elements = await page.query_selector_all("a.a-link-normal.s-no-outline")
            for link_el in link_elements:
                href = await link_el.get_attribute("href")
                if href and "/dp/" in href:  # Only product pages
                    full_url = urljoin("https://www.amazon.in", href)
                    urls.append(full_url)
                    print(f"  ✅ Found: {full_url}")

            # Random delay between pages
            await asyncio.sleep(random.uniform(5, 10))

        await browser.close()

    # Remove duplicates and save to CSV
    urls = list(set(urls))
    pd.DataFrame(urls, columns=["url"]).to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved {len(urls)} product URLs to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(scrape_amazon_urls())
