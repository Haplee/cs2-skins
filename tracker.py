"""
Main tracking logic for the Steam Inventory Price Tracker.
"""

import steam_client
import price_fetcher
import database
import analysis
import config



def run_tracker(
    steam_id: str,
    use_test_data: bool = False,
    currency: str = "USD",
    filter_tradable: bool = False,
):

    """
    Runs the full tracking and analysis process.

    Args:
        steam_id: The 64-bit SteamID of the user.
        use_test_data: If True, uses a hardcoded test inventory.
        currency: The currency to fetch prices in.
        filter_tradable: If True, only fetches tradable items.

    Returns:
        A tuple containing (list_of_items, dict_of_prices, error_message).
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

        steam_id,
        use_test_data=use_test_data,
        filter_tradable=filter_tradable,

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

    current_prices = price_fetcher.fetch_all_prices(
        unique_inventory_items, currency=currency
    )

    error_message = None

    if current_prices is None:
        print("Could not fetch price data from external APIs.")
        error_message = (
            "Error: No se pudieron obtener los datos de precios desde la API de Skinport. "
            "El servicio puede estar temporalmente caído. Los precios históricos podrían seguir visibles."
        )
        current_prices = {}  # Use an empty dict to avoid further errors
    print("Price fetch complete.")

    # 4. Save the new price data to the database
    print("\n[Step 4/4] Saving new price data to the database...")
    database.save_prices(current_prices)

    # 5. Analyze and build results dictionary
    analysis_results = {}
    for item_name in unique_inventory_items:
        item_price_data = current_prices.get(item_name, {})

        current_price = item_price_data.get("skinport")  # Using skinport for analysis

        analysis_results[item_name] = {
            "current_price": current_price,
            "trend": analysis.analyze_item_trend(item_name, current_price)
            if current_price is not None
            else "Price not available.",

        }

    print("\n--- Tracking Complete ---")
    return unique_inventory_items, analysis_results, error_message


if __name__ == "__main__":
    # This allows running the tracker standalone for debugging
    print("Running tracker in standalone debug mode...")
    try:
        # We still use the config for standalone runs
        steam_id_from_config, use_test_data_from_config = config.get_config()

        run_tracker(steam_id_from_config, use_test_data_from_config)
    except (ValueError) as e:

        print(f"Could not run standalone tracker: {e}")
