import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PredictionResult } from '../PredictionResult';
import { predictSaleProbability } from '../../services/api';

// Mock the API service
jest.mock('../../services/api', () => ({
  predictSaleProbability: jest.fn(),
}));

describe('PredictionForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(<PredictionResult />);
    
    expect(screen.getByLabelText(/bedrooms/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/bathrooms/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/square footage/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/year built/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/lot size/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/zipcode/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /predict/i })).toBeInTheDocument();
  });

  it('submits form with correct data', async () => {
    const mockPrediction = { probability: 0.75 };
    (predictSaleProbability as jest.Mock).mockResolvedValueOnce(mockPrediction);

    render(<PredictionForm />);

    // Fill in form fields
    fireEvent.change(screen.getByLabelText(/bedrooms/i), { target: { value: '3' } });
    fireEvent.change(screen.getByLabelText(/bathrooms/i), { target: { value: '2' } });
    fireEvent.change(screen.getByLabelText(/square footage/i), { target: { value: '1500' } });
    fireEvent.change(screen.getByLabelText(/year built/i), { target: { value: '1990' } });
    fireEvent.change(screen.getByLabelText(/lot size/i), { target: { value: '5000' } });
    fireEvent.change(screen.getByLabelText(/zipcode/i), { target: { value: '02108' } });

    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /predict/i }));

    // Wait for API call
    await waitFor(() => {
      expect(predictSaleProbability).toHaveBeenCalledWith({
        bedrooms: 3,
        bathrooms: 2,
        sqft: 1500,
        year_built: 1990,
        lot_size: 5000,
        zipcode: '02108',
      });
    });

    // Check if prediction result is displayed
    expect(screen.getByText(/75%/i)).toBeInTheDocument();
  });

  it('handles API errors correctly', async () => {
    const errorMessage = 'Failed to get prediction';
    (predictSaleProbability as jest.Mock).mockRejectedValueOnce(new Error(errorMessage));

    render(<PredictionForm />);

    // Fill in form fields
    fireEvent.change(screen.getByLabelText(/bedrooms/i), { target: { value: '3' } });
    fireEvent.change(screen.getByLabelText(/bathrooms/i), { target: { value: '2' } });
    fireEvent.change(screen.getByLabelText(/square footage/i), { target: { value: '1500' } });
    fireEvent.change(screen.getByLabelText(/year built/i), { target: { value: '1990' } });
    fireEvent.change(screen.getByLabelText(/lot size/i), { target: { value: '5000' } });
    fireEvent.change(screen.getByLabelText(/zipcode/i), { target: { value: '02108' } });

    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /predict/i }));

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  it('validates form inputs', async () => {
    render(<PredictionForm />);

    // Try to submit empty form
    fireEvent.click(screen.getByRole('button', { name: /predict/i }));

    // Check for validation messages
    expect(screen.getByText(/bedrooms is required/i)).toBeInTheDocument();
    expect(screen.getByText(/bathrooms is required/i)).toBeInTheDocument();
    expect(screen.getByText(/square footage is required/i)).toBeInTheDocument();
    expect(screen.getByText(/year built is required/i)).toBeInTheDocument();
    expect(screen.getByText(/lot size is required/i)).toBeInTheDocument();
    expect(screen.getByText(/zipcode is required/i)).toBeInTheDocument();

    // API should not be called
    expect(predictSaleProbability).not.toHaveBeenCalled();
  });
}); 