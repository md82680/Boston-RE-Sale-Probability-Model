"""Main FastAPI application for the property sale prediction API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

# Add project root to path to allow imports from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import Property, PredictionResponse
from api.endpoints import router as api_router

# Create FastAPI app
app = FastAPI(
    title="Boston Real Estate Sale Probability API",
    description="API for predicting the probability of property sales in Boston",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Boston Real Estate Sale Probability API",
        "documentation": "/docs",
        "api_endpoints": "/api"
    }

if __name__ == "__main__":
    # Run the API server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 