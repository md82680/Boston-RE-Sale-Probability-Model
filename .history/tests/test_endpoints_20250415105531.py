import pytest  # noqa: F401


pytestmark = pytest.mark.api  # Mark all tests in this file with 'api' tag

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "model_loaded": True}

def test_predict_single_property(client, sample_property):
    response = client.post("/predict", json=sample_property)
    assert response.status_code == 200
    data = response.json()
    assert "sale_probability" in data
    assert "prediction_date" in data
    assert "model_version" in data
    assert isinstance(data["sale_probability"], float)
    assert 0 <= data["sale_probability"] <= 1

def test_predict_batch_properties(client, sample_batch_properties):
    response = client.post("/predict/batch", json=sample_batch_properties)
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
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422

def test_invalid_batch_data(client):
    invalid_data = {"properties": [{"square_feet": "invalid"}]}
    response = client.post("/predict/batch", json=invalid_data)
    assert response.status_code == 422

def test_logging_single_prediction(client, sample_property, tmp_path):
    # Configure logging to use temporary directory
    import logging
    log_file = tmp_path / "single_predictions.log"
    handler = logging.FileHandler(str(log_file))
    logging.getLogger().addHandler(handler)

    response = client.post("/predict", json=sample_property)
    assert response.status_code == 200
    
    # Check if log file was created and contains entry
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Prediction:" in log_content

def test_logging_batch_predictions(client, sample_batch_properties, tmp_path):
    # Similar to above but for batch predictions
    import logging
    log_file = tmp_path / "batch_predictions.log"
    handler = logging.FileHandler(str(log_file))
    logging.getLogger().addHandler(handler)

    response = client.post("/predict/batch", json=sample_batch_properties)
    assert response.status_code == 200
    
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Batch prediction" in log_content
