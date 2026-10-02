import time
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerStudentProject/0.1)"}

# Edit this list: add or remove domains (no https://)
SITES = [
    "delhiwatchcompany.com",
    "jaipurwatchcompany.com",
    "ajwa.in",
    "cypherwatches.com",
    "sylvi.in",
    "horpawatch.com",
]

for domain in SITES:
    url = f"https://{domain}/products.json?limit=250"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        products = data["products"]
    except Exception as e:
        print(f"{domain:28} -> NOT USABLE ({type(e).__name__})")
        time.sleep(2)
        continue

    with_compare = 0
    for p in products:
        for v in p["variants"]:
            cap = v.get("compare_at_price")
            if cap and float(cap) > float(v["price"]):
                with_compare += 1
                break
    print(f"{domain:28} -> OK, {len(products)} products, "
          f"{with_compare} with a discount shown")
    time.sleep(2)  # be polite