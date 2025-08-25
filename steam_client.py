"""
Handles fetching a user's Steam inventory.
"""
import requests


def get_inventory(
    steam_id: str,
    use_test_data: bool = False,
    filter_tradable: bool = False,
    filter_item_type: str = None,
) -> list[str]:
    """
    Fetches a user's CS2 inventory and returns a list of market_hash_names.

    Args:
        steam_id: The 64-bit SteamID of the user.
        use_test_data: If True, returns a hardcoded list of items for testing.
        filter_tradable: If True, only returns tradable items.
        filter_item_type: If set, only returns items with this type tag.

    Returns:
        A list of 'market_hash_name' for all matching items in the inventory.
        Returns an empty list if the inventory is private or an error occurs.
    """
    if use_test_data:
        print("[Debug] Using hardcoded test inventory data.")
        # This test data is assumed to be tradable and of various types
        test_items = [
            "AK-47 | Redline (Field-Tested)",  # Rifle
            "AWP | Asiimov (Field-Tested)",  # Rifle
            "Glock-18 | Water Elemental (Minimal Wear)",  # Pistol
            "USP-S | Kill Confirmed (Field-Tested)",  # Pistol
            "★ Karambit | Doppler (Factory New)",  # Knife
            "Sticker | Natus Vincere (Holo) | Katowice 2014",  # Sticker
        ]
        if filter_item_type:
            return [
                item
                for item in test_items
                if filter_item_type.lower() in item.lower()
            ]
        return test_items

    # For CS2, the app_id is 730 and the context_id is 2.
    inventory_url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
    market_hash_names = []

    try:
        response = requests.get(inventory_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()

        if data.get("success") != 1 or "descriptions" not in data:
            print(
                f"Failed to fetch inventory. Response: {data.get('error', 'No descriptions found')}"
            )
            return []

        # Create a mapping from classid_instanceid to the description object
        descriptions = {
            f"{desc['classid']}_{desc.get('instanceid', '0')}": desc
            for desc in data["descriptions"]
        }

        for asset in data.get("assets", []):
            asset_key = f"{asset['classid']}_{asset['instanceid']}"
            description = descriptions.get(asset_key)

            if not description:
                continue

            # Apply tradable filter
            is_tradable = description.get("tradable", 0) == 1
            if filter_tradable and not is_tradable:
                continue

            # Apply item type filter
            if filter_item_type:
                item_tags = description.get("tags", [])
                # Find the 'Type' tag dictionary safely
                type_tag_dict = next(
                    (tag for tag in item_tags if tag.get("category") == "Type"),
                    None,
                )

                if not type_tag_dict:
                    continue  # Skip item if it has no Type tag and we are filtering

                # Safely get the name of the type, checking common keys
                type_name = type_tag_dict.get(
                    "name"
                ) or type_tag_dict.get("localized_tag_name")

                if (
                    not type_name
                    or filter_item_type.lower() not in type_name.lower()
                ):
                    continue

            market_hash_names.append(description["market_hash_name"])

        return market_hash_names

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
    example_steam_id = "76561197960435530"
    print(f"Fetching inventory for SteamID: {example_steam_id}")

    print("\n--- All Items ---")
    inventory_items = get_inventory(example_steam_id)
    if inventory_items:
        print(f"Found {len(inventory_items)} items.")
        for item in inventory_items[:5]:
            print(f"- {item}")
    else:
        print("Could not fetch inventory.")

    print("\n--- Tradable Items Only ---")
    tradable_items = get_inventory(example_steam_id, filter_tradable=True)
    if tradable_items:
        print(f"Found {len(tradable_items)} tradable items.")
        for item in tradable_items[:5]:
            print(f"- {item}")
    else:
        print("No tradable items found or could not fetch inventory.")

    print("\n--- 'Weapon' Type Only ---")
    weapon_items = get_inventory(example_steam_id, filter_item_type="Weapon")
    if weapon_items:
        print(f"Found {len(weapon_items)} weapon items.")
        for item in weapon_items[:5]:
            print(f"- {item}")
    else:
        print("No weapon items found or could not fetch inventory.")
