import sqlite3

conn = sqlite3.connect("data/prices.db")

print("Products per category:")
for cat, n in conn.execute(
    "SELECT COALESCE(category, '(none)'), COUNT(*) "
    "FROM products GROUP BY category ORDER BY 2 DESC"
):
    print(f"  {cat:25} {n}")

print("\nTotals:")
print("  products:", conn.execute("SELECT COUNT(*) FROM products").fetchone()[0])
print("  price rows:", conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0])