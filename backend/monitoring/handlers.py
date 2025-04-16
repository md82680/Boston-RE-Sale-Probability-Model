from datetime import datetime
from .metrics import (
    prediction_requests,
    model_accuracy,
    prediction_latency,
    prediction_errors
)

class MetricsHandler:
    @staticmethod
    def record_prediction_request():
        """Increment the prediction request counter"""
        prediction_requests.inc()

    @staticmethod
    def record_prediction_accuracy(actual, predicted):
        """Record the accuracy of a prediction"""
        accuracy = 1 - abs(actual - predicted)
        model_accuracy.observe(accuracy)

    @staticmethod
    def record_prediction_time(start_time):
        """Record the time taken for a prediction"""
        duration = datetime.now().timestamp() - start_time
        prediction_latency.observe(duration)

    @staticmethod
    def record_prediction_error(error_type):
        """Record a prediction error"""
        prediction_errors.labels(type=error_type).inc()

# Usage in your API endpoints:
"""
from monitoring.handlers import MetricsHandler

@app.post("/predict")
async def predict():
    start_time = datetime.now().timestamp()
    MetricsHandler.record_prediction_request()
    
    try:
        # Your prediction logic here
        MetricsHandler.record_prediction_time(start_time)
        return result
    except Exception as e:
        MetricsHandler.record_prediction_error(type(e).__name__)
        raise
"""
