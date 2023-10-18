import React from 'react';
import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import ManoJugador from '../components/ManoJugador/ManoJugador.jsx';

const mockCards0 = [];

const mockCards1 = [{cartaNombre: "lacosa", id: 1, tipo: true}];

const mockCards4 = [
  {cartaNombre: "lacosa", id: 1, tipo: true},
  {cartaNombre: "lanzallamas", id: 2, tipo: true},
  {cartaNombre: "lanzallamas", id: 3, tipo: true},
  {cartaNombre: "lanzallamas", id: 4, tipo: true},
];

const mockCards6 = [
  {cartaNombre: "lacosa", id: 1, tipo: true},
  {cartaNombre: "lanzallamas", id: 2, tipo: true},
  {cartaNombre: "lanzallamas", id: 3, tipo: true},
  {cartaNombre: "lanzallamas", id: 4, tipo: true},
  {cartaNombre: "lanzallamas", id: 5, tipo: true},
  {cartaNombre: "lanzallamas", id: 6, tipo: true},
];

const esTurno = true;
const actualizar = jest.fn();

describe('ManoJugador', () => {
  it('renders 0 cards when cards.length is 0', () => {
    const { getAllByTestId } = render(<ManoJugador cartas={mockCards0} esTurno={esTurno} actualizar={actualizar}/>);
    let components = [];

    try {
      components = getAllByTestId('carta');
      fail('there are elements rendered');
    }
    catch (error) {
      expect(components.length).toBe(0);
    }
  });

  it('renders 1 cards when cards.length is 1', () => {
    const { getAllByTestId } = render(<ManoJugador cartas={mockCards1} esTurno={esTurno} actualizar={actualizar}/>);
    const components = getAllByTestId('carta');

    expect(components.length).toBe(1);
  });

  it('renders 4 cards when cards.length is 4', () => {
    const { getAllByTestId } = render(<ManoJugador cartas={mockCards4} esTurno={esTurno} actualizar={actualizar}/>);
    const components = getAllByTestId('carta');

    expect(components.length).toBe(4);
  });

  it('renders 6 cards when cards.length is 6', () => {
    const { getAllByTestId } = render(<ManoJugador cartas={mockCards6} esTurno={esTurno} actualizar={actualizar}/>);
    const components = getAllByTestId('carta');

    expect(components.length).toBe(6);
  });
});