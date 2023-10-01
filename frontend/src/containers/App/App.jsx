import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Inicio from '../../components/Inicio/Inicio.jsx';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/'>
          <Route index element={<Inicio />}/>
          <Route path='home' element={<Inicio />}/>
          <Route path='crear' element={<Inicio />}/>
          <Route path='lobby/:idLobby' element={<Inicio />}/>
          <Route path='partida/:idPartida' element={<Inicio />}/>
          <Route path='*' element={<h1>Error 404 - Not Found</h1>}/>
        </Route>
      </Routes>
    </Router>
  )
}

export default App;
