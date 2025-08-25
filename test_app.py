import pytest
import os
import database

# Import the Flask app instance and the function to be tested
from app import app
from analysis import analyze_item_trend

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_analyze_item_trend():
    """
    Tests the trend analysis logic with a clean database.
    """
    # Setup: ensure the database and table exist
    database.create_tables()

    try:
        # Test case: Not enough data for a new item
        trend = analyze_item_trend("a_new_item_with_no_history", 100.0)
        assert "Not enough data" in trend
    finally:
        # Teardown: remove the database file to ensure test isolation
        if os.path.exists(database.DB_FILE):
            os.remove(database.DB_FILE)


def test_index_route(client):
    """
    Tests the main page ('/') to ensure it loads successfully.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Steam Inventory Price Tracker" in response.data


def test_track_route_test_mode(client, mocker):
    """
    Tests the /track route in test mode.
    We use 'mocker' to prevent the real tracker.run_tracker from running.
    """
    # Mock the main tracker function to avoid long-running processes

    mocker.patch(
        "tracker.run_tracker",
        return_value=(
            ["Item 1", "Item 2"],
            {
                "Item 1": {"current_price": 10.0, "trend": "Stable"},
                "Item 2": {"current_price": 25.0, "trend": "High"},
            },
        ),
    )

    response = client.post("/track", data={"use_test_data": "true"})
    assert response.status_code == 200
    assert (
        b"Resultados del An\xc3\xa1lisis" in response.data
    )  # "Resultados del Análisis"
    assert b"Item 1" in response.data
    assert b"Stable" in response.data
