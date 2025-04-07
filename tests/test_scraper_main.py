"""Tests for the scraper main script."""

import pytest
from unittest.mock import patch
import pandas as pd


# Flask API Tests
@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    from main import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_scrape_route_success(client):
    """Test the /scrape API endpoint with successful response."""
    # Create mock DataFrame that would be returned by the scraper
    mock_df = pd.DataFrame(
        {
            "Character": ["Dan Heng"],
            "Path": ["The Hunt"],
            "Rarity": [4],
            "Element": ["Wind"],
        }
    )

    with patch("main.scrape_data", return_value=mock_df) as mock_scrape_data:
        with patch("main.load_to_sqlite") as mock_load_sqlite:
            response = client.get("/scrape")

            # Assert response is successful
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["status"] == "success"
            assert "data_shape" in json_data

            # Verify function calls
            mock_scrape_data.assert_called_once()
            mock_load_sqlite.assert_called_once_with(mock_df)


def test_scrape_route_error(client):
    """Test the /scrape API endpoint with error handling."""
    with patch("main.scrape_data", side_effect=Exception("API Scraping error")):
        response = client.get("/scrape")

        # Assert response indicates error
        assert response.status_code == 500
        json_data = response.get_json()
        assert json_data["status"] == "error"
        assert "An internal error has occurred." in json_data["message"]


def test_visualize_route_success(client):
    """Test the /visualize API endpoint with successful response."""
    with patch("main.visualize_data") as mock_visualize:
        response = client.get("/visualize")

        # Assert response is successful
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["status"] == "success"
        assert json_data["message"] == "Visualization creation complete"

        # Verify function calls
        mock_visualize.assert_called_once()


def test_visualize_route_error(client):
    """Test the /visualize API endpoint with error handling."""
    with patch("main.visualize_data", side_effect=Exception("Visualization error")):
        response = client.get("/visualize")

        # Assert response indicates error
        assert response.status_code == 500
        json_data = response.get_json()
        assert json_data["status"] == "error"
        assert "An internal error has occurred." in json_data["message"]


if __name__ == "__main__":
    pytest.main()
