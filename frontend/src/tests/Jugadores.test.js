import React from 'react';
import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import Jugadores from '../components/Jugador/Jugadores.jsx';

const mockJugadores0 = [];

const mockJugadores1 = [
  {username: 'p1', id: 1, esTurno: true, posicion: 1, eliminado: false},
];

const mockJugadores4 = [
  {username: 'p1', id: 1, esTurno: true, posicion: 1, eliminado: false},
  {username: 'p2', id: 2, esTurno: false, posicion: 2, eliminado: false},
  {username: 'p3', id: 3, esTurno: false, posicion: 3, eliminado: false},
  {username: 'p4', id: 4, esTurno: false, posicion: 4, eliminado: false},
];

const mockJugadores9 = [
  {username: 'p1', id: 1, esTurno: true, posicion: 1, eliminado: false},
  {username: 'p2', id: 2, esTurno: false, posicion: 2, eliminado: false},
  {username: 'p3', id: 3, esTurno: false, posicion: 3, eliminado: false},
  {username: 'p4', id: 4, esTurno: false, posicion: 4, eliminado: false},
  {username: 'p5', id: 5, esTurno: false, posicion: 5, eliminado: false},
  {username: 'p6', id: 6, esTurno: false, posicion: 6, eliminado: false},
  {username: 'p7', id: 7, esTurno: false, posicion: 7, eliminado: false},
  {username: 'p8', id: 8, esTurno: false, posicion: 8, eliminado: false},
  {username: 'p9', id: 9, esTurno: false, posicion: 9, eliminado: false},
];

const mockJugadores12 = [
  {username: 'p1', id: 1, esTurno: true, posicion: 1, eliminado: false},
  {username: 'p2', id: 2, esTurno: false, posicion: 2, eliminado: false},
  {username: 'p3', id: 3, esTurno: false, posicion: 3, eliminado: false},
  {username: 'p4', id: 4, esTurno: false, posicion: 4, eliminado: false},
  {username: 'p5', id: 5, esTurno: false, posicion: 5, eliminado: false},
  {username: 'p6', id: 6, esTurno: false, posicion: 6, eliminado: false},
  {username: 'p7', id: 7, esTurno: false, posicion: 7, eliminado: false},
  {username: 'p8', id: 8, esTurno: false, posicion: 8, eliminado: false},
  {username: 'p9', id: 9, esTurno: false, posicion: 9, eliminado: false},
  {username: 'p10', id: 10, esTurno: false, posicion: 10, eliminado: false},
  {username: 'p11', id: 11, esTurno: false, posicion: 11, eliminado: false},
  {username: 'p12', id: 12, esTurno: false, posicion: 12, eliminado: false},
];

const mockJugadores15 = [
  {username: 'p1', id: 1, esTurno: true, posicion: 1, eliminado: false},
  {username: 'p2', id: 2, esTurno: false, posicion: 2, eliminado: false},
  {username: 'p3', id: 3, esTurno: false, posicion: 3, eliminado: false},
  {username: 'p4', id: 4, esTurno: false, posicion: 4, eliminado: false},
  {username: 'p5', id: 5, esTurno: false, posicion: 5, eliminado: false},
  {username: 'p6', id: 6, esTurno: false, posicion: 6, eliminado: false},
  {username: 'p7', id: 7, esTurno: false, posicion: 7, eliminado: false},
  {username: 'p8', id: 8, esTurno: false, posicion: 8, eliminado: false},
  {username: 'p9', id: 9, esTurno: false, posicion: 9, eliminado: false},
  {username: 'p10', id: 10, esTurno: false, posicion: 10, eliminado: false},
  {username: 'p11', id: 11, esTurno: false, posicion: 11, eliminado: false},
  {username: 'p12', id: 12, esTurno: false, posicion: 12, eliminado: false},
  {username: 'p13', id: 13, esTurno: false, posicion: 13, eliminado: false},
  {username: 'p14', id: 14, esTurno: false, posicion: 14, eliminado: false},
  {username: 'p15', id: 15, esTurno: false, posicion: 15, eliminado: false},
];

window.sessionStorage.getItem = jest.fn(() => '1'); // Mock user_id

describe('Jugadores', () => {
  beforeAll(() =>
    sessionStorage.setItem('user_id', 1)
  );

  afterAll(() => 
    sessionStorage.removeItem('user_id')
  );

  it('renders jugadores when jugadores.length is 0', () => {
    const { getAllByTestId } = render(<Jugadores jugadores={mockJugadores0} />);

    const middleJugadores = getAllByTestId('middle');

    expect(middleJugadores[0].children.length).toBe(1);
  });

  it('renders jugadores when jugadores.length is less than 4', () => {
    const { getAllByTestId } = render(<Jugadores jugadores={mockJugadores1} />);

    const middleJugadores = getAllByTestId('middle');

    expect(middleJugadores[0].children.length).toBe(1);
  });

  it('renders jugadores when jugadores.length is 4', () => {
    const { getAllByTestId } = render(<Jugadores jugadores={mockJugadores4} />);

    const middleJugadores = getAllByTestId('middle');

    expect(middleJugadores[0].children.length).toBe(mockJugadores4.length - 3);
  });

  it('renders jugadores when jugadores.length is more than 4 and less than 12', () => {
    const { getAllByTestId } = render(<Jugadores jugadores={mockJugadores9} />);

    const middleJugadores = getAllByTestId('middle');

    expect(middleJugadores[0].children.length).toBe(mockJugadores9.length - 3);
  });

  it('renders jugadores when jugadores.length is 12', () => {
    const { getAllByTestId } = render(<Jugadores jugadores={mockJugadores12} />);

    const middleJugadores = getAllByTestId('middle');

    expect(middleJugadores[0].children.length).toBe(mockJugadores12.length - 3);
  });

  it('renders jugadores when jugadores.length is more than 12', () => {
    const { getAllByTestId } = render(<Jugadores jugadores={mockJugadores15} />);

    const middleJugadores = getAllByTestId('middle');

    expect(middleJugadores[0].children.length).toBe(mockJugadores15.length - 3);
  });
});