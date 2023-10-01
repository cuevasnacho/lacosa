import React from 'react';
import { render, fireEvent, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import InicioForm from './InicioForm';

describe('InicioForm', () => {
  beforeEach(() => {
    // Reset the mocks before each test
    jest.clearAllMocks();
  });

  it('should render the form', () => {
    render(<InicioForm />);
    expect(screen.getByText('INGRESE EL NOMBRE DE SU USUARIO')).toBeInTheDocument();
    expect(screen.getByText('Ingresar')).toBeInTheDocument();
  });
});
