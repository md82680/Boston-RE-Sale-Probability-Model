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
        "property_type": "single_family",
        "square_feet": 2000,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 1990,
        "lot_size": 5000,
        "zip_code": "12345"
        # Add other required fields based on your Property model
    }

@pytest.fixture
def sample_batch_properties():
    return {
        "properties": [
            {
                "property_type": "single_family",
                "square_feet": 2000,
                "bedrooms": 3,
                "bathrooms": 2,
                "year_built": 1990,
                "lot_size": 5000,
                "zip_code": "12345"
            },
            {
                "property_type": "townhouse",
                "square_feet": 1500,
                "bedrooms": 2,
                "bathrooms": 1.5,
                "year_built": 2000,
                "lot_size": 3000,
                "zip_code": "12346"
            }
        ]
    }
