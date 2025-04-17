import { checkHealth, predictSaleProbability } from '../api';

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

      const input = {
        bedrooms: 3,
        bathrooms: 2,
        sqft: 1500,
        year_built: 1990,
        lot_size: 5000,
        zipcode: '02108',
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

      const input = {
        bedrooms: 3,
        bathrooms: 2,
        sqft: 1500,
        year_built: 1990,
        lot_size: 5000,
        zipcode: '02108',
      };

      await expect(predictSaleProbability(input)).rejects.toThrow('Failed to get prediction');
    });
  });
}); 