import React, { useState } from 'react';
import { predictSaleProbability } from '../services/api';
import { validatePropertyData } from '../utils/validation';
import { Property, PredictionResponse } from '../types';
import PredictionResult from './PredictionResult';

const PropertyForm = () => {
  const [property, setProperty] = useState({
    years_owned: 0,
    has_liens: false,
    property_value: 0,
    last_transaction_date: new Date().toISOString().split('T')[0],
  } as Property);
  
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

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

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    
    // Client-side validation
    const validationErrors = validatePropertyData(property);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    
    setIsLoading(true);
    try {
      const result = await predictSaleProbability(property);
      setPrediction(result);
      setErrors({});
    } catch (error) {
      setErrors({ 
        submit: error instanceof Error 
          ? error.message 
          : 'An error occurred during prediction'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Property Sale Prediction</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Years Owned
            </label>
            <input
              type="number"
              name="years_owned"
              value={property.years_owned}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            {errors.years_owned && (
              <p className="mt-1 text-sm text-red-600">{errors.years_owned}</p>
            )}
          </div>

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
              Last Transaction Date
            </label>
            <input
              type="date"
              name="last_transaction_date"
              value={property.last_transaction_date}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            {errors.last_transaction_date && (
              <p className="mt-1 text-sm text-red-600">{errors.last_transaction_date}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Has Liens
            </label>
            <input
              type="checkbox"
              name="has_liens"
              checked={property.has_liens}
              onChange={handleChange}
              className="mt-2 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
          </div>
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
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-300"
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
