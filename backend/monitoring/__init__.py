from .metrics import (
    prediction_requests,
    model_accuracy,
    prediction_latency,
    prediction_errors
)

from .performance import (
    evaluate_marketing_performance,
    trigger_model_retraining,
    generate_performance_charts
)

# Export what should be available when importing the package
__all__ = [
    'prediction_requests',
    'model_accuracy',
    'prediction_latency',
    'prediction_errors',
    'evaluate_marketing_performance',
    'trigger_model_retraining',
    'generate_performance_charts'
]
