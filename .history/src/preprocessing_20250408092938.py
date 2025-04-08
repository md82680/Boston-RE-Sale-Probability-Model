import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_data(filepath='../data/boston_real_estate_sale_probability.csv'):
    """
    Load and perform initial data cleaning
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
        
    Returns:
    --------
    pandas.DataFrame
        Cleaned dataframe
    """
    # Load data
    df = pd.read_csv(filepath)
    
    # Convert date strings to datetime objects
    df['last_transaction_date'] = pd.to_datetime(df['last_transaction_date'])
    
    # Handle missing values if any
    df = df.dropna()
    
    return df

def prepare_features_targets(df, target='sale_probability'):
    """
    Split dataframe into features (X) and target (y)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    target : str
        Target variable name
        
    Returns:
    --------
    tuple
        (X, y) where X is features dataframe and y is target series
    """
    # Extract target
    y = df[target]
    
    # Extract features, drop target and any non-predictive columns
    X = df.drop(columns=[target, 'last_transaction_date'])
    
    return X, y

def create_preprocessing_pipeline():
    """
    Create a preprocessing pipeline with categorical encoding and scaling
    
    Returns:
    --------
    sklearn.pipeline.Pipeline
        Preprocessing pipeline
    """
    # Identify categorical columns
    categorical_cols = ['neighborhood']
    
    # Identify numerical columns (excluding the categorical ones)
    numerical_cols = ['years_owned', 'property_value', 'square_feet', 'bedrooms', 
                      'bathrooms', 'property_age', 'distance_to_t', 'school_rating',
                      'property_tax', 'has_liens', 'lien_amount', 'mortgage_rate',
                      'income_to_mortgage_ratio', 'market_inventory_months', 'avg_days_on_market']
    
    # Define preprocessing for numerical columns
    numerical_transformer = StandardScaler()
    
    # Define preprocessing for categorical columns
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Create preprocessing pipeline
    preprocessing_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor)
    ])
    
    return preprocessing_pipeline

if __name__ == "__main__":
    # Test the preprocessing functions
    df = load_data()
    X, y = prepare_features_targets(df)
    
    print(f"Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
