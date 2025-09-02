# 🛒 Flipkart & Amazon Product Scraper

A **Python-based web scraping project** to extract product details from **Flipkart** and **Amazon**.  
The scraper collects product information such as:

- ✅ Product Name  
- ✅ Price  
- ✅ Brand  
- ✅ Rating & Review Count  
- ✅ Product URL  

The scraped data is stored in **CSV** and **JSON** formats for analysis.

---

## 📂 Project Structure

Flipkart_amazon_sp/
│── amazon_scrape_project/ # Amazon scraper logic
│ ├── amazon_scraper.py
│ └── init.py
│
│── flipkart_scrape_project/ # Flipkart scraper logic
│ ├── flipkart_scraper.py
│ └── init.py
│
│── output/ # Scraped data (CSV & JSON)
│ ├── amazon_products.csv
│ 
│ ├── flipkart_products.csv
│ 
│
│── requirements.txt # Dependencies
│── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Features

- Scrapes **multiple product pages**  
- Extracts **name, brand, price, ratings, reviews, and URL**  
- Supports **Flipkart** & **Amazon** separately  
- Saves results into `CSV` and `JSON`  
- Implements random user agents & request delays  

---

## 🚀 Setup & Usage

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Flipkart_amazon_sp.git
cd Flipkart_amazon_sp
2️⃣ Install Requirements
bash
Copy code
pip install -r requirements.txt
3️⃣ Run Flipkart Scraper
bash
Copy code
python flipkart_scrape_project/flipkart_scraper.py
4️⃣ Run Amazon Scraper
bash
Copy code
python amazon_scrape_project/amazon_scraper.py
5️⃣ Output
Scraped data will be saved inside the output/ folder:

bash
Copy code
output/flipkart_products.csv
output/amazon_products.csv

📊 Example Output
Flipkart (CSV/JSON)
Product Name	Price	Brand	Rating	URL
Samsung 6.5kg Washing Machine	₹15,990	Samsung	4.3 ⭐	View
Whirlpool 7kg Fully Automatic	₹18,499	Whirlpool	4.4 ⭐	View

Amazon (CSV/JSON)
Product Name	Price	Brand	Rating	URL
LG 7kg Front Load Washing Machine	₹22,990	LG	4.5 ⭐	View
IFB 6.5kg Fully Automatic	₹19,990	IFB	4.4 ⭐	View

 Notes
This scraper is for educational purposes only

Always respect website Terms of Service

Amazon & Flipkart may update their HTML structure, so code adjustments may be required

🛠️Tech Stack
Python 3.x

Requests / BeautifulSoup4 (for parsing)

Pandas (for saving CSV/JSON)

Random User-Agent (to avoid blocking)
