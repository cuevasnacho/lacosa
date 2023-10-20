import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import {setupServer} from 'msw/node'
import { rest } from 'msw';
import Finalizar from './Finalizar';
import { BrowserRouter as Router} from 'react-router-dom';

const MOCK_GET =[ [
    { nombre_jugador:"messi",equipo:"Humanos"}
  ],
  {ganadores:"humanos"}
];
  const server = setupServer(
    rest.get('http://localhost:3000/jugadoresDB', (req, res, ctx) => res(ctx.status(200), ctx.json(MOCK_GET))),
  );
beforeAll(()=>server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
test('Conectado y un jugador gano', async () => {
    const component = render(<Router>
      <Finalizar/>
    </Router>);
    component.debug()
    await component.findByText('messi');
    /*
    await component.findByText('Humanos');*/
  });

/*
test("Mostrar 4 jugadores no repetidos con exito",()=>{
    const jugadoresDB={
        "jugadores":[
            {
                nombre_jugador:"LionelMessi",
                equipo:"Humano"
            },
            {
                nombre_jugador:"elbicho",
                equipo:"Humano"
            },
            {
                nombre_jugador:"elcelebro",
                equipo:"Humano"
            },
            {
                nombre_jugador:"bichiFuerte",
                equipo:"Humano"
            }
        ],
        "ganador":"Humanos"
    }
    const component = render(<Router>
        <Finalizar jugadoresDB={jugadoresDB}/>
    </Router>);
    component.getByText("Victoria para los Humanos")
    component.getByText("LionelMessi")
    component.getByText("elbicho")
    component.getByText("elcelebro")
    component.getByText("bichiFuerte")
    component.getAllByText("Humano")
})*/