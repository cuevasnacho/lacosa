import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FormCrearPartida from '../components/Formularios/CrearPartida/FormCrearPartida';


describe('FormCrearPartida', () => {
  
  it('renders FormCrearPartida component', () => {
    render(<FormCrearPartida />);
  });

});