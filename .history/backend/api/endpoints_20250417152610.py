"""API endpoints for the property sale prediction service."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
import pandas as pd
import pickle
import os
import sys
import logging
from datetime import datetime
from monitoring.handlers import MetricsHandler

# Import Pydantic models
from .models import Property, BatchPropertyRequest, PredictionResponse, BatchPredictionResponse

# Add project root to path to allow imports from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load the model
model_path = os.path.join("models", "best_model.pkl")

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    logger.info(f"Model loaded successfully from {model_path}")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

# Create router
router = APIRouter()

@router.get("/health")
async def health_check():
    """Check if the API is healthy and model is loaded."""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@router.post("/predict", response_model=PredictionResponse)
async def predict_sale_probability(property_data: Property, background_tasks: BackgroundTasks):
    """
    Predict sale probability for a single property.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    start_time = datetime.now().timestamp()
    MetricsHandler.record_prediction_request()
    
    try:
        # Convert to DataFrame
        df = pd.DataFrame([property_data.model_dump()])
        
        # Preprocess data to match model expectations
        # Option 1: Remove neighborhood if model wasn't trained with it
        if 'neighborhood' in df.columns:
            df = df.drop(columns=['neighborhood'])
        
        # Option 2: Or encode neighborhood if model expects it encoded
        # df = encode_neighborhood(df)  # You'd need to implement this function
        
        # Make prediction
        prediction = float(model.predict(df)[0])
        
        # Log this prediction (non-blocking)
        background_tasks.add_task(
            log_prediction, 
            property_data.model_dump(), 
            prediction
        )
        
        # Record metrics
        MetricsHandler.record_prediction_time(start_time)
        if hasattr(property_data, 'actual_sale'):
            MetricsHandler.record_prediction_accuracy(
                property_data.actual_sale, 
                prediction
            )
        
        return {
            "sale_probability": prediction,
            "prediction_date": datetime.now(),
            "model_version": "1.0.0"
        }
    
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        MetricsHandler.record_prediction_error(type(e).__name__)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(batch_request: BatchPropertyRequest, background_tasks: BackgroundTasks):
    """
    Predict sale probabilities for multiple properties.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert list of properties to DataFrame
        properties_dicts = [prop.model_dump() for prop in batch_request.properties]
        df = pd.DataFrame(properties_dicts)
        
        # Preprocess data to match model expectations
        # Option 1: Remove neighborhood if model wasn't trained with it
        if 'neighborhood' in df.columns:
            df = df.drop(columns=['neighborhood'])
        
        # Option 2: Or encode neighborhood if model expects it encoded
        # df = encode_neighborhood(df)  # You'd need to implement this function
        
        # Make predictions
        predictions = model.predict(df).tolist()
        
        # Log these predictions (non-blocking)
        background_tasks.add_task(
            log_batch_predictions, 
            properties_dicts, 
            predictions
        )
        
        # Record metrics
        start_time = datetime.now().timestamp()
        MetricsHandler.record_prediction_request()
        MetricsHandler.record_prediction_time(start_time)
        
        return {
            "predictions": predictions,
            "prediction_date": datetime.now(),
            "model_version": "1.0.0"
        }
    
    except Exception as e:
        logger.error(f"Error making batch predictions: {str(e)}")
        MetricsHandler.record_prediction_error(type(e).__name__)
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

# Helper functions
def log_prediction(property_data, prediction):
    """Log a prediction to file system."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Prediction: {prediction:.4f} - Property: {property_data}\n"
        
        # Use configurable log directory
        log_dir = getattr(log_prediction, "log_dir", "logs/predictions")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "single_predictions.log"), "a") as f:
            f.write(log_entry)
    except Exception as e:
        logger.error(f"Error logging prediction: {str(e)}")

# Set default log directory
log_prediction.log_dir = "logs/predictions"

def log_batch_predictions(properties_data, predictions):
    """Log batch predictions to file system."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Batch prediction - Count: {len(predictions)}\n"
        
        os.makedirs("logs/predictions", exist_ok=True)
        with open("logs/predictions/batch_predictions.log", "a") as f:
            f.write(log_entry)
    except Exception as e:
        logger.error(f"Error logging batch predictions: {str(e)}") 