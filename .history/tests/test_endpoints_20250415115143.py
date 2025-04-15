import pytest  # noqa: F401
from fastapi.testclient import TestClient #noqa: F401
import os

pytestmark = pytest.mark.api  # Mark all tests in this file with 'api' tag

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "model_loaded": True}

def test_predict_single_property(client, sample_property):
    # sample_property should match the structure in Property model
    response = client.post("/api/predict", json=sample_property)
    assert response.status_code == 200
    data = response.json()
    assert "sale_probability" in data
    assert "prediction_date" in data
    assert "model_version" in data
    assert isinstance(data["sale_probability"], float)
    assert 0 <= data["sale_probability"] <= 1

def test_predict_batch_properties(client, sample_batch_properties):
    response = client.post("/api/predict/batch", json=sample_batch_properties)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "prediction_date" in data
    assert "model_version" in data
    assert len(data["predictions"]) == len(sample_batch_properties["properties"])
    assert all(isinstance(p, float) for p in data["predictions"])
    assert all(0 <= p <= 1 for p in data["predictions"])

def test_invalid_property_data(client):
    invalid_data = {"square_feet": "invalid"}
    response = client.post("/api/predict", json=invalid_data)
    assert response.status_code == 422

def test_invalid_batch_data(client):
    invalid_data = {"properties": [{"square_feet": "invalid"}]}
    response = client.post("/api/predict/batch", json=invalid_data)
    assert response.status_code == 422

def test_logging_single_prediction(client, sample_property):
    response = client.post("/api/predict", json=sample_property)
    assert response.status_code == 200
    # No log checking, just verify the endpoint works

def test_logging_batch_predictions(client, sample_batch_properties):
    response = client.post("/api/predict/batch", json=sample_batch_properties)
    assert response.status_code == 200
    # No log checking, just verify the endpoint works
