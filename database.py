"""
Handles all database operations for the price tracker.
Uses SQLite for simple, file-based storage.
"""

import sqlite3
from datetime import datetime, timezone
import os

# In a serverless environment like Vercel, only the /tmp directory is writable.
DB_FILE = os.path.join("/tmp", "price_history.db")



def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Creates the necessary database tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table to store price history

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            source TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME NOT NULL
        )
    """
    )

    # Create an index for faster lookups by item_name
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_item_name ON price_history (item_name)"
    )

    conn.commit()
    conn.close()
    print("Database tables checked/created successfully.")


def save_prices(price_data: dict[str, dict[str, float]]):
    """
    Saves a batch of price data to the database.

    Args:
        price_data: A dictionary structured like:
                    {'item_name': {'source': price, ...}, ...}
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    timestamp = datetime.now(timezone.utc)

    records_to_insert = []
    for item_name, sources in price_data.items():
        for source, price in sources.items():
            records_to_insert.append((item_name, source, price, timestamp))

    if not records_to_insert:
        print("No price data to save.")
        return

    cursor.executemany(
        "INSERT INTO price_history (item_name, source, price, timestamp) VALUES (?, ?, ?, ?)",
        records_to_insert,
    )

    conn.commit()
    conn.close()

    print(
        f"Successfully saved {len(records_to_insert)} price records to the database."
    )


if __name__ == "__main__":
    # Example usage:
    print("Initializing database...")
    create_tables()

    # Example data similar to what price_fetcher.py would provide
    example_price_data = {

        "AK-47 | Redline (Field-Tested)": {"skinport": 49.19},
        "AWP | Asiimov (Field-Tested)": {"skinport": 171.13},
    }

    print("\nSaving example data...")
    save_prices(example_price_data)

    # Verify data was saved
    print("\nVerifying saved data...")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM price_history ORDER BY timestamp DESC LIMIT 2"
    )
    rows = cursor.fetchall()
    for row in rows:
        print(dict(row))
    conn.close()
