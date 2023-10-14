import React from 'react';
import '@testing-library/jest-dom';
import { render, fireEvent } from '@testing-library/react';
import Mazo from '../components/Mazo/Mazo.jsx';

describe('Mazo Component', () => {
  it('renders the Mazo button and handles click event', () => {
    const esTurno = true;
    const levantarCarta = jest.fn();

    const { getByTestId } = render(
      <Mazo esTurno={esTurno} levantarCarta={levantarCarta} />
    );

    const mazoButton = getByTestId('mazo');

    fireEvent.click(mazoButton);

    expect(levantarCarta).toHaveBeenCalledTimes(1);
  });

  it('renders the Mazo button and handles click event when esTurno is false', () => {
    const esTurno = false;
    const levantarCarta = jest.fn();

    const { getByTestId } = render(
      <Mazo esTurno={esTurno} levantarCarta={levantarCarta} />
    );

    const mazoButton = getByTestId('mazo');

    fireEvent.click(mazoButton);

    expect(levantarCarta).toHaveBeenCalledTimes(1);
  });
});
