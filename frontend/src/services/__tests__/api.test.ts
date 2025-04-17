import { checkHealth, predictSaleProbability } from '../api';
import { Property } from '../../types';

// Mock fetch
global.fetch = jest.fn();

describe('API Service', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  describe('checkHealth', () => {
    it('should return health status', async () => {
      const mockResponse = { status: 'ok', model_loaded: true };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await checkHealth();
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith('/api/health');
    });

    it('should throw error on failed request', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      await expect(checkHealth()).rejects.toThrow('Failed to check API health');
    });
  });

  describe('predictSaleProbability', () => {
    it('should return prediction result', async () => {
      const mockResponse = { probability: 0.75 };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const input: Property = {
        years_owned: 2,
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
      };

      const result = await predictSaleProbability(input);
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(input),
      });
    });

    it('should throw error on failed request', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const input: Property = {
        years_owned: 2,
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
      };

      await expect(predictSaleProbability(input)).rejects.toThrow('Failed to get prediction');
    });
  });
}); 