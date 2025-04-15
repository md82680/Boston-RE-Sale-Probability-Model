import pytest
import os
from fastapi.testclient import TestClient
from api.main import app

# Create required directories
os.makedirs("logs", exist_ok=True)
os.makedirs("logs/predictions", exist_ok=True)

@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_property():
    """Sample property data matching the Property model requirements."""
    return {
        "years_owned": 15,
        "property_value": 750000,
        "square_feet": 1800,
        "bedrooms": 3,
        "bathrooms": 2.5,
        "property_age": 85,
        "neighborhood": "South End",
        "distance_to_t": 0.5,
        "school_rating": 7.5,
        "property_tax": 6500,
        "has_liens": 0,
        "lien_amount": 0,
        "mortgage_rate": 3.5,
        "income_to_mortgage_ratio": 3.8,
        "market_inventory_months": 2.5,
        "avg_days_on_market": 30
    }

@pytest.fixture
def sample_batch_properties():
    """Sample batch property data for testing."""
    return {
        "properties": [
            {
                "years_owned": 15,
                "property_value": 750000,
                "square_feet": 1800,
                "bedrooms": 3,
                "bathrooms": 2.5,
                "property_age": 85,
                "neighborhood": "South End",
                "distance_to_t": 0.5,
                "school_rating": 7.5,
                "property_tax": 6500,
                "has_liens": 0,
                "lien_amount": 0,
                "mortgage_rate": 3.5,
                "income_to_mortgage_ratio": 3.8,
                "market_inventory_months": 2.5,
                "avg_days_on_market": 30
            },
            {
                "years_owned": 5,
                "property_value": 550000,
                "square_feet": 1200,
                "bedrooms": 2,
                "bathrooms": 1.0,
                "property_age": 60,
                "neighborhood": "Allston",
                "distance_to_t": 0.3,
                "school_rating": 6.5,
                "property_tax": 4800,
                "has_liens": 1,
                "lien_amount": 50000,
                "mortgage_rate": 4.2,
                "income_to_mortgage_ratio": 2.5,
                "market_inventory_months": 3.5,
                "avg_days_on_market": 45
            }
        ]
    }
