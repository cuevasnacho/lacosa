
import { useState } from 'react'
import './App.css'
import ManoJugador from '../../components/ManoJugador/ManoJugador'
import Diccionario from '../../components/Carta/Diccionario'
import Jugadores from '../../components/Jugador/Jugadores'

function App() {
  const [cartas, setCartas] = useState([Diccionario['lacosa'], Diccionario['cuerdas_podridas'], Diccionario['lacosa'], Diccionario['cuerdas_podridas']]);
  
  const test = [
    {
      username: 'Jugador 1',
      esTurno: false
    },
    {
      username: 'Jugador 2',
      esTurno: false
    },
    {
      username: 'Jugador 3',
      esTurno: true
    },
    {
      username: 'Jugador 4',
      esTurno: false
    }
  ];

  return (
    <>
      <Jugadores jugadores={test} />
    </>
  )
}

export default App
