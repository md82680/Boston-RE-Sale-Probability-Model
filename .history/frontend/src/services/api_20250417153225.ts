import { Property, BatchPropertyRequest, PredictionResponse, BatchPredictionResponse } from '../types';

const API_URL = '/api';

export async function predictSaleProbability(property: Property): Promise<PredictionResponse> {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(property),
  });

  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to get prediction');
    } catch (e) {
      throw new Error('Failed to get prediction');
    }
  }

  return response.json();
}

export async function predictBatchProperties(
  properties: Property[]
): Promise<BatchPredictionResponse> {
  const response = await fetch(`${API_URL}/predict/batch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ properties }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to get batch prediction');
  }

  return response.json();
}

export async function checkHealth(): Promise<{ status: string; model_loaded: boolean }> {
  const response = await fetch(`${API_URL}/health`);
  
  if (!response.ok) {
    throw new Error('Failed to check API health');
  }
  
  return response.json();
}
