# check_db.py
import sqlite3

def check_database(db_file="db.sqlite"):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    print(f"📂 Connected to {db_file}\n")

    # List tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("📌 Tables in database:", [t[0] for t in tables])

    if "products" in [t[0] for t in tables]:
        # Count rows
        cur.execute("SELECT COUNT(*) FROM products")
        total_rows = cur.fetchone()[0]
        print(f"\n✅ Total rows in 'products': {total_rows}\n")

        # Show sample rows
        cur.execute("SELECT * FROM products LIMIT 5")
        rows = cur.fetchall()
        print("🔎 Sample data (first 5 rows):")
        for row in rows:
            print(row)
    else:
        print("\n⚠️ No 'products' table found yet.")

    conn.close()

if __name__ == "__main__":
    check_database()
