import sqlite3
import pandas as pd

conn = sqlite3.connect("data/prices.db")

# read all prices, skipping boAt's test listings
df = pd.read_sql(
    "SELECT p.id AS product_id, p.name, pr.price, pr.mrp "
    "FROM prices pr JOIN products p ON p.id = pr.product_id "
    "WHERE LOWER(p.name) NOT LIKE '%test%' "
    "ORDER BY p.id, pr.scraped_at",
    conn,
)

g = df.groupby("product_id")
latest = g.tail(1).set_index("product_id")   # newest row per product
stats = g["price"].agg(median_price="median", min_price="min", n_obs="count")
out = latest.join(stats)

out["advertised_pct"] = (out["mrp"] - out["price"]) / out["mrp"] * 100
out["real_pct"] = (out["median_price"] - out["price"]) / out["median_price"] * 100
out["gap"] = out["advertised_pct"] - out["real_pct"]

# colors of one product repeat the same row, so keep one
out["short_name"] = out["name"].str.split(" - ").str[0].str[:35]
out = out.dropna(subset=["advertised_pct"])
out = out.drop_duplicates(subset=["short_name", "price", "mrp"])

cols = ["short_name", "price", "mrp", "median_price", "min_price",
        "advertised_pct", "real_pct", "gap", "n_obs"]
print(out.sort_values("gap", ascending=False)[cols].head(15).round(1).to_string(index=False))
print(f"\nProducts scored: {len(out)}   Max observations per product: {out['n_obs'].max()}")