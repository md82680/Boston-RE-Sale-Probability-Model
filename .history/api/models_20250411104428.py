"""Pydantic models for the API."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import datetime

class Property(BaseModel):
    """Model for property data input."""
    
    years_owned: int = Field(..., ge=1, le=100)
    property_value: float = Field(..., ge=50000)
    square_feet: int = Field(..., ge=200)
    bedrooms: int = Field(..., ge=0, le=10)
    bathrooms: float = Field(..., ge=0, le=10)
    property_age: int = Field(..., ge=0)
    neighborhood: str
    distance_to_t: float = Field(..., ge=0)
    school_rating: float = Field(..., ge=1, le=10)
    property_tax: float = Field(..., ge=0)
    has_liens: int = Field(..., ge=0, le=1)
    lien_amount: float = Field(..., ge=0)
    mortgage_rate: float = Field(..., ge=0, le=20)
    income_to_mortgage_ratio: float = Field(..., ge=0)
    market_inventory_months: float = Field(..., ge=0)
    avg_days_on_market: int = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "years_owned": 15,
                "property_value": 750000,
                "square_feet": 1800,
                "bedrooms": 3,
                "bathrooms": 2.5,
                "property_age": 85,
                "neighborhood": "South End",
                "distance_to_t": 0.5,
                "school_rating": 7.5,
                "property_tax": 6500,
                "has_liens": 0,
                "lien_amount": 0,
                "mortgage_rate": 3.5,
                "income_to_mortgage_ratio": 3.8,
                "market_inventory_months": 2.5,
                "avg_days_on_market": 30
            }
        }


class BatchPropertyRequest(BaseModel):
    """Model for batch property prediction request."""
    
    properties: List[Property]


class PredictionResponse(BaseModel):
    """Model for prediction response."""
    
    sale_probability: float
    prediction_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    model_version: str = "1.0.0"


class BatchPredictionResponse(BaseModel):
    """Model for batch prediction response."""
    
    predictions: List[float]
    prediction_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    model_version: str = "1.0.0" 