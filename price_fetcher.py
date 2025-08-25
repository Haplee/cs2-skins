"""
Handles fetching item prices from various sources.
"""

import requests

SKINPORT_API_URL = "https://api.skinport.com/v1/items"


def get_prices_from_skinport(item_names: list[str]) -> dict[str, float]:
    """
    Fetches prices for a list of items from the Skinport API.

    Args:
        item_names: A list of 'market_hash_name' to look up.

    Returns:
        A dictionary mapping item name to its suggested price.
        Returns an empty dictionary if an error occurs.
    """
    prices = {}
    print("Fetching prices from Skinport...")

    try:
        # Skinport API returns all items, so we fetch once and then filter.
        params = {"app_id": 730, "currency": "USD"}
        headers = {"Accept-Encoding": "br"}
        response = requests.get(
            SKINPORT_API_URL, params=params, headers=headers
        )

        response.raise_for_status()

        all_items = response.json()

        # Create a lookup table for faster access
        skinport_prices = {
            item["market_hash_name"]: item.get("suggested_price")
            for item in all_items
        }


        for item_name in item_names:
            if item_name in skinport_prices:
                price = skinport_prices[item_name]
                if price is not None:
                    prices[item_name] = float(price)

        return prices

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching from Skinport API: {e}")
        return {}
    except ValueError:
        print("Failed to decode JSON from Skinport API response.")
        return {}


def fetch_all_prices(item_names: list[str]) -> dict[str, dict[str, float]]:
    """
    Fetches prices from all available sources for the given items.

    Args:
        item_names: A list of 'market_hash_name' to look up.

    Returns:
        A dictionary where keys are item names and values are another
        dictionary mapping the source ('skinport', 'csfloat', etc.) to its price.
    """
    all_prices = {item: {} for item in item_names}

    # --- Skinport ---
    skinport_prices = get_prices_from_skinport(item_names)
    for item, price in skinport_prices.items():
        if item in all_prices:
            all_prices[item]["skinport"] = price


    # --- Other sources would be called here ---
    # e.g., csfloat_prices = get_prices_from_csfloat(item_names)

    return all_prices


if __name__ == "__main__":

    # Example Usage
    example_items = [
        "AK-47 | Redline (Field-Tested)",
        "AWP | Asiimov (Field-Tested)",
        "Glock-18 | Water Elemental (Minimal Wear)",
        "Non-existent Item 123",  # To test filtering

    ]

    print(f"Fetching prices for {len(example_items)} items...")
    retrieved_prices = fetch_all_prices(example_items)

    print("\n--- Retrieved Prices ---")
    for item, sources in retrieved_prices.items():
        if sources:
            print(f"- {item}:")
            for source, price in sources.items():
                print(f"  - {source}: ${price:.2f}")
        else:
            print(f"- {item}: Not found on any source.")
    print("------------------------")
