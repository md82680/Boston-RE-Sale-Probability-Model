import pytest
from api.models import Property, BatchPropertyRequest, PredictionResponse, BatchPredictionResponse
from datetime import datetime
from pydantic import ValidationError

def test_valid_property_model():
    property_data = {
        "square_feet": 2000,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 1990,
        "lot_size": 5000,
        "zip_code": "12345"
    }
    
    property = Property(**property_data)
    assert property.square_feet == 2000
    assert property.bedrooms == 3
    assert property.bathrooms == 2
    assert property.year_built == 1990
    assert property.lot_size == 5000
    assert property.zip_code == "12345"

def test_property_model_validation():
    # Test invalid square feet
    with pytest.raises(ValidationError):
        Property(
            square_feet=-100,  # Invalid negative value
            bedrooms=3,
            bathrooms=2,
            year_built=1990,
            lot_size=5000,
            zip_code="12345"
        )
    
    # Test invalid year
    with pytest.raises(ValidationError):
        Property(
            square_feet=2000,
            bedrooms=3,
            bathrooms=2,
            year_built=2025,  # Future year
            lot_size=5000,
            zip_code="12345"
        )

def test_batch_property_request():
    properties = [
        {
            "square_feet": 2000,
            "bedrooms": 3,
            "bathrooms": 2,
            "year_built": 1990,
            "lot_size": 5000,
            "zip_code": "12345"
        },
        {
            "square_feet": 1500,
            "bedrooms": 2,
            "bathrooms": 1,
            "year_built": 1985,
            "lot_size": 4000,
            "zip_code": "12346"
        }
    ]
    
    batch_request = BatchPropertyRequest(properties=properties)
    assert len(batch_request.properties) == 2
    assert batch_request.properties[0].square_feet == 2000
    assert batch_request.properties[1].square_feet == 1500

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
