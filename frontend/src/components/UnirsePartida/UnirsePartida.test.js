import { render } from '@testing-library/react';
import UnirsePartida from './UnirsePartida';
import { BrowserRouter as Router } from 'react-router-dom';
import { rest } from 'msw';
import {setupServer} from 'msw/node'
import '@testing-library/jest-dom';

const MOCK_GET = [
    { lobby_id:1,match_id: 1, lobby_name: 'PrimerPartida',number_of_players:6
     ,host_name: "host1",min_players:4,max_players:12,privada:false},
     { lobby_id:2,match_id: 3, lobby_name: 'SegundaPartida',number_of_players:7
     ,host_name: "host2",min_players:4,max_players:12,privada:false},
     { lobby_id:3,match_id: 3, lobby_name: 'TercerPartida',number_of_players:8
     ,host_name: "host3",min_players:4,max_players:12,privada:false},
     { lobby_id:1,match_id: 1, lobby_name: 'PrimerPartida',number_of_players:6
     ,host_name: "host1",min_players:4,max_players:12,privada:false},
  ];

  const server = setupServer(
    rest.get('http://localhost:5173/Partidas', (req, res, ctx) => res(ctx.status(200), ctx.json(MOCK_GET))),
  ); 

beforeAll(()=>server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('Conectado y hay 4 partidas disponibles incluyendo un nombre repetido', async () => {
    const component = render(<Router>
      <UnirsePartida />
    </Router>);
    await component.findByText('Nombre de Partida');
    await component.findByText('Host');
    await component.findByText('CantJug');
    await component.findAllByText('6/12');
    await component.findByText('7/12');
    await component.findByText('8/12');
    await component.findAllByText('PrimerPartida');
    await component.findByText('SegundaPartida');
    await component.findByText('Tercera Partida');
  });