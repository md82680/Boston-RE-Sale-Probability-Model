import React, { useState } from 'react';
import { predictSaleProbability } from '../services/api';

interface FormData {
  bedrooms: number;
  bathrooms: number;
  sqft: number;
  year_built: number;
  lot_size: number;
  zipcode: string;
}

export const PredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    bedrooms: 0,
    bathrooms: 0,
    sqft: 0,
    year_built: 0,
    lot_size: 0,
    zipcode: '',
  });
  const [prediction, setPrediction] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const result = await predictSaleProbability(formData);
      setPrediction(result.probability);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get prediction');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'zipcode' ? value : Number(value)
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="bedrooms">Bedrooms</label>
        <input
          type="number"
          id="bedrooms"
          name="bedrooms"
          value={formData.bedrooms}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <div>
        <label htmlFor="bathrooms">Bathrooms</label>
        <input
          type="number"
          id="bathrooms"
          name="bathrooms"
          value={formData.bathrooms}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <div>
        <label htmlFor="sqft">Square Footage</label>
        <input
          type="number"
          id="sqft"
          name="sqft"
          value={formData.sqft}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <div>
        <label htmlFor="year_built">Year Built</label>
        <input
          type="number"
          id="year_built"
          name="year_built"
          value={formData.year_built}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <div>
        <label htmlFor="lot_size">Lot Size</label>
        <input
          type="number"
          id="lot_size"
          name="lot_size"
          value={formData.lot_size}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <div>
        <label htmlFor="zipcode">Zipcode</label>
        <input
          type="text"
          id="zipcode"
          name="zipcode"
          value={formData.zipcode}
          onChange={handleChange}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
        Predict
      </button>
      {prediction !== null && (
        <div className="text-center text-xl">
          Sale Probability: {(prediction * 100).toFixed(1)}%
        </div>
      )}
      {error && <div className="text-red-500">{error}</div>}
    </form>
  );
}; 