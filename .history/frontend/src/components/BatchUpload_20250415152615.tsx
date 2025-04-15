import { useState, Dispatch, SetStateAction } from 'react';
import { predictBatchProperties } from '../services/api';
import { Property, BatchPredictionResponse } from '../types';
import { validatePropertyData } from '../utils/validation';

const BatchUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [predictions, setPredictions] = useState<BatchPredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a CSV file to upload');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Parse CSV file
      const properties = await parseCSV(file);
      
      // Validate each property
      const validationErrors = properties.flatMap((property, index) => {
        const errors = validatePropertyData(property);
        return Object.keys(errors).length > 0 
          ? [`Row ${index + 1}: ${Object.values(errors).join(', ')}`] 
          : [];
      });
      
      if (validationErrors.length > 0) {
        setError(`Validation errors in CSV: ${validationErrors.join('; ')}`);
        setIsLoading(false);
        return;
      }
      
      // Send to API
      const result = await predictBatchProperties(properties);
      setPredictions(result);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred processing the file');
    } finally {
      setIsLoading(false);
    }
  };

  // Function to parse CSV (simplified - would need a more robust parser in production)
  const parseCSV = async (file: File): Promise<Property[]> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        try {
          const text = e.target?.result as string;
          const lines = text.split('\n');
          const headers = lines[0].split(',');
          
          const properties: Property[] = [];
          
          for (let i = 1; i < lines.length; i++) {
            if (!lines[i].trim()) continue;
            
            const values = lines[i].split(',');
            const property = {} as any;
            
            headers.forEach((header, index) => {
              const value = values[index].trim();
              
              // Convert to appropriate types
              if (['property_value', 'square_feet', 'bedrooms', 'bathrooms', 
                   'property_age', 'distance_to_t', 'school_rating', 'property_tax',
                   'lien_amount', 'mortgage_rate', 'income_to_mortgage_ratio',
                   'market_inventory_months', 'avg_days_on_market', 'years_owned'].includes(header)) {
                property[header] = parseFloat(value);
              } else if (header === 'has_liens') {
                property[header] = value.toLowerCase() === 'true';
              } else {
                property[header] = value;
              }
            });
            
            properties.push(property as Property);
          }
          
          resolve(properties);
          
        } catch (err) {
          reject(new Error('Error parsing CSV file. Please ensure it matches the required format.'));
        }
      };
      
      reader.onerror = () => {
        reject(new Error('Error reading file'));
      };
      
      reader.readAsText(file);
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Batch Property Predictions</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Upload Properties CSV
          </label>
          <p className="text-sm text-gray-500 mb-2">
            File should contain one property per row with all required fields
          </p>
          
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          />
        </div>
        
        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}
        
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading || !file}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Processing...' : 'Upload and Predict'}
          </button>
        </div>
      </form>
      
      {predictions && (
        <div className="mt-8">
          <h3 className="text-xl font-medium text-gray-900 mb-4">Batch Results</h3>
          <p className="mb-2">
            Processed {predictions.predictions.length} properties on {new Date(predictions.prediction_date).toLocaleDateString()}
          </p>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Property #
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Sale Probability
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {predictions.predictions.map((prob, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {index + 1}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        prob < 0.3 
                          ? 'bg-red-100 text-red-800' 
                          : prob < 0.7 
                            ? 'bg-yellow-100 text-yellow-800' 
                            : 'bg-green-100 text-green-800'
                      }`}>
                        {(prob * 100).toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="mt-4 flex justify-end">
            <button
              onClick={() => {
                // Convert to CSV and download
                const csv = "Property #,Sale Probability\n" + 
                  predictions.predictions.map((prob, index) => 
                    `${index + 1},${(prob * 100).toFixed(1)}%`
                  ).join('\n');
                
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.setAttribute('hidden', '');
                a.setAttribute('href', url);
                a.setAttribute('download', 'property_predictions.csv');
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
              }}
              className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Download Results
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BatchUpload;

