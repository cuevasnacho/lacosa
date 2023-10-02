
import { useState } from 'react'
import './App.css'
import ManoJugador from '../../components/ManoJugador/ManoJugador'
import Diccionario from '../../components/Carta/Diccionario'
import Jugador from '../../components/Jugador/Jugador'

function App() {
  const [cartas, setCartas] = useState([Diccionario['lacosa'], Diccionario['cuerdas_podridas'], Diccionario['lacosa'], Diccionario['cuerdas_podridas']]);
  const user = "Juaen"
  return (
    <>
      <Jugador username={user} esTurno={false} />
    </>
  )
}

export default App
