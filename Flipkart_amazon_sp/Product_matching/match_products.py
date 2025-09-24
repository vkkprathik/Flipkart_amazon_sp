import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -----------------------------
# Step 1. Load Data
# -----------------------------
amazon_df = pd.read_csv("D:/Task_08_09/Product_matching/amazon-products-details-cleaned.csv")
flipkart_df = pd.read_csv("D:/Task_08_09/Product_matching/flipkart-products-csv.csv")

# Normalize column names
amazon_df = amazon_df.rename(columns=str.lower)
flipkart_df = flipkart_df.rename(columns=str.lower)

# Expected columns: title, brand, price, url
for col in ["title", "brand", "price"]:
    if col not in amazon_df.columns or col not in flipkart_df.columns:
        raise ValueError(f"❌ Missing required column: {col}")

# -----------------------------
# Step 2. Preprocess Text
# -----------------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # keep only alphanumeric
    text = re.sub(r'\s+', ' ', text).strip()
    return text

amazon_df["title_clean"] = amazon_df["title"].apply(clean_text)
flipkart_df["title_clean"] = flipkart_df["title"].apply(clean_text)

# -----------------------------
# Step 3. Helper Functions
# -----------------------------
def extract_models(title):
    """Extracts storage, ram, processor, year, suffix terms."""
    patterns = [
        r"\d+\s?gb", r"\d+\s?tb", r"\d+\s?inch",
        r"i[3579]", r"ryzen\s?\d",
        r"\d{4}", r"pro", r"max", r"ultra"
    ]
    found = []
    for p in patterns:
        matches = re.findall(p, title.lower())
        found.extend(matches)
    return set(found)

def model_match_score(title_a, title_b):
    models_a = extract_models(title_a)
    models_b = extract_models(title_b)
    if not models_a or not models_b:
        return 0
    overlap = models_a.intersection(models_b)
    return len(overlap) / max(len(models_a), len(models_b))

def price_similarity(price_a, price_b):
    """Returns 1 if same, else reduces with difference."""
    try:
        price_a, price_b = float(price_a), float(price_b)
        if price_a <= 0 or price_b <= 0:
            return 0
        diff = abs(price_a - price_b) / max(price_a, price_b)
        return max(0, 1 - diff)  # closer price = higher score
    except:
        return 0

def brand_score(brand_a, brand_b):
    if not brand_a or not brand_b:
        return 0
    return 1 if str(brand_a).strip().lower() == str(brand_b).strip().lower() else 0

# -----------------------------
# Step 4. Embeddings
# -----------------------------
print("⚡ Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

amazon_vecs = model.encode(amazon_df["title_clean"].tolist(), convert_to_numpy=True)
flipkart_vecs = model.encode(flipkart_df["title_clean"].tolist(), convert_to_numpy=True)

# -----------------------------
# Step 5. FAISS Index
# -----------------------------
d = amazon_vecs.shape[1]
index = faiss.IndexFlatL2(d)
index.add(flipkart_vecs)

# -----------------------------
# Step 6. Matching
# -----------------------------
k = 1  # get top-1 best match
distances, indices = index.search(amazon_vecs, k)

matches = []
for i, (dist, idx) in enumerate(zip(distances, indices)):
    amazon_title = amazon_df.iloc[i]["title"]
    amazon_price = amazon_df.iloc[i].get("price", None)
    amazon_brand = amazon_df.iloc[i].get("brand", "")
    amazon_url = amazon_df.iloc[i].get("url", "")

    flip_title = flipkart_df.iloc[idx[0]]["title"]
    flip_price = flipkart_df.iloc[idx[0]].get("price", None)
    flip_brand = flipkart_df.iloc[idx[0]].get("brand", "")
    flip_url = flipkart_df.iloc[idx[0]].get("url", "")

    # Scores
    embedding_sim = 1 - dist[0]  # lower distance = higher sim
    b_score = brand_score(amazon_brand, flip_brand)
    p_score = price_similarity(amazon_price, flip_price)
    m_score = model_match_score(amazon_title, flip_title)

    # Weighted Final Score
    final_score = (0.5 * embedding_sim) + (0.2 * b_score) + (0.2 * p_score) + (0.1 * m_score)

    matches.append({
        "Amazon_Title": amazon_title,
        "Amazon_Brand": amazon_brand,
        "Amazon_Price": amazon_price,
        "Amazon_URL": amazon_url,
        "Flipkart_Title": flip_title,
        "Flipkart_Brand": flip_brand,
        "Flipkart_Price": flip_price,
        "Flipkart_URL": flip_url,
        "Embedding_Sim": round(embedding_sim, 4),
        "Brand_Score": b_score,
        "Price_Score": round(p_score, 3),
        "Model_Score": round(m_score, 3),
        "Final_Score": round(final_score, 4)
    })

# -----------------------------
# Step 7. Save Results
# -----------------------------
matched_df = pd.DataFrame(matches)
matched_df = matched_df.sort_values(by="Final_Score", ascending=False)  # best matches first
matched_df.to_csv("MatchedProducts.csv", index=False)

print("✅ Matching complete! Results saved to MatchedProducts.csv")
