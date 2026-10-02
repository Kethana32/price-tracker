import time
from datetime import datetime

import requests

from db import get_connection, init_db, get_or_create_product, add_price

SITE = "www.boat-lifestyle.com"
URL = f"https://{SITE}/products.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerStudentProject/0.1)"}
MAX_PAGES = 20      # safety limit
DELAY_SECONDS = 2   # be polite


def fetch_all_products():
    products = []
    for page in range(1, MAX_PAGES + 1):
        r = requests.get(URL, params={"limit": 250, "page": page},
                         headers=HEADERS, timeout=20)
        r.raise_for_status()
        batch = r.json()["products"]
        if not batch:          # empty page means we've reached the end
            break
        products.extend(batch)
        print(f"Page {page}: {len(batch)} products")
        time.sleep(DELAY_SECONDS)
    return products


def main():
    init_db()
    now = datetime.now().isoformat(timespec="seconds")
    products = fetch_all_products()

    rows_added = 0
    with get_connection() as conn:
        for p in products:
            for v in p["variants"]:
                name = p["title"]
                if len(p["variants"]) > 1:
                    name += f" - {v['title']}"

                product_id = get_or_create_product(
                    conn,
                    site=SITE,
                    site_product_id=str(v["id"]),
                    name=name,
                    category=p.get("product_type") or None,
                    url=f"https://{SITE}/products/{p['handle']}",
                )

                compare = v.get("compare_at_price")
                add_price(
                    conn,
                    product_id,
                    now,
                    price=float(v["price"]),
                    mrp=float(compare) if compare else None,
                    in_stock=int(v["available"]),
                )
                rows_added += 1

    print(f"\nSaved {rows_added} price rows from {len(products)} products")


if __name__ == "__main__":
    main()