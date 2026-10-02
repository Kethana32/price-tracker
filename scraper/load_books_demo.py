from datetime import datetime

import pandas as pd

from db import get_connection, init_db, get_or_create_product, add_price

DEMO_DB = "data/demo.db"

init_db(DEMO_DB)
df = pd.read_csv("data/books_clean.csv")
now = datetime.now().isoformat(timespec="seconds")

with get_connection(DEMO_DB) as conn:
    for _, row in df.iterrows():
        product_id = get_or_create_product(
            conn,
            site="books.toscrape.com",
            site_product_id=row["url"],   # the URL is unique per book
            name=row["title"],
            category="books",
            url=row["url"],
        )
        add_price(conn, product_id, now, row["price"],
                  rating=row["rating"], in_stock=int(row["in_stock"]))

    n_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    n_prices = conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
    print(f"products: {n_products}, price rows: {n_prices}")