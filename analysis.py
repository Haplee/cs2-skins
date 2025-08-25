"""
Performs analysis on the price history data.
"""

from datetime import datetime, timedelta, timezone
import database


def get_price_history(item_name: str, days: int = 30) -> list[tuple]:
    """
    Retrieves the price history for a specific item over a number of days.

    Args:
        item_name: The 'market_hash_name' of the item.
        days: The number of past days to retrieve data for.

    Returns:
        A list of tuples, where each tuple is (timestamp, price).
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()

    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    query = (
        "SELECT timestamp, price FROM price_history "
        "WHERE item_name = ? AND timestamp >= ? ORDER BY timestamp ASC"
    )
    cursor.execute(query, (item_name, start_date))

    history = cursor.fetchall()
    conn.close()
    return [(row["timestamp"], row["price"]) for row in history]


def analyze_item_trend(item_name: str, current_price: float) -> str:
    """
    Analyzes the price trend for a single item and provides a recommendation.

    Args:
        item_name: The 'market_hash_name' of the item.
        current_price: The current price of the item.

    Returns:
        A string summarizing the trend (e.g., "stable", "overpriced", "good deal").
    """
    history = get_price_history(item_name, days=30)

    if len(history) < 2:
        return "Not enough data to analyze trend."

    prices = [row[1] for row in history]
    avg_price_30_days = sum(prices) / len(prices)

    # Analyze last 7 days
    last_7_days_prices = []
    now_utc = datetime.now(timezone.utc)
    for ts_from_db, price in history:
        ts_obj = datetime.fromisoformat(ts_from_db)
        # Ensure the datetime object is timezone-aware before comparison
        if ts_obj.tzinfo is None:
            ts_obj = ts_obj.replace(tzinfo=timezone.utc)

        if (now_utc - ts_obj).days <= 7:
            last_7_days_prices.append(price)

    if not last_7_days_prices:

        avg_price_7_days = avg_price_30_days  # Fallback

    else:
        avg_price_7_days = sum(last_7_days_prices) / len(last_7_days_prices)

    # Simple trend logic
    price_str = f"${current_price:.2f}"
    avg_price_str = f"${avg_price_7_days:.2f}"
    if current_price > avg_price_7_days * 1.1:
        trend = (
            f"High: Current price ({price_str}) is >10% "
            f"above 7-day average ({avg_price_str})."
        )
    elif current_price < avg_price_7_days * 0.9:
        trend = (
            f"Low: Current price ({price_str}) is >10% "
            f"below 7-day average ({avg_price_str})."
        )
    else:
        trend = (
            f"Stable: Current price ({price_str}) is within 10% "
            f"of 7-day average ({avg_price_str})."
        )

    return trend


if __name__ == "__main__":
    # Example usage (requires data in the database)
    print("Running analysis example...")

    # First, ensure there's data to analyze
    database.create_tables()
    # Add some dummy historical data
    conn = database.get_db_connection()
    cursor = conn.cursor()

    item_to_test = "AK-47 | Redline (Field-Tested)"

    # Clear old test data
    cursor.execute(
        "DELETE FROM price_history WHERE item_name = ?", (item_to_test,)
    )

    dummy_data = [
        (
            item_to_test,
            "skinport",
            50.0,
            datetime.now(timezone.utc) - timedelta(days=10),
        ),
        (
            item_to_test,
            "skinport",
            52.5,
            datetime.now(timezone.utc) - timedelta(days=5),
        ),
        (
            item_to_test,
            "skinport",
            51.0,
            datetime.now(timezone.utc) - timedelta(days=2),
        ),
    ]
    query = (
        "INSERT INTO price_history (item_name, source, price, timestamp) "
        "VALUES (?, ?, ?, ?)"
    )
    cursor.executemany(query, dummy_data)
    conn.commit()
    conn.close()

    print(f"Analyzing trend for: {item_to_test}")

    # Simulate a "current" price check
    current_market_price = 45.0
    analysis_result = analyze_item_trend(item_to_test, current_market_price)

    print(
        f" -> Current Price: ${current_market_price:.2f} -> {analysis_result}"
    )

    current_market_price = 55.0
    analysis_result = analyze_item_trend(item_to_test, current_market_price)
    print(
        f" -> Current Price: ${current_market_price:.2f} -> {analysis_result}"
    )

    current_market_price = 51.5
    analysis_result = analyze_item_trend(item_to_test, current_market_price)
    print(
        f" -> Current Price: ${current_market_price:.2f} -> {analysis_result}"
    )

