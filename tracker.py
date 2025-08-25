"""
Main tracking logic for the Steam Inventory Price Tracker.

This script orchestrates the process of:
1. Fetching a user's Steam inventory.
2. Fetching the current market prices for those items from various sources.
3. Storing the price data in a local database.
4. Returning the results for presentation.

NOTE: This implementation fetches prices from Skinport.com only. It is designed
to be extensible for other sources. It also only works for public Steam inventories.
"""

import steam_client
import price_fetcher
import database
import analysis
import config


def run_tracker(steam_id: str, use_test_data: bool = False):
    """
    Runs the full tracking and analysis process.

    Args:
        steam_id: The 64-bit SteamID of the user.
        use_test_data: If True, uses a hardcoded test inventory.

    Returns:
        A tuple containing (list_of_items, dict_of_prices, analysis_results).
        Returns (None, None, None) if an error occurs.
    """
    print("--- Running Tracker ---")
    if use_test_data:
        print("!!! RUNNING IN TEST MODE - Using a hardcoded inventory. !!!")

    # 1. Initialize the database
    print("\n[Step 1/4] Initializing database...")
    database.create_tables()

    # 2. Fetch Steam Inventory
    print(f"\n[Step 2/4] Fetching Steam Inventory for SteamID: {steam_id}...")
    inventory_items = steam_client.get_inventory(
        steam_id, use_test_data=use_test_data
    )
    if not inventory_items:
        print(
            "Could not fetch inventory. It might be private or the SteamID is invalid."
        )
        return None, None, None

    unique_inventory_items = sorted(list(set(inventory_items)))
    print(
        f"Found {len(inventory_items)} total items ({len(unique_inventory_items)} unique)."
    )

    # 3. Fetch current prices for these items
    print(
        f"\n[Step 3/4] Fetching current market prices for {len(unique_inventory_items)} unique items..."
    )
    current_prices = price_fetcher.fetch_all_prices(unique_inventory_items)
    if not current_prices:
        print("Could not fetch any price data.")
        # We can still proceed to analysis with historical data if any
    print("Price fetch complete.")

    # 4. Save the new price data to the database
    print("\n[Step 4/4] Saving new price data to the database...")
    database.save_prices(current_prices)

    # 5. Analyze and build results dictionary
    analysis_results = {}
    for item_name in unique_inventory_items:
        item_price_data = current_prices.get(item_name, {})
        current_price = item_price_data.get(
            "skinport"
        )  # Using skinport for analysis

        analysis_results[item_name] = {
            "current_price": current_price,
            "trend": (
                analysis.analyze_item_trend(item_name, current_price)
                if current_price is not None
                else "Price not available."
            ),
        }

    print("\n--- Tracking Complete ---")
    return unique_inventory_items, analysis_results


if __name__ == "__main__":
    # This allows running the tracker standalone for debugging
    print("Running tracker in standalone debug mode...")
    try:
        # We still use the config for standalone runs
        steam_id_from_config, use_test_data_from_config = config.get_config()
        items, results = run_tracker(
            steam_id_from_config, use_test_data_from_config
        )

        if items:
            print("\n--- STANDALONE REPORT ---")
            for item in items:
                result = results.get(item, {})
                price = result.get("current_price")
                trend = result.get("trend")
                price_str = f"${price:.2f}" if price is not None else "N/A"
                print(f"\n- {item}")
                print(f"  > Current Price: {price_str}")
                print(f"  > Trend Analysis: {trend}")
            print("\n--- Report Complete ---")

    except (FileNotFoundError, ValueError) as e:
        print(f"Could not run standalone tracker: {e}")
