"""
Handles reading configuration from environment variables.
"""

import os


def get_config() -> tuple[str, bool]:
    """
    Reads configuration from environment variables.

    Returns:
        A tuple containing (steam_id, use_test_inventory).

    Raises:
        ValueError: If the STEAM_ID environment variable is not set.
    """
    # In a Vercel environment, these are set in the project settings.
    # For local development, you can set them in your shell before running the app.
    # Example: export STEAM_ID="your_id_here"

    steam_id = os.environ.get("STEAM_ID")
    if not steam_id:
        raise ValueError(
            "The 'STEAM_ID' environment variable is not set. "
            "Please set it in your Vercel project settings or in your local shell."
        )

    # The value will be a string 'true' or 'false', so we check against 'true'.
    use_test_inventory_str = os.environ.get(
        "USE_TEST_INVENTORY", "false"
    ).lower()
    use_test_inventory = use_test_inventory_str == "true"

    return steam_id, use_test_inventory


if __name__ == "__main__":
    # Example usage:
    print("Attempting to read configuration from environment variables...")
    try:
        # To test this module, we first need to set the environment variables.
        print("\nSetting dummy environment variables for testing...")
        os.environ["STEAM_ID"] = "76561197960435530"
        os.environ["USE_TEST_INVENTORY"] = "true"
        steam_id, use_test = get_config()
        print("Config read successfully:")
        print(f"  SteamID: {steam_id}")
        print(f"  Use Test Inventory: {use_test}")

        # Clean up the dummy variables
        del os.environ["STEAM_ID"]
        del os.environ["USE_TEST_INVENTORY"]
        print("\nDummy environment variables unset.")

    except ValueError as e:
        print(f"Error: {e}")
        # Test the error case
        print("\nTesting error case when STEAM_ID is not set...")
        if "STEAM_ID" in os.environ:
            del os.environ["STEAM_ID"]
        try:
            get_config()
        except ValueError as e_inner:
            print(f"Successfully caught expected error: {e_inner}")
