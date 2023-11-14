import {screen,render } from '@testing-library/react';
import '@testing-library/jest-dom';
import LogPartida from '../components/LogPartida/LogPartida';

const MockJugadas = [{"msj":"pepe jugó la carta lanzallamas contra valcu"},
{"msj":"messi jugó la carta sospecha contra pepe2"},{"msj":"pepe3 jugó la carta lanzallamas contra valcu2"}];

test('Mostrando 3 jugadas', () => {
    const component = render(<LogPartida messages={MockJugadas}/>);
    component.findByText("Historial de Jugadas");
})

