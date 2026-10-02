import sys
import requests
from urllib.robotparser import RobotFileParser

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerStudentProject/0.1)"}

site = sys.argv[1].rstrip("/")          # e.g. https://example.com
paths = ["/products.json", "/collections/all", "/"]

try:
    r = requests.get(site + "/robots.txt", headers=HEADERS, timeout=10)
except requests.exceptions.RequestException as e:
    print("Could not reach the site:", e)
    sys.exit(1)

print("robots.txt status:", r.status_code)

rp = RobotFileParser()
if r.status_code == 200:
    rp.parse(r.text.splitlines())
    rp.modified()
elif r.status_code in (401, 403):
    rp.disallow_all = True      # site refuses bots: treat everything as off-limits
else:
    rp.allow_all = True         # no robots.txt (e.g. 404) means no stated restrictions

for path in paths:
    allowed = rp.can_fetch("*", site + path)
    print(f"{path:20} -> {'ALLOWED' if allowed else 'DISALLOWED'}")

print("\nCrawl-delay:", rp.crawl_delay("*"))