import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import {setupServer} from 'msw/node'
import { rest } from 'msw';
import Finalizar from './Finalizar';
import { BrowserRouter as Router} from 'react-router-dom';

const MOCK_GET_Humanos ={
      jugadores:[
        { nombre_jugador:"messi",equipo:"Humanos"},
        { nombre_jugador:"elbicho..suuuuuu",equipo:"Humanos"},
        { nombre_jugador:"lebronjames",equipo:"Humanos"},
        { nombre_jugador:"elcutiromero",equipo:"Humanos"},
      ],
    ganador:"Humanos",
} 
const server = setupServer(
  rest.get('http://127.0.0.1:8000/abandonar', (req, res, ctx) => res(ctx.status(200), ctx.json(MOCK_GET_Humanos))),
);
beforeAll(()=>server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
test('Conectado y 5 ganadores', async () => {
    const component = render(<Router>
      <Finalizar/>
    </Router>);
    await component.findByText('messi');
    await component.findByText('elbicho..suuuuuu');
    await component.findByText('lebronjames');
    await component.findByText('elcutiromero');
    await component.findByText('Victoria para los Humanos');
});

  test('No hay ganadores', async () => {
    server.use(
      rest.get('http://localhost:3000/jugadoresDB', (req, res, ctx) => res(ctx.status(200), ctx.json([]))),
    );
    const component = render(<Router>
      <Finalizar />
    </Router>);
    await component.findByText('No hay jugadores ganadores');
  });

