"""
Handles fetching a user's Steam inventory.
"""

import requests

# For CS2, the app_id is 730 and the context_id is 2.
INVENTORY_URL = "https://steamcommunity.com/inventory/{steam_id}/730/2"


def get_inventory(steam_id: str, use_test_data: bool = False) -> list[str]:
    """
    Fetches a user's CS2 inventory and returns a list of market_hash_names.

    Args:
        steam_id: The 64-bit SteamID of the user.
        use_test_data: If True, returns a hardcoded list of items for testing.

    Returns:
        A list of 'market_hash_name' for all items in the inventory.
        Returns an empty list if the inventory is private or an error occurs.
    """
    if use_test_data:
        print("[Debug] Using hardcoded test inventory data.")
        return [
            "AK-47 | Redline (Field-Tested)",
            "AWP | Asiimov (Field-Tested)",
            "Glock-18 | Water Elemental (Minimal Wear)",
            "USP-S | Kill Confirmed (Field-Tested)",
            "★ Karambit | Doppler (Factory New)",  # A high-value item
        ]

    url = INVENTORY_URL.format(steam_id=steam_id)
    market_hash_names = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()

        if data.get("success") == 1 and "descriptions" in data:
            # Create a mapping from classid_instanceid to market_hash_name
            descriptions = {
                f"{desc['classid']}_{desc.get('instanceid', '0')}": desc[
                    "market_hash_name"
                ]
                for desc in data["descriptions"]
            }

            for asset in data.get("assets", []):
                asset_key = f"{asset['classid']}_{asset['instanceid']}"
                if asset_key in descriptions:
                    market_hash_names.append(descriptions[asset_key])

            return market_hash_names
        else:
            print(
                f"Failed to fetch inventory. Response: {data.get('error', 'No descriptions found')}"
            )
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the inventory: {e}")
        return []
    except ValueError:  # Catches JSON decoding errors
        print(
            "Failed to decode JSON from response. The user's inventory might be private."
        )
        return []


if __name__ == "__main__":
    # Example usage: Replace with a public inventory's SteamID for testing.
    # Note: This will only work if the inventory is public.
    example_steam_id = (
        "76561197960435530"  # A known public inventory for testing
    )
    print(f"Fetching inventory for SteamID: {example_steam_id}")
    inventory_items = get_inventory(example_steam_id)
    if inventory_items:
        print(f"Found {len(inventory_items)} items.")
        # Print the first 5 items for brevity
        for item in inventory_items[:5]:
            print(f"- {item}")
    else:
        print(
            "Could not fetch inventory. It might be private or the SteamID is invalid."
        )
