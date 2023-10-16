import React from 'react';
import { render, fireEvent, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import InicioForm from '../components/InicioForm/InicioForm.jsx';

// Mock the HTTP service
jest.mock('../services/HttpService.js', () => ({
  httpRequest: jest.fn(),
}));

describe('InicioForm', () => {
  beforeEach(() => {
    // Reset the mocks before each test
    jest.clearAllMocks();
  });

  it('submits form data on button click', async () => {
    const mockResponse = { player_id: 132, player_name: 'Ignacio' };
    // Mock the HTTP request function to return a response
    require('../services/HttpService.js').httpRequest.mockResolvedValueOnce(mockResponse);

    render(<InicioForm />);
    const input = screen.getByTestId('player_name');
    const submitButton = screen.getByText('Ingresar');

    // Enter a player name
    fireEvent.change(input, { target: { value: 'Ignacio' } });

    // Click the submit button
    fireEvent.click(submitButton);

    // Ensure that the form was submitted
    expect(await screen.findByText('Ingresar')).toBeInTheDocument();
  });

  it('displays error message if no player name is entered', async () => {
    render(<InicioForm />);
    const submitButton = screen.getByText('Ingresar');

    // Click the submit button without entering a player name
    fireEvent.click(submitButton);

    // Ensure that the error message is displayed
    expect(await screen.findByText('Debes ingresar un nombre!')).toBeInTheDocument();
  });
});
