"""Utilities for marketing outreach based on property predictions."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/marketing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailService:
    """Class to handle email service integration (e.g., SendGrid, Mailchimp)."""
    
    def __init__(self, api_key=None):
        """Initialize with API key from env vars if not provided."""
        self.api_key = api_key or os.getenv("EMAIL_API_KEY")
        self.api_url = os.getenv("EMAIL_API_URL")
        
        if not self.api_key:
            raise ValueError("Email API key not found. Set EMAIL_API_KEY environment variable.")
    
    def schedule_email(self, recipient_email, template_id, personalization_vars, send_date=None):
        """
        Schedule an email using the email service API.
        
        Parameters:
        -----------
        recipient_email : str
            Email address of the recipient
        template_id : str
            ID of the email template to use
        personalization_vars : dict
            Variables for template personalization
        send_date : datetime, optional
            When to send the email (defaults to now)
        
        Returns:
        --------
        dict
            Response from the email service API
        """
        # Format send date
        if send_date is None:
            send_date = datetime.now() + timedelta(hours=1)
        
        formatted_date = send_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Prepare request payload
        payload = {
            "recipient": recipient_email,
            "template_id": template_id,
            "personalization": personalization_vars,
            "scheduled_time": formatted_date
        }
        
        # Make API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/v1/email/schedule",
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scheduling email: {str(e)}")
            return {"error": str(e)}


def prioritize_properties(properties_df):
    """
    Create prioritized list of properties for marketing outreach.
    
    Parameters:
    -----------
    properties_df : pandas.DataFrame
        DataFrame of properties with sale probabilities
    
    Returns:
    --------
    pandas.DataFrame
        Properties sorted by outreach priority
    """
    # Score is based on sale probability and property value
    properties_df['outreach_score'] = (
        properties_df['sale_probability'] * 0.7 + 
        (properties_df['property_value'] / 1000000) * 0.3
    )
    
    # Return sorted properties
    return properties_df.sort_values('outreach_score', ascending=False)


def generate_personalization_vars(property_row):
    """
    Create personalized variables for email templates.
    
    Parameters:
    -----------
    property_row : pandas.Series
        Single property data row
    
    Returns:
    --------
    dict
        Personalization variables for email template
    """
    # Years owned text
    if property_row['years_owned'] > 25:
        years_owned_text = "many years"
    elif property_row['years_owned'] > 15:
        years_owned_text = "over a decade"
    elif property_row['years_owned'] > 5:
        years_owned_text = "several years"
    else:
        years_owned_text = "a few years"
    
    # Neighborhood
    neighborhood = property_row['neighborhood']
    
    # Customize message based on property characteristics
    if property_row['has_liens'] == 1:
        financial_message = "including options for properties with existing liens"
    elif property_row['property_value'] > 1000000:
        financial_message = "with specialized handling for luxury properties"
    else:
        financial_message = "with maximum return on your investment"
    
    return {
        "owner_name": property_row.get('owner_name', "Homeowner"),
        "property_address": property_row.get('address', "your Boston property"),
        "years_owned_text": years_owned_text,
        "neighborhood": neighborhood,
        "financial_message": financial_message,
        "predicted_probability": f"{property_row['sale_probability']:.0%}"
    }


def calculate_optimal_send_time(property_row):
    """
    Calculate the optimal time to send marketing email.
    
    Parameters:
    -----------
    property_row : pandas.Series
        Single property data row
    
    Returns:
    --------
    datetime
        Optimal date and time to send email
    """
    # Default to next Tuesday at 10:30 AM (typically good open rates)
    now = datetime.now()
    days_until_tuesday = (1 - now.weekday()) % 7
    
    if days_until_tuesday == 0:  # It's Tuesday today
        days_until_tuesday = 7  # Next Tuesday
    
    next_tuesday = now + timedelta(days=days_until_tuesday)
    send_time = next_tuesday.replace(hour=10, minute=30, second=0, microsecond=0)
    
    return send_time


def schedule_marketing_campaign(high_probability_df, email_api_key=None):
    """
    Schedule personalized emails for high-probability properties.
    
    Parameters:
    -----------
    high_probability_df : pandas.DataFrame
        DataFrame of high-probability properties
    email_api_key : str, optional
        API key for email service
    
    Returns:
    --------
    dict
        Campaign statistics and results
    """
    logger.info(f"Scheduling marketing campaign for {len(high_probability_df)} properties")
    
    # Prioritize properties
    prioritized_df = prioritize_properties(high_probability_df)
    
    # Initialize email service
    email_service = EmailService(api_key=email_api_key)
    
    # Track results
    results = {
        "total_properties": len(prioritized_df),
        "emails_scheduled": 0,
        "errors": 0
    }
    
    # For each property
    for idx, property_row in prioritized_df.iterrows():
        try:
            # Generate personalization
            personalization = generate_personalization_vars(property_row)
            
            # Select template based on property characteristics
            if property_row['property_value'] > 1000000:
                template_id = "luxury_property_template"
            elif property_row['has_liens'] == 1:
                template_id = "lien_property_template"
            else:
                template_id = "standard_property_template"
            
            # Calculate send time
            send_time = calculate_optimal_send_time(property_row)
            
            # Schedule email
            response = email_service.schedule_email(
                recipient_email=property_row['owner_email'],
                template_id=template_id,
                personalization_vars=personalization,
                send_date=send_time
            )
            
            if "error" not in response:
                results["emails_scheduled"] += 1
                logger.info(f"Scheduled email for property {property_row.get('id', idx)}")
            else:
                results["errors"] += 1
                logger.error(f"Error scheduling email for property {property_row.get('id', idx)}: {response['error']}")
        
        except Exception as e:
            results["errors"] += 1
            logger.error(f"Error processing property {property_row.get('id', idx)}: {str(e)}")
    
    # Log final results
    logger.info(f"Campaign scheduled: {results['emails_scheduled']} emails, {results['errors']} errors")
    
    return results


if __name__ == "__main__":
    # Test with sample data
    from src.batch_predictions import run_prediction_batch
    
    high_prob_properties = run_prediction_batch(threshold=0.6)
    
    if len(high_prob_properties) > 0:
        campaign_results = schedule_marketing_campaign(high_prob_properties)
        print(f"Campaign scheduled: {campaign_results['emails_scheduled']} emails")
    else:
        print("No high-probability properties found for marketing") 