import React, { useState } from 'react';
import { predictSaleProbability } from '../services/api';
import { validatePropertyData } from '../utils/validation';
import { Property, PredictionResponse } from '../types';
import PredictionResult from './PredictionResult';
import { lookupPropertyDetails } from '../services/propertyApi';

const PropertyForm = () => {
  const [property, setProperty] = useState({
    address: '',
    years_owned: 0,
    property_value: 500000,
    square_feet: 1500,
    bedrooms: 3,
    bathrooms: 2,
    property_age: 25,
    neighborhood: 'South End',
    distance_to_t: 0.5,
    school_rating: 7.5,
    property_tax: 5000,
    has_liens: false,
    lien_amount: 0,
    mortgage_rate: 4.5,
    income_to_mortgage_ratio: 3.5,
    market_inventory_months: 3.0,
    avg_days_on_market: 30,
    last_transaction_date: new Date().toISOString().split('T')[0]
  } as Property);
  
  const [prediction, setPrediction] = useState(null as PredictionResponse | null);
  const [errors, setErrors] = useState({} as Record<string, string>);
  const [isLoading, setIsLoading] = useState(false);
  const [addressLookupResult, setAddressLookupResult] = useState(null);

  const handleChange = (e: any) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    // Handle different input types
    const processedValue = type === 'checkbox' 
      ? (e.target as HTMLInputElement).checked
      : type === 'number' 
        ? parseFloat(value) 
        : value;
        
    setProperty({
      ...property,
      [name]: processedValue
    });
  };

  const handleAddressChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const address = e.target.value;
    setProperty({ ...property, address });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // First, lookup property details
      const propertyDetails = await lookupPropertyDetails(property.address);
      
      // Calculate years owned from last transaction date
      const yearsOwned = calculateYearsOwned(propertyDetails.lastTransactionDate);
      
      // Update property with calculated data
      const updatedProperty = {
        ...property,
        years_owned: yearsOwned,
      };

      // Get prediction
      const result = await predictSaleProbability(updatedProperty);
      setPrediction(result);
      setErrors({});
    } catch (error) {
      setErrors({ 
        submit: error instanceof Error ? error.message : 'An error occurred' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Property Sale Prediction</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Property Address
          </label>
          <input
            type="text"
            name="address"
            value={property.address}
            onChange={handleAddressChange}
            placeholder="2 Helena St, Leominster, MA 01453"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        
        {/* Property details */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Form fields go here - I'll show a few examples */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Property Value ($)
            </label>
            <input
              type="number"
              name="property_value"
              value={property.property_value}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            {errors.property_value && (
              <p className="mt-1 text-sm text-red-600">{errors.property_value}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Square Feet
            </label>
            <input
              type="number"
              name="square_feet"
              value={property.square_feet}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            {errors.square_feet && (
              <p className="mt-1 text-sm text-red-600">{errors.square_feet}</p>
            )}
          </div>

          {/* Add more form fields for all property attributes */}
        </div>

        {errors.submit && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="text-sm text-red-700">{errors.submit}</div>
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {isLoading ? 'Processing...' : 'Predict Sale Probability'}
          </button>
        </div>
      </form>

      {prediction && <PredictionResult prediction={prediction} />}
    </div>
  );
};

export default PropertyForm;
