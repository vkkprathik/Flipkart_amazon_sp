from data_extractor import run_extraction

if __name__ == "__main__":
    SEARCH_QUERY = "washing machine"
    OUTPUT_FILE = r"D:\Day_Task\flipkart_scraper_project\products.csv"

    run_extraction(SEARCH_QUERY, OUTPUT_FILE)
    