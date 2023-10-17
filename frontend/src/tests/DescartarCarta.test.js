import React from 'react';
import { useState } from 'react';
import '@testing-library/jest-dom';
import { render, fireEvent, screen } from '@testing-library/react';
import { descartarCarta } from '../components/Carta/DescartarCarta';
import ManoJugador from '../components/ManoJugador/ManoJugador';
import Carta from '../components/Carta/Carta';
import Diccionario from '../components/Carta/Diccionario';

jest.mock('../services/HttpService.js', () => ({
    httpRequest: jest.fn(),
  }));

  jest.mock('../components/Carta/DescartarCarta', () => ({
    descartarCarta: jest.fn(),
  }));

describe('DescartarCarta', () => {
    beforeEach(() => {
        // Reset the mocks before each test
        jest.clearAllMocks();
    });

    // Mockear mano del jugador
    let cartas = [{cartaNombre: "analisis", id: 1, tipo: 0},
    {cartaNombre: "lacosa", id: 2, tipo: 0},
    {cartaNombre: "lanzallamas", id: 3, tipo: 0},
    {cartaNombre: "cuerdas_podridas", id: 4, tipo: 0},
    {cartaNombre: "aterrador", id: 5, tipo: 0},];

    
    test('Happy path', () => { 
        const actualizarMano = jest.fn();

        const { getByAltText, getByText } = render(<
            Carta carta={cartas[0]} esTurno={true} actualizar={actualizarMano} mano={cartas} />);
        const cartita = getByAltText('analisis');

        fireEvent.mouseOver(cartita);

        const descartarButton = getByText('Descartar');

        fireEvent.click(descartarButton);

        expect(descartarCarta).toHaveBeenCalledTimes(1);
     })

    test('Descartar cuando se tiene cuatro cartas en la mano', () => { 
        const actualizarMano = jest.fn();

        let cartasTest2 = [{cartaNombre: "analisis", id: 1, tipo: 0},
        {cartaNombre: "lacosa", id: 2, tipo: 0},
        {cartaNombre: "lanzallamas", id: 3, tipo: 0},
        {cartaNombre: "cuerdas_podridas", id: 4, tipo: 0},];

        const { getByAltText, getByText } = render(<
            Carta carta={cartasTest2[0]} esTurno={true} actualizar={actualizarMano} mano={cartas} />);
        
            const cartita = getByAltText('analisis');

        fireEvent.mouseOver(cartita);

        const descartarButton = getByText('Descartar');

        fireEvent.click(descartarButton);
        
        // Se llama a descartarCarta pero nunca se actualiza la mano
        expect(descartarCarta).toHaveBeenCalledTimes(1);
        expect(actualizarMano).toHaveBeenCalledTimes(0);
     })
     
});