import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the API module
jest.mock('./services/api', () => ({
  checkHealth: jest.fn().mockResolvedValue({ status: 'ok', model_loaded: true })
}));

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Boston Real Estate Sale Probability/i)).toBeInTheDocument();
  });

  it('shows loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/Connecting to API/i)).toBeInTheDocument();
  });
}); 