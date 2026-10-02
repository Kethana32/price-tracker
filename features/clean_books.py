import pandas as pd

df = pd.read_csv("data/books_raw.csv")

# "£51.77" -> 51.77  (remove everything except digits and the dot)
df["price"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)

# "Three" -> 3
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["rating"] = df["rating"].map(rating_map)

# "In stock" -> True/False
df["in_stock"] = df["availability"].str.contains("In stock")
df = df.drop(columns=["availability"])

df = df.drop_duplicates(subset="url")
print(df.isna().sum())
print(df.describe())

df.to_csv("data/books_clean.csv", index=False)
print(f"\nSaved {len(df)} clean rows to data/books_clean.csv")