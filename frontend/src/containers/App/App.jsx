import './App.css'
import UnirsePartida from "../../components/UnirsePartida/UnirsePartida.jsx"
//import {BrowserRouter as Router,Routes,Route} from "react-router-dom"


function App() {
  
  return (
    <>
    <UnirsePartida></UnirsePartida>
    </>
  )
}
/*<Router>
      <Routes>
        <Route exact path="/UnirsePartida/:idJugador/:nombreJug" element={<UnirsePartida/>}></Route>
        <Route exact path="/lobby/:idPartida/:idJugador" element={<Lobby/>}></Route>
        <Route exact path='/' element={<Inicio/>}></Route>
      </Routes>
</Router>*/
export default App
