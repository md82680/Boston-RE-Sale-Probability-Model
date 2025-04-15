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

def test_logging_single_prediction(client, sample_property, tmp_path):
    # Directly modify the endpoint's logging path for testing
    import api.endpoints as endpoints
    
    # Store original path to restore later
    original_log_dir = "logs/predictions"
    
    # Point log output to our test directory
    os.makedirs(str(tmp_path), exist_ok=True)
    endpoints.log_prediction.log_dir = str(tmp_path)
    
    try:
        response = client.post("/api/predict", json=sample_property)
        assert response.status_code == 200
        
        # Force execution of background tasks
        task_data = response.headers.get("X-Fastapi-Background-Tasks-Count")
        
        # Wait a moment for logging to complete
        import time
        time.sleep(0.1)
        
        # Check for log file - look for single_predictions.log in tmp_path
        log_file = tmp_path / "single_predictions.log"
        assert log_file.exists(), f"Log file not found at {log_file}"
        log_content = log_file.read_text()
        assert "Prediction:" in log_content
    finally:
        # Restore original logging path
        endpoints.log_prediction.log_dir = original_log_dir

def test_logging_batch_predictions(client, sample_batch_properties, tmp_path):
    # Similar to above but for batch predictions
    import logging
    log_file = tmp_path / "batch_predictions.log"
    handler = logging.FileHandler(str(log_file))
    logging.getLogger().addHandler(handler)

    response = client.post("/api/predict/batch", json=sample_batch_properties)
    assert response.status_code == 200
    
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Batch prediction" in log_content
