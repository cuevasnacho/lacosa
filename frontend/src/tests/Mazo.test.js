import React from 'react';
import '@testing-library/jest-dom';
import { render, fireEvent, getByTestId, screen } from '@testing-library/react';
import Mazo from '../components/Mazo/Mazo.jsx';
import { robarCarta } from '../components/Mazo/RobarCarta.jsx';

const mockCartas1 = [
  {cartaNombre: 'analisis', id: 2, tipo: 0},
  {cartaNombre: 'lacosa', id: 3, tipo: 0},
  {cartaNombre: 'lanzallamas', id: 5, tipo: 0},
  {cartaNombre: 'cuerdas_podridas', id: 1, tipo: 1},
];

const mockCartas2 = [
  {cartaNombre: 'analisis', id: 2, tipo: 0},
  {cartaNombre: 'lacosa', id: 3, tipo: 0},
  {cartaNombre: 'lanzallamas', id: 5, tipo: 0},
  {cartaNombre: 'cuerdas_podridas', id: 1, tipo: 1},
  {cartaNombre: 'lanzallamas', id: 4, tipo: 0},
];

const mockCartas3 = [
  {cartaNombre: 'lacosa', id: 3, tipo: 0},
  {cartaNombre: 'lanzallamas', id: 5, tipo: 0},
  {cartaNombre: 'cuerdas_podridas', id: 1, tipo: 1},
];

// Mock the robarCarta function
jest.mock('../components/Mazo/RobarCarta.jsx', () => ({
  robarCarta: jest.fn(),
}));

describe('Mazo', () => {
  it('renders the Mazo button and handles click event when the length of mano is 4', () => {
    const esTurno = true;
    const actualizarMano = jest.fn();

    const { getByTestId } = render(
      <Mazo esTurno={esTurno} mano={mockCartas1} actualizarMano={actualizarMano} />
    );

    const mazoButton = getByTestId('mazo');

    fireEvent.click(mazoButton);

    expect(robarCarta).toHaveBeenCalledTimes(1);
    expect(robarCarta).toHaveBeenCalledWith(mockCartas1, actualizarMano);
  });

  it('renders the Mazo button and shows an alert when the length of mano is greater than 4', () => {
    const esTurno = true;
    const actualizarMano = jest.fn();

    window.alert = jest.fn(); // Mock the window.alert function

    const { getByTestId } = render(
      <Mazo esTurno={esTurno} mano={mockCartas2} actualizarMano={actualizarMano} />
    );

    const mazoButton = getByTestId('mazo');

    fireEvent.click(mazoButton);

    expect(robarCarta).toHaveBeenCalledTimes(0);
    expect(window.alert).toHaveBeenCalledWith("No se puede robar mas cartas");
  });

  it('renders the Mazo button and handles click event when the length of mano is less than 4', () => {
    const esTurno = true;
    const actualizarMano = jest.fn();

    const { getByTestId } = render(
      <Mazo esTurno={esTurno} mano={mockCartas3} actualizarMano={actualizarMano} />
    );

    const mazoButton = getByTestId('mazo');

    fireEvent.click(mazoButton);

    expect(robarCarta).toHaveBeenCalledTimes(1);
    expect(robarCarta).toHaveBeenCalledWith(mockCartas3, actualizarMano);
  });  
});