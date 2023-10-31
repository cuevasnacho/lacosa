import { BrowserRouter as Router } from 'react-router-dom';
import { fireEvent,render,screen,waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Finalizar from '../components/FinalizarPartida/Finalizar';

const config_get={
    headers:{
      "Accept": "*/*",
      "Content-Type":"application/json"
    },
    method:"GET"
  };

  const config_delete={
    headers:{
      "Accept": "*/*",
      "Content-Type":"application/json"
    },
    method:"DELETE"
  };

const MOCK_DELETE={
    ok:true
}
const MOCK_GET ={
    jugadores:["messi","elbicho","elfideo"],
    ganadores:"Humanos"
}

  beforeEach(()=>{
    global.fetch = jest.fn((args)=>{
      return Promise.resolve({
        ok:true,
        json:() => Promise.resolve(args === `http://localhost:8000/partida/resultado/2`?MOCK_GET:{})
      })
    })
  })

  test("Conectando y mostrando los 3 Ganadores (messi,elbicho,elfideo)",async ()=>{
    const idpartida="2";
    const component=render(<Router><Finalizar idpartida={idpartida}/>);
      </Router>);
      await waitFor(()=>{
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith(`http://localhost:8000/partida/resultado/${idpartida}`,config_get);
        expect(screen.getByText('Victoria para Humanos')).toBeInTheDocument();
        expect(screen.getByText('messi')).toBeInTheDocument();
        expect(screen.getByText('elbicho')).toBeInTheDocument();
        expect(screen.getByText('elfideo')).toBeInTheDocument();
      })
  })

global.fetch = jest.fn((args)=>{
    return Promise.resolve({
        ok:true,
        json:() => Promise.resolve(args === `http://localhost:8000/partida/clear/2/3`?MOCK_DELETE:{})
    })
})
  describe('Finalizar', () => {
    test('Enviar petición DELETE al hacer click en "Volver Inicio"', async () => {
        const idjugador=3;
        const idpartida=2;
        const { getByText } = render(<Router>
            <Finalizar idjugador={idjugador} idpartida={idpartida} />
        </Router>);
        const button = getByText('Volver Inicio');
        fireEvent.click(button);
        await waitFor(() => {
            expect(fetch).toHaveBeenCalledTimes(2);
            expect(fetch).toHaveBeenCalledWith(`http://localhost:8000/partida/clear/${idpartida}/${idjugador}`,config_delete)    
        })
    });
  });