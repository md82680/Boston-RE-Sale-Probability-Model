import pytest
from fastapi.testclient import TestClient
from api.endpoints import router
from fastapi import FastAPI

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def sample_property():
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
