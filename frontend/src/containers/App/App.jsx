import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Inicio from '../../components/Inicio/Inicio.jsx';
import Lobby from '../../components/Lobby/Lobby.jsx';
import FormCrearPartida from '../../components/Formularios/CrearPartida/FormCrearPartida.jsx';
import UnirsePartida from '../../components/UnirsePartida/UnirsePartida';
import Partida from '../../components/Partida/Partida.jsx';
import { DefensaMock } from '../../components/Defensa/DefensaMock.jsx';

function App() {
  return (
    <Router>
      <Routes>
          <Route index element={<Inicio />}/>
          <Route path='/home' element={<UnirsePartida />}/>
          <Route path='/crear' element={<FormCrearPartida />}/>
          <Route path='/lobby/:idLobby' element={<Lobby />}/>
          <Route path='/partida/:idPartida' element={<Partida />}/>
          <Route path='*' element={<h1>Error 404 - Not Found</h1>}/>
      </Routes>
    </Router>
  )
}

export default App;
