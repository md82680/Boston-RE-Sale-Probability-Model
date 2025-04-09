"""Performance monitoring utilities for marketing campaigns and model predictions."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import logging
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/monitoring.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def evaluate_marketing_performance(campaign_results_path=None):
    """
    Evaluate marketing campaign performance against model predictions.
    
    Parameters:
    -----------
    campaign_results_path : str, optional
        Path to CSV file with campaign results
    
    Returns:
    --------
    dict
        Performance metrics and retraining recommendation
    """
    if campaign_results_path is None:
        # Find the most recent campaign results file
        marketing_dir = "marketing"
        result_files = [f for f in os.listdir(marketing_dir) if f.startswith("campaign_results")]
        if not result_files:
            logger.warning("No campaign results files found")
            return None
        
        # Sort by creation time
        result_files.sort(key=lambda x: os.path.getmtime(os.path.join(marketing_dir, x)), reverse=True)
        campaign_results_path = os.path.join(marketing_dir, result_files[0])
    
    # Load campaign results
    try:
        campaign_results = pd.read_csv(campaign_results_path)
        logger.info(f"Loaded campaign results from {campaign_results_path}")
    except Exception as e:
        logger.error(f"Error loading campaign results: {str(e)}")
        return None
    
    # Calculate performance metrics
    metrics = {}
    
    # Conversion rate (actual sales)
    metrics["conversion_rate"] = campaign_results["converted"].mean()
    
    # Model predicted average
    metrics["model_predicted_avg"] = campaign_results["sale_probability"].mean()
    
    # Calculate difference
    metrics["prediction_actual_diff"] = abs(metrics["model_predicted_avg"] - metrics["conversion_rate"])
    
    # Determine if retraining is recommended
    metrics["retrain_recommended"] = metrics["prediction_actual_diff"] > 0.15
    
    # Additional metrics
    metrics["total_contacts"] = len(campaign_results)
    metrics["total_conversions"] = campaign_results["converted"].sum()
    metrics["revenue_generated"] = campaign_results["converted"].sum() * campaign_results["commission"].mean()
    
    # ROI calculation if cost data is available
    if "campaign_cost" in campaign_results.columns:
        total_cost = campaign_results["campaign_cost"].sum()
        metrics["campaign_roi"] = (metrics["revenue_generated"] - total_cost) / total_cost
    
    # Log results
    logger.info(f"Campaign performance: {metrics['conversion_rate']:.2%} conversion rate")
    if metrics["retrain_recommended"]:
        logger.warning(
            f"Model retraining recommended: predicted {metrics['model_predicted_avg']:.2%}, "
            f"actual {metrics['conversion_rate']:.2%}"
        )
    
    # Save metrics to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_path = f"monitoring/metrics/campaign_metrics_{timestamp}.json"
    
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    
    return metrics

def trigger_model_retraining():
    """
    Trigger model retraining process.
    """
    logger.info("Triggering model retraining")
    
    # Create a flag file for the retraining process
    retrain_flag_path = "monitoring/retrain_flag.txt"
    with open(retrain_flag_path, "w") as f:
        f.write(f"Retraining triggered at {datetime.now().isoformat()}")
    
    # In a production system, this might call an API endpoint or submit a job
    # to a workflow orchestrator like Airflow, Prefect, or Kubeflow
    logger.info(f"Retraining flag created at {retrain_flag_path}")

def generate_performance_charts(metrics_directory="monitoring/metrics"):
    """
    Generate performance charts from saved metrics.
    
    Parameters:
    -----------
    metrics_directory : str
        Directory containing saved metrics JSON files
    """
    # Find all metrics files
    metrics_files = [f for f in os.listdir(metrics_directory) if f.endswith(".json")]
    if not metrics_files:
        logger.warning(f"No metrics files found in {metrics_directory}")
        return
    
    # Load metrics
    all_metrics = []
    for file in metrics_files:
        file_path = os.path.join(metrics_directory, file)
        try:
            with open(file_path, "r") as f:
                metrics = json.load(f)
                # Extract date from filename
                date_str = file.split("_")[2].split(".")[0]
                metrics["date"] = datetime.strptime(date_str, "%Y%m%d")
                all_metrics.append(metrics)
        except Exception as e:
            logger.error(f"Error loading metrics from {file_path}: {str(e)}")
    
    # Convert to DataFrame and sort by date
    metrics_df = pd.DataFrame(all_metrics)
    metrics_df = metrics_df.sort_values("date")
    
    # Create charts directory
    charts_dir = "visualizations/performance"
    os.makedirs(charts_dir, exist_ok=True)
    
    # Generate conversion rate vs predicted probability chart
    plt.figure(figsize=(10, 6))
    plt.plot(metrics_df["date"], metrics_df["conversion_rate"], label="Actual Conversion Rate", marker="o")
    plt.plot(metrics_df["date"], metrics_df["model_predicted_avg"], label="Predicted Probability", marker="x")
    plt.title("Model Prediction Accuracy Over Time")
    plt.xlabel("Campaign Date")
    plt.ylabel("Probability / Rate")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "prediction_accuracy.png"), dpi=300)
    
    # Generate ROI chart if available
    if "campaign_roi" in metrics_df.columns:
        plt.figure(figsize=(10, 6))
        plt.bar(metrics_df["date"], metrics_df["campaign_roi"])
        plt.title("Campaign ROI Over Time")
        plt.xlabel("Campaign Date")
        plt.ylabel("ROI")
        plt.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "campaign_roi.png"), dpi=300)
    
    logger.info(f"Performance charts generated in {charts_dir}")

if __name__ == "__main__":
    # Test the performance evaluation
    metrics = evaluate_marketing_performance()
    
    if metrics and metrics["retrain_recommended"]:
        trigger_model_retraining()
    
    # Generate performance charts
    generate_performance_charts() 