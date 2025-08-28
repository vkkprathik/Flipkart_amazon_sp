from data_extractor import run_extraction

# --- Config ---
SEARCH_QUERY = "washing machine"
OUTPUT_FILE = r"D:\Day_Task\amazon_scraper_project\products.csv"
TOTAL_PAGES = 16  # You can adjust this as needed

if __name__ == "__main__":
    run_extraction(SEARCH_QUERY, OUTPUT_FILE, total_pages=TOTAL_PAGES)
