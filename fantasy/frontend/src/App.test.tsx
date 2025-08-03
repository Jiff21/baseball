import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Fantasy Expected Start component', () => {
  render(<App />);
  const headerElement = screen.getByText(/Fantasy Expected Start/i);
  expect(headerElement).toBeInTheDocument();
});
