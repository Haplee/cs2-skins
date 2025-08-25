"""
<<<<<<< HEAD
Handles reading configuration from environment variables.
"""
import os

def get_config() -> tuple[str, bool]:
    """
    Reads configuration from environment variables.
=======
Handles reading configuration from config.ini file.
"""
import configparser
import os

CONFIG_FILE = "config.ini"
CONFIG_TEMPLATE = "config.ini.template"

def get_config() -> tuple[str, bool]:
    """
    Reads configuration from config.ini.
>>>>>>> main

    Returns:
        A tuple containing (steam_id, use_test_inventory).

    Raises:
<<<<<<< HEAD
        ValueError: If the STEAM_ID environment variable is not set.
    """
    # In a Vercel environment, these are set in the project settings.
    # For local development, you can set them in your shell before running the app.
    # Example: export STEAM_ID="your_id_here"

    steam_id = os.environ.get('STEAM_ID')
    if not steam_id:
        raise ValueError(
            "The 'STEAM_ID' environment variable is not set. "
            "Please set it in your Vercel project settings or in your local shell."
        )

    # The value will be a string 'true' or 'false', so we check against 'true'.
    use_test_inventory_str = os.environ.get('USE_TEST_INVENTORY', 'false').lower()
    use_test_inventory = use_test_inventory_str == 'true'
=======
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
>>>>>>> main

    return steam_id, use_test_inventory

if __name__ == '__main__':
    # Example usage:
<<<<<<< HEAD
    print("Attempting to read configuration from environment variables...")
    try:
        # To test this module, we first need to set the environment variables.
        print("\nSetting dummy environment variables for testing...")
        os.environ['STEAM_ID'] = '76561197960435530'
        os.environ['USE_TEST_INVENTORY'] = 'true'

=======
    print("Attempting to read configuration...")
    try:
>>>>>>> main
        steam_id, use_test = get_config()
        print("Config read successfully:")
        print(f"  SteamID: {steam_id}")
        print(f"  Use Test Inventory: {use_test}")
<<<<<<< HEAD

        # Clean up the dummy variables
        del os.environ['STEAM_ID']
        del os.environ['USE_TEST_INVENTORY']
        print("\nDummy environment variables unset.")

    except ValueError as e:
        print(f"Error: {e}")
        # Test the error case
        print("\nTesting error case when STEAM_ID is not set...")
        if 'STEAM_ID' in os.environ:
            del os.environ['STEAM_ID']
        try:
            get_config()
        except ValueError as e_inner:
            print(f"Successfully caught expected error: {e_inner}")
=======
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
>>>>>>> main
