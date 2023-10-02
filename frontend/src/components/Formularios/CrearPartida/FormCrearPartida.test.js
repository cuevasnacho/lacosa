import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FormCrearPartida from './FormCrearPartida';

// Mock localStorage
beforeEach(() => {
  Object.defineProperty(window, 'localStorage', {
    value: {
      getItem: jest.fn(),
      setItem: jest.fn(),
    },
    writable: true,
  });
});

test('submits the form with the default values', async () => {
  render(<FormCrearPartida />);

  // Fill in the form fields
  userEvent.type(screen.getByLabelText('Nombre de la Partida'), 'Mi Partida');
  userEvent.type(screen.getByLabelText('Mínimo de Jugadores'), '6');
  userEvent.type(screen.getByLabelText('Máximo de Jugadores'), '8');
  userEvent.type(screen.getByLabelText('Contraseña'), 'myPassword');

  // Submit the form
  userEvent.click(screen.getByText('Crear Partida'));

  // Wait for the form submission to complete (you might need to adjust the timing)
  await waitFor(() => {
    // Assertions after the form is submitted
    expect(window.localStorage.setItem).toHaveBeenCalled();
    expect(window.localStorage.setItem).toHaveBeenCalledWith('CrearPartida', expect.any(String));
  });

  // You can add more assertions if needed
});
