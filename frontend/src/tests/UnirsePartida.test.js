import UnirsePartida from '../components/UnirsePartida/UnirsePartida';
import { BrowserRouter as Router } from 'react-router-dom';
import { render,screen,waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';


const MOCK_GET = [
  { lobby_id:1,match_id: 1, lobby_name: 'PrimerPartida',number_of_players:6
   ,host_name: 'host1',min_players:4,max_players:12,is_private:false},
   { lobby_id:2,match_id: 3, lobby_name: 'SegundaPartida',number_of_players:7
   ,host_name: 'host2',min_players:4,max_players:12,is_private:false},
   { lobby_id:3,match_id: 3, lobby_name: 'TercerPartida',number_of_players:8
   ,host_name: 'host3',min_players:4,max_players:12,is_private:false},
   { lobby_id:1,match_id: 1, lobby_name: 'CuartaPartida',number_of_players:5
   ,host_name: 'host4',min_players:4,max_players:12,is_private:false},
];


const config ={
  headers:{
    "Accept": "*/*",
    "Content-Type":"application/json"
  },
  method:"GET"
};
beforeEach(()=>{
  global.fetch = jest.fn((args)=>{
    return Promise.resolve({
      ok:true,
      json:() => Promise.resolve(args === `http://localhost:8000/partidas/listar`?MOCK_GET:[])
    })
  })
})

test("Conectando y mostrando la 4 partidas",async ()=>{
  const component=render(<Router><UnirsePartida/>);
    </Router>);
    await waitFor(()=>{
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith(`http://localhost:8000/partidas/listar`,config);
      //component.findByText('Lista de Partidas');
      expect(screen.getByText('Lista de Partidas')).toBeInTheDocument();
      expect(screen.getByText('Nombre de Partida')).toBeInTheDocument();
      expect(screen.getByText('Host')).toBeInTheDocument();
      expect(screen.getByText('CantJug')).toBeInTheDocument();
      expect(screen.getByText('PrimerPartida')).toBeInTheDocument();
      expect(screen.getByText('SegundaPartida')).toBeInTheDocument();
      expect(screen.getByText('TercerPartida')).toBeInTheDocument();
      expect(screen.getByText('CuartaPartida')).toBeInTheDocument();
      expect(screen.getByText('host1')).toBeInTheDocument();
      expect(screen.getByText('host2')).toBeInTheDocument();
      expect(screen.getByText('host3')).toBeInTheDocument();
      expect(screen.getByText('host4')).toBeInTheDocument();
      expect(screen.getByText('6/12')).toBeInTheDocument();
      expect(screen.getByText('7/12')).toBeInTheDocument();
      expect(screen.getByText('8/12')).toBeInTheDocument();
      expect(screen.getByText('5/12')).toBeInTheDocument();

    })
})