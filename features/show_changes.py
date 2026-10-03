import sqlite3
import pandas as pd

conn = sqlite3.connect("data/prices.db")

# every price row, with the product name attached
df = pd.read_sql(
    "SELECT p.name, pr.product_id, pr.scraped_at, pr.price "
    "FROM prices pr JOIN products p ON p.id = pr.product_id "
    "ORDER BY pr.product_id, pr.scraped_at",
    conn,
)

# put each price next to the one before it (same product)
df["prev_price"] = df.groupby("product_id")["price"].shift()

# keep only rows where the price is different from before
changed = df[df["prev_price"].notna() & (df["price"] != df["prev_price"])].copy()
changed["change_pct"] = ((changed["price"] - changed["prev_price"])
                         / changed["prev_price"] * 100).round(1)
changed["name"] = changed["name"].str[:35]

cols = ["name", "scraped_at", "prev_price", "price", "change_pct"]
print(f"Total price changes: {len(changed)}\n")

print("Biggest drops:")
print(changed.sort_values("change_pct")[cols].head(15).to_string(index=False))

print("\nBiggest increases:")
print(changed.sort_values("change_pct", ascending=False)[cols].head(15).to_string(index=False))

big_drops = (changed["change_pct"] <= -5).sum()
print(f"\nDrops of 5% or more: {big_drops}")