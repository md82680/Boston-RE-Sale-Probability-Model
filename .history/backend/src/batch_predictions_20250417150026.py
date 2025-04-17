"""Batch prediction utilities for property sale probability."""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import logging

from src.database import get_properties_from_database, update_property_predictions
from src.preprocessing import prepare_features_targets

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/batch_predictions.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_model(model_path='models/best_model.pkl'):
    """
    Load the trained model from disk.
    
    Parameters:
    -----------
    model_path : str
        Path to the model file
        
    Returns:
    --------
    object
        Loaded model
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def run_prediction_batch(threshold=0.7, export=True):
    """
    Run batch predictions on properties from the database.
    
    Parameters:
    -----------
    threshold : float
        Probability threshold for high-probability properties
    export : bool
        Whether to export high-probability properties to CSV
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with high-probability properties
    """
    logger.info("Starting batch prediction run")
    
    try:
        # Load model
        model = load_model()
        logger.info("Model loaded successfully")
        
        # Get property data
        properties = get_properties_from_database()
        logger.info(f"Retrieved {len(properties)} properties from database")
        
        if len(properties) == 0:
            logger.warning("No properties retrieved from database")
            return pd.DataFrame()
        
        # Prepare features (assuming schema matches training data)
        X = properties.drop(columns=['id', 'owner_name', 'owner_email', 'address', 
                                     'sale_probability', 'last_prediction_date'], errors='ignore')
        
        # Make predictions
        predictions = model.predict(X)
        properties['sale_probability'] = predictions
        logger.info("Predictions generated successfully")
        
        # Update database with new predictions
        update_property_predictions(properties['id'], predictions)
        logger.info("Database updated with new predictions")
        
        # Filter high-probability properties
        high_prob_properties = properties[properties['sale_probability'] > threshold]
        logger.info(f"Identified {len(high_prob_properties)} high-probability properties (>{threshold})")
        
        # Export for marketing if requested
        if export and len(high_prob_properties) > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"marketing/high_probability_targets_{timestamp}.csv"
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            
            high_prob_properties.to_csv(export_path, index=False)
            logger.info(f"Exported high-probability targets to {export_path}")
        
        return high_prob_properties
    
    except Exception as e:
        logger.error(f"Error in batch prediction process: {str(e)}", exc_info=True)
        raise
    
if __name__ == "__main__":
    # Run batch predictions
    high_prob_properties = run_prediction_batch()
    print(f"Found {len(high_prob_properties)} high-probability properties") 