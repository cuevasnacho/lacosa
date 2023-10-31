import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import BotonAbandonar from '../components/AbandonarPartida/BotonAbandonar';
//Mock de la petición por fetch
const MOCK_POST={
    ok:true
}
const config ={
  headers:{
    "Content-Type":"application/json"
  },
  method:"POST"
};

//Mock del websocket
const mockWebSocket = {
    send: jest.fn(),
  };

beforeEach(()=>{
    global.fetch = jest.fn((args)=>{
      return Promise.resolve({
        ok:true,
        json:() => Promise.resolve(args === `http://localhost:8000/abandonar_lobby/2/1`?MOCK_POST:[])
      })
    })
  })

describe('BotonAbandonar', () => {
  test('debe enviar un mensaje WebSocket y realizar una solicitud HTTP al hacer click en el botton', async () => {
    const idJugador=1;
    const idLobby=2;
    const { getByText } = render(
      <BotonAbandonar idJugador={idJugador} idLobby={idLobby} websocket={mockWebSocket} />
    );
    const button = getByText('Abandonar');
    fireEvent.click(button);
    await waitFor(() => {
      expect(mockWebSocket.send).toHaveBeenCalledWith(
        JSON.stringify({ action: 'abandonar_lobby', data: idJugador })
      );
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith(`http://localhost:8000/lobbys/${idLobby}/${idJugador}`,config)    
    })
  });
});
