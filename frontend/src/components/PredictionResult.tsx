import React from 'react';
import { PredictionResponse } from '../types';

interface PredictionResultProps {
  prediction: PredictionResponse;
}

const PredictionResult = ({ prediction }: PredictionResultProps) => {
  const probability = prediction.sale_probability * 100;
  
  // Determine color based on probability
  const getColorClass = () => {
    if (probability < 30) return 'text-red-600';
    if (probability < 70) return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <div className="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200">
      <h3 className="text-xl font-medium text-gray-900 mb-4">Prediction Result</h3>
      
      <div className="flex flex-col md:flex-row justify-between">
        <div className="mb-4 md:mb-0">
          <p className="text-sm text-gray-500">Sale Probability</p>
          <p className={`text-4xl font-bold ${getColorClass()}`}>
            {probability.toFixed(1)}%
          </p>
        </div>
        
        <div className="flex flex-col">
          <div className="mb-2">
            <p className="text-sm text-gray-500">Prediction Date</p>
            <p className="text-lg">
              {new Date(prediction.prediction_date).toLocaleDateString()}
            </p>
          </div>
          
          <div>
            <p className="text-sm text-gray-500">Model Version</p>
            <p className="text-lg">{prediction.model_version}</p>
          </div>
        </div>
      </div>
      
      <div className="mt-6">
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div 
            className={`h-4 rounded-full ${
              probability < 30 
                ? 'bg-red-500' 
                : probability < 70 
                  ? 'bg-yellow-500' 
                  : 'bg-green-500'
            }`} 
            style={{ width: `${probability}%` }}
          ></div>
        </div>
        
        <div className="flex justify-between mt-1 text-xs text-gray-500">
          <span>Low Probability</span>
          <span>Medium Probability</span>
          <span>High Probability</span>
        </div>
      </div>
      
      <div className="mt-6">
        <h4 className="text-md font-medium text-gray-900 mb-2">What does this mean?</h4>
        <p className="text-gray-600">
          {probability < 30 
            ? "This property has a low probability of selling in the current market. Consider adjusting the price or making improvements before listing."
            : probability < 70 
              ? "This property has a moderate chance of selling. The right marketing and pricing strategy could improve its prospects."
              : "This property has a high probability of selling quickly in the current market."
          }
        </p>
      </div>
    </div>
  );
};

export default PredictionResult;
