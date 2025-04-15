import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def train_test_split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets
    
    Parameters:
    -----------
    X : pandas.DataFrame
        Feature dataframe
    y : pandas.Series
        Target series
    test_size : float
        Proportion of data to use for testing
    random_state : int
        Random seed for reproducibility
        
    Returns:
    --------
    tuple
        (X_train, X_test, y_train, y_test)
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train, y_train, model_type='random_forest', params=None):
    """
    Train a regression model
    
    Parameters:
    -----------
    X_train : pandas.DataFrame
        Training features
    y_train : pandas.Series
        Training target
    model_type : str
        Type of model to train ('random_forest' or 'gradient_boosting')
    params : dict
        Model parameters. If None, default parameters are used.
        
    Returns:
    --------
    object
        Trained model
    """
    if model_type == 'random_forest':
        if params is None:
            params = {
                'n_estimators': 100, 
                'max_depth': 10,
                'min_samples_split': 5,
                'random_state': 42
            }
        model = RandomForestRegressor(**params)
    elif model_type == 'gradient_boosting':
        if params is None:
            params = {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 5,
                'random_state': 42
            }
        model = GradientBoostingRegressor(**params)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train the model
    model.fit(X_train, y_train)
    
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate a trained model
    
    Parameters:
    -----------
    model : object
        Trained model
    X_test : pandas.DataFrame
        Test features
    y_test : pandas.Series
        Test target
        
    Returns:
    --------
    dict
        Dictionary of evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2,
        'predictions': y_pred
    }

def plot_feature_importance(model, feature_names, output_file=None):
    """
    Plot feature importance for tree-based models
    
    Parameters:
    -----------
    model : object
        Trained model with feature_importances_ attribute
    feature_names : list
        List of feature names
    output_file : str
        Path to save the plot. If None, the plot is displayed but not saved.
    """
    if not hasattr(model, 'feature_importances_'):
        raise ValueError("Model does not have feature_importances_ attribute")
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Create dataframe for plotting
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    # Plot
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
    plt.title('Feature Importance')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300)
    plt.show()

def save_model(model, model_path, feature_names=None):
    """
    Save trained model and optional metadata
    
    Parameters:
    -----------
    model : object
        Trained model
    model_path : str
        Path to save the model file
    feature_names : list
        List of feature names (optional)
    """
    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save feature names if provided
    if feature_names is not None:
        feature_path = model_path.replace('.pkl', '_features.pkl')
        with open(feature_path, 'wb') as f:
            pickle.dump(feature_names, f)
    
    print(f"Model saved to {model_path}")

def load_model(model_path):
    """
    Load a trained model
    
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

if __name__ == "__main__":
    # Test code to verify functionality
    from preprocessing import load_data, prepare_features_targets
    
    # Load and prepare data
    df = load_data()
    X, y = prepare_features_targets(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    print("Model evaluation metrics:")
    for metric, value in metrics.items():
        if metric != 'predictions':
            print(f"{metric}: {value:.4f}")
    
    # Plot feature importance
    plot_feature_importance(model, X.columns.tolist())
