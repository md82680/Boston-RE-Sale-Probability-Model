import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_boston_real_estate_data(num_properties=1000, random_seed=42):
    """
    Generate synthetic Boston real estate data with sale probability
    
    Parameters:
    -----------
    num_properties : int
        Number of properties to generate
    random_seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    pandas.DataFrame
        Dataframe containing synthetic property data
    """
    # Set random seed
    np.random.seed(random_seed)
    
    # Define Boston neighborhoods
    boston_neighborhoods = [
        'Back Bay', 'Beacon Hill', 'North End', 'South End', 'Fenway',
        'Allston', 'Brighton', 'Jamaica Plain', 'Roxbury', 'Dorchester',
        'South Boston', 'East Boston', 'Charlestown', 'West Roxbury', 
        'Hyde Park', 'Mattapan', 'Roslindale'
    ]
    
    # Generate data
    data = {
        'years_owned': np.random.randint(1, 40, num_properties),
        'property_value': np.random.normal(750000, 250000, num_properties),
        'square_feet': np.random.normal(1800, 600, num_properties),
        'bedrooms': np.random.choice([1, 2, 3, 4, 5, 6], num_properties, p=[0.05, 0.2, 0.4, 0.25, 0.07, 0.03]),
        'bathrooms': np.random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4], num_properties, 
                                      p=[0.1, 0.15, 0.3, 0.2, 0.15, 0.05, 0.05]),
        'property_age': np.random.normal(70, 40, num_properties),
        'neighborhood': np.random.choice(boston_neighborhoods, num_properties),
        'distance_to_t': np.random.gamma(2, 2, num_properties),  # miles to nearest T station
        'school_rating': np.random.normal(7, 1.5, num_properties),  # 1-10 scale
        'property_tax': np.random.normal(8000, 3000, num_properties),  # Annual property tax
        'has_liens': np.random.choice([0, 1], num_properties, p=[0.9, 0.1]),  # 90% no liens
        'mortgage_rate': np.random.normal(0.035, 0.005, num_properties),  # Current mortgage rate
        'income_to_mortgage_ratio': np.random.normal(3.5, 1, num_properties),  # Higher is better
        'market_inventory_months': np.random.normal(3, 1, num_properties),  # Months of inventory
        'avg_days_on_market': np.random.normal(30, 15, num_properties)  # Average days on market
    }
    
    # Create dataframe
    df = pd.DataFrame(data)
    
    # Clean up data - enforce realistic bounds
    df['property_value'] = np.maximum(df['property_value'], 200000)
    df['square_feet'] = np.maximum(df['square_feet'], 500)
    df['property_age'] = np.maximum(df['property_age'], 0)
    df['school_rating'] = np.clip(df['school_rating'], 1, 10)
    df['distance_to_t'] = np.maximum(df['distance_to_t'], 0.1)
    
    # Add lien amount for properties with liens
    df['lien_amount'] = 0
    has_lien_mask = df['has_liens'] == 1
    df.loc[has_lien_mask, 'lien_amount'] = df.loc[has_lien_mask, 'property_value'] * np.random.uniform(0.05, 0.3, has_lien_mask.sum())
    
    # Generate transaction dates
    current_date = datetime.now()
    max_days_back = 365 * 40  # Maximum 40 years back
    days_back = np.random.randint(0, max_days_back, num_properties)
    transaction_dates = [(current_date - timedelta(days=int(days))).strftime('%Y-%m-%d') for days in days_back]
    df['last_transaction_date'] = transaction_dates
    
    # Calculate sale probability based on various factors
    sale_probability = np.zeros(num_properties)
    
    # Base probability
    sale_probability += np.random.normal(0.3, 0.05, num_properties)
    
    # Adjust based on years owned (U-shaped: more likely when new or very old)
    years_effect = -0.01 * df['years_owned'] + 0.0003 * df['years_owned']**2
    sale_probability += years_effect
    
    # Adjust based on property value (higher value properties slightly less likely to sell)
    value_effect = -0.05 * (df['property_value'] / 1000000)
    sale_probability += value_effect
    
    # Liens dramatically decrease sale probability
    sale_probability -= 0.3 * df['has_liens']
    
    # Higher income to mortgage ratio increases probability
    sale_probability += 0.03 * (df['income_to_mortgage_ratio'] - 3)
    
    # Market factors
    sale_probability -= 0.03 * (df['market_inventory_months'] - 3)  # Higher inventory lowers probability
    sale_probability -= 0.003 * (df['avg_days_on_market'] - 30)  # Longer DOM lowers probability
    
    # Finalize probabilities
    df['sale_probability'] = np.clip(sale_probability, 0.01, 0.99)
    
    return df

if __name__ == "__main__":
    # Generate data
    boston_real_estate = generate_boston_real_estate_data(1000)
    
    # Save to CSV
    boston_real_estate.to_csv('../data/boston_real_estate_sale_probability.csv', index=False)
    print("Dataset saved to '../data/boston_real_estate_sale_probability.csv'")
