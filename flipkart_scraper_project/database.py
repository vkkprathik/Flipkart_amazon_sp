# database.py
import sqlite3
import pandas as pd

DB_NAME = "db.sqlite"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            title TEXT,
            rating TEXT,
            reviews TEXT,
            highlights TEXT,
            price TEXT,
            original_price TEXT,
            discount TEXT,
            url TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()


def insert_product(product):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO products
        (brand, title, rating, reviews, highlights, price, original_price, discount, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product.get("brand"),
        product.get("title"),
        product.get("rating"),
        product.get("reviews"),
        product.get("highlights"),
        product.get("price"),
        product.get("original_price"),
        product.get("discount"),
        product.get("url"),
    ))
    conn.commit()
    conn.close()


def insert_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        insert_product(row.to_dict())
    print(f"[INFO] Inserted {len(df)} products into {DB_NAME}")
