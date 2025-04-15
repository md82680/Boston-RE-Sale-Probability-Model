"""Database connection utilities for the property database."""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_connection():
    """
    Create a connection to the property database.
    
    Returns:
    --------
    sqlalchemy.engine.Engine
        Database connection engine
    """
    # Get database credentials from environment variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    
    # Create connection string
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Create and return engine
    return create_engine(connection_string)

def get_properties_from_database(filters=None):
    """
    Fetch property data from the database with optional filters.
    
    Parameters:
    -----------
    filters : dict, optional
        Filtering conditions for the query
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing property data
    """
    # Get database connection
    engine = get_database_connection()
    
    # Base query
    query = "SELECT * FROM properties"
    
    # Add filters if any
    if filters:
        where_clauses = []
        for key, value in filters.items():
            where_clauses.append(f"{key} = '{value}'")
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
    
    # Execute query and return results
    return pd.read_sql(query, engine)

def update_property_predictions(property_ids, predictions):
    """
    Update properties with their predicted sale probabilities.
    
    Parameters:
    -----------
    property_ids : list
        List of property IDs
    predictions : list
        List of corresponding sale probabilities
    """
    # Get database connection
    engine = get_database_connection()
    
    # Create connection
    with engine.connect() as conn:
        # Update each property
        for prop_id, prediction in zip(property_ids, predictions):
            conn.execute(
                sqlalchemy.text(
                    "UPDATE properties SET sale_probability = :prob, last_prediction_date = CURRENT_DATE WHERE id = :id"
                ),
                {"prob": float(prediction), "id": prop_id}
            )
        
        # Commit the transaction
        conn.commit()

if __name__ == "__main__":
    # Test connection
    try:
        engine = get_database_connection()
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}") 