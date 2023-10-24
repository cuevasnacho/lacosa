import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import JugarCarta from '../components/Carta/JugarCarta';
import { toast } from 'react-toastify';
import { httpRequest } from '../services/HttpService.js';

const cartas = [{cartaNombre: "analisis", tipo: 0, id: 4},
    {cartaNombre: "lacosa", tipo: 0, id: 5},
    {cartaNombre: "sospecha", tipo: 0, id: 6},
    {cartaNombre: "cambio_de_lugar", tipo: 0, id: 7},]

const props = {
    carta: {cartaNombre: "analisis", tipo: 0, id: 4},
    socket: jest.fn(),
    jugadores: [{username: "user1", esTurno: true, eliminado: false},
                {username: "user2", esTurno: false, eliminado: false},
                {username: "user3", esTurno: false, eliminado: false},
                {username: "user4", esTurno: false, eliminado: false}],
    funcionDescartar: jest.fn(),
    mano: cartas
}

describe('JugarCarta', () => {
    it('Renders JugarCarta component', () => {
        render(<JugarCarta {...props}/>);
    });
});