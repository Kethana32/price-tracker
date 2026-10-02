import time
from datetime import datetime
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 50
DELAY_SECONDS = 1  # be polite: pause between requests

rows = []
scraped_at = datetime.now().isoformat(timespec="seconds")

for page in range(1, TOTAL_PAGES + 1):
    url = BASE_URL.format(page)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"  # fixes the "Â£" symbol problem

    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select("article.product_pod"):
        rows.append({
            "title": book.h3.a["title"],
            "price": book.select_one(".price_color").text,
            "rating": book.select_one("p.star-rating")["class"][1],
            "availability": book.select_one(".availability").text.strip(),
            "url": urljoin(url, book.h3.a["href"]),
            "scraped_at": scraped_at,
        })

    print(f"Page {page}/{TOTAL_PAGES} done ({len(rows)} books so far)")
    time.sleep(DELAY_SECONDS)

df = pd.DataFrame(rows)
df.to_csv("data/books_raw.csv", index=False, encoding="utf-8")
print(f"\nSaved {len(df)} books to data/books_raw.csv")