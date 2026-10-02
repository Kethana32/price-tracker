import sqlite3
from pathlib import Path

DB_PATH = Path("data/prices.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    site            TEXT NOT NULL,
    site_product_id TEXT NOT NULL,
    name            TEXT NOT NULL,
    category        TEXT,
    url             TEXT,
    UNIQUE (site, site_product_id)
);

CREATE TABLE IF NOT EXISTS prices (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   INTEGER NOT NULL,
    scraped_at   TEXT NOT NULL,
    price        REAL NOT NULL,
    mrp          REAL,
    rating       REAL,
    review_count INTEGER,
    in_stock     INTEGER,
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE INDEX IF NOT EXISTS idx_prices_product_time
    ON prices (product_id, scraped_at);
"""


def get_connection(db_path=DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA)


def get_or_create_product(conn, site, site_product_id, name, category=None, url=None):
    """Return the product's id, inserting it only if it doesn't exist yet."""
    conn.execute(
        """INSERT OR IGNORE INTO products (site, site_product_id, name, category, url)
           VALUES (?, ?, ?, ?, ?)""",
        (site, site_product_id, name, category, url),
    )
    row = conn.execute(
        "SELECT id FROM products WHERE site = ? AND site_product_id = ?",
        (site, site_product_id),
    ).fetchone()
    return row[0]


def add_price(conn, product_id, scraped_at, price, mrp=None,
              rating=None, review_count=None, in_stock=None):
    """Always INSERT a new row. Never update old prices."""
    conn.execute(
        """INSERT INTO prices
           (product_id, scraped_at, price, mrp, rating, review_count, in_stock)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (product_id, scraped_at, price, mrp, rating, review_count, in_stock),
    )