import pytest
from api.models import Property, BatchPropertyRequest, PredictionResponse, BatchPredictionResponse
from datetime import datetime
from pydantic import ValidationError

def test_valid_property_model():
    property_data = {
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
    
    property = Property(**property_data)
    assert property.years_owned == 15
    assert property.property_value == 750000

def test_property_model_validation():
    # Test invalid square feet
    with pytest.raises(ValidationError):
        Property(
            years_owned=15,
            property_value=750000,
            square_feet=100,  # Invalid - too small
            bedrooms=3,
            bathrooms=2.5,
            property_age=85,
            neighborhood="South End",
            distance_to_t=0.5,
            school_rating=7.5,
            property_tax=6500,
            has_liens=0,
            lien_amount=0,
            mortgage_rate=3.5,
            income_to_mortgage_ratio=3.8,
            market_inventory_months=2.5,
            avg_days_on_market=30
        )
    
    # Test invalid bedrooms (too many)
    with pytest.raises(ValidationError):
        Property(
            years_owned=15,
            property_value=750000,
            square_feet=1800,
            bedrooms=15,  # Invalid - too many
            bathrooms=2.5,
            property_age=85,
            neighborhood="South End",
            distance_to_t=0.5,
            school_rating=7.5,
            property_tax=6500,
            has_liens=0,
            lien_amount=0,
            mortgage_rate=3.5,
            income_to_mortgage_ratio=3.8,
            market_inventory_months=2.5,
            avg_days_on_market=30
        )

def test_batch_property_request():
    properties = [
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
    
    batch_request = BatchPropertyRequest(properties=properties)
    assert len(batch_request.properties) == 2
    assert batch_request.properties[0].square_feet == 1800
    assert batch_request.properties[1].square_feet == 1200

def test_prediction_response():
    response_data = {
        "sale_probability": 0.75,
        "prediction_date": datetime.now(),
        "model_version": "1.0.0"
    }
    
    response = PredictionResponse(**response_data)
    assert 0 <= response.sale_probability <= 1
    assert isinstance(response.prediction_date, datetime)
    assert response.model_version == "1.0.0"

def test_batch_prediction_response():
    response_data = {
        "predictions": [0.75, 0.6, 0.8],
        "prediction_date": datetime.now(),
        "model_version": "1.0.0"
    }
    
    response = BatchPredictionResponse(**response_data)
    assert len(response.predictions) == 3
    assert all(0 <= p <= 1 for p in response.predictions)
    assert isinstance(response.prediction_date, datetime)
    assert response.model_version == "1.0.0"

def test_empty_batch_request():
    with pytest.raises(ValidationError):
        BatchPropertyRequest(properties=[])

def test_invalid_prediction_values():
    with pytest.raises(ValidationError):
        PredictionResponse(
            sale_probability=1.5,  # Should be between 0 and 1
            prediction_date=datetime.now(),
            model_version="1.0.0"
        )

def test_model_version_format():
    # Test valid version format
    response = PredictionResponse(
        sale_probability=0.5,
        prediction_date=datetime.now(),
        model_version="1.0.0"
    )
    assert response.model_version.count(".") == 2

    # Test invalid version format
    with pytest.raises(ValidationError):
        PredictionResponse(
            sale_probability=0.5,
            prediction_date=datetime.now(),
            model_version="invalid_version"
        )
