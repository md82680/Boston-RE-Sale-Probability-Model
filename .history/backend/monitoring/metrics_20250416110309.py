from prometheus_client import Counter, Histogram

# Prediction metrics
prediction_requests = Counter(
    'prediction_requests_total',
    'Total number of prediction requests'
)

model_accuracy = Histogram(
    'model_accuracy',
    'Prediction accuracy distribution'
)

# Performance metrics
prediction_latency = Histogram(
    'prediction_latency_seconds',
    'Time taken for predictions'
)

# Error metrics
prediction_errors = Counter(
    'prediction_errors_total',
    'Total number of prediction errors'
)
