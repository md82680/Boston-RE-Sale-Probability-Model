import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import PropertyForm from '../PropertyForm';
import { predictSaleProbability } from '../../services/api';

// Mock the API service
jest.mock('../../services/api', () => ({
  predictSaleProbability: jest.fn(),
}));

describe('PropertyForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(<PropertyForm />);
    
    expect(screen.getByText(/Property Value/i)).toBeInTheDocument();
    expect(screen.getByText(/Square Feet/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Predict Sale Probability/i })).toBeInTheDocument();
  });

  it('submits form with correct data', async () => {
    const mockPrediction = { sale_probability: 0.75, prediction_date: new Date().toISOString(), model_version: '1.0.0' };
    (predictSaleProbability as jest.Mock).mockResolvedValueOnce(mockPrediction);

    render(<PropertyForm />);

    // Submit form with default values
    fireEvent.click(screen.getByRole('button', { name: /Predict Sale Probability/i }));

    // Wait for API call
    await waitFor(() => {
      expect(predictSaleProbability).toHaveBeenCalled();
    });
  });

  it('handles API errors correctly', async () => {
    const errorMessage = 'Failed to get prediction';
    (predictSaleProbability as jest.Mock).mockRejectedValueOnce(new Error(errorMessage));

    render(<PropertyForm />);

    // Submit form with default values
    fireEvent.click(screen.getByRole('button', { name: /Predict Sale Probability/i }));

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  it('shows loading state during submission', async () => {
    // Don't resolve the promise immediately to keep the loading state
    const mockPromise = new Promise(resolve => setTimeout(() => {
      resolve({ sale_probability: 0.75, prediction_date: new Date().toISOString(), model_version: '1.0.0' });
    }, 100));
    
    (predictSaleProbability as jest.Mock).mockReturnValueOnce(mockPromise);

    render(<PropertyForm />);

    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /Predict Sale Probability/i }));

    // Check for loading state
    expect(screen.getByText(/Processing/i)).toBeInTheDocument();
  });
}); 