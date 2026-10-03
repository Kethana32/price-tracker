import sqlite3
import pandas as pd

conn = sqlite3.connect("data/prices.db")
df = pd.read_sql(
    "SELECT product_id, scraped_at, price FROM prices ORDER BY product_id, scraped_at",
    conn,
)

runs = df["scraped_at"].nunique()
print("Scrape runs so far:", runs)
if runs < 2:
    raise SystemExit("Need at least 2 runs to compare. Try again after the next scheduled run.")

# compare each price with the same variant's previous price
df["prev_price"] = df.groupby("product_id")["price"].shift()
pairs = df.dropna(subset=["prev_price"])
changed = pairs[pairs["price"] != pairs["prev_price"]]
drops = changed[changed["price"] < changed["prev_price"]]

print(f"Comparisons: {len(pairs)}")
print(f"Price changes: {len(changed)} ({len(changed) / len(pairs):.2%})")
print(f"  drops: {len(drops)}   increases: {len(changed) - len(drops)}")
print(f"Variants that changed at least once: "
      f"{changed['product_id'].nunique()} of {df['product_id'].nunique()}")