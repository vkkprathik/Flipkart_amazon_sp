import pandas as pd

def clean_data(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    # Convert all column names to lowercase
    df.columns = [col.lower() for col in df.columns]

    # Replace null/empty with N/A
    df = df.fillna("N/A")

    # --- Clean discount column ---
    if "discount" in df.columns:
        df["discount"] = (
            df["discount"]
            .astype(str)
            .str.replace(r"[\(\)%]|off", "", regex=True)   # remove (), %, off
            .str.strip()
        )
        df["discount"] = df["discount"].replace("", "N/A")

    # --- Split reviews into rating_count and review_count ---
    if "reviews" in df.columns:
        df[["rating_count", "review_count"]] = df["reviews"].astype(str).str.extract(
            r"(?:(\d+(?:,\d+)*)\s*Ratings)?\s*(?:(\d+(?:,\d+)*)\s*Reviews)?"
        )
        df["rating_count"] = df["rating_count"].fillna("N/A")
        df["review_count"] = df["review_count"].fillna("N/A")
        df.drop(columns=["reviews"], inplace=True)

    # --- Remove 'highlths' column if exists ---
    if "highlths" in df.columns:
        df.drop(columns=["highlths"], inplace=True)

    # --- Clean numeric price values ---
    price_cols = [col for col in df.columns if "price" in col]
    for col in price_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[^\d]", "", regex=True)  # keep only digits
            .replace("", "N/A")
        )

    # Save cleaned file
    df.to_csv(output_file, index=False)
    print(f"✅ Cleaned dataset saved to {output_file}")


if __name__ == "__main__":
    input_file = "products.csv"             # your raw input file
    output_file = "products_cleaned_v2.csv" # cleaned output file
    clean_data(input_file, output_file)
