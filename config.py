"""
Handles reading configuration from config.ini file.
"""
import configparser
import os

CONFIG_FILE = "config.ini"
CONFIG_TEMPLATE = "config.ini.template"

def get_config() -> tuple[str, bool]:
    """
    Reads configuration from config.ini.

    Returns:
        A tuple containing (steam_id, use_test_inventory).

    Raises:
        FileNotFoundError: If config.ini does not exist.
        ValueError: If steam_id is not set correctly.
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(
            f"Configuration file '{CONFIG_FILE}' not found. "
            f"Please copy the template '{CONFIG_TEMPLATE}' to '{CONFIG_FILE}' "
            "and fill in your details."
        )

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    steam_id = config.get('Steam', 'steam_id', fallback='').strip()
    if not steam_id or steam_id == 'YOUR_STEAM_ID_HERE':
        raise ValueError(
            f"SteamID is not configured in '{CONFIG_FILE}'. "
            "Please open the file and set your 64-bit SteamID."
        )

    use_test_inventory = config.getboolean('Settings', 'use_test_inventory', fallback=False)

    return steam_id, use_test_inventory

if __name__ == '__main__':
    # Example usage:
    print("Attempting to read configuration...")
    try:
        steam_id, use_test = get_config()
        print("Config read successfully:")
        print(f"  SteamID: {steam_id}")
        print(f"  Use Test Inventory: {use_test}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("\nCreating a dummy config.ini for testing this module...")
        with open(CONFIG_FILE, "w") as f:
            f.write("[Steam]\n")
            f.write("steam_id = 76561197960435530\n")
            f.write("[Settings]\n")
            f.write("use_test_inventory = true\n")

        steam_id, use_test = get_config()
        print("\nConfig read successfully after creating dummy file:")
        print(f"  SteamID: {steam_id}")
        print(f"  Use Test Inventory: {use_test}")
        os.remove(CONFIG_FILE) # Clean up dummy file
        print("\nDummy config file removed.")
