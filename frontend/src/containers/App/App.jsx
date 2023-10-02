
import { useState } from 'react'
import './App.css'
import ManoJugador from '../../components/ManoJugador/ManoJugador'
import Diccionario from '../../components/Carta/Diccionario'

function App() {
  const [cartas, setCartas] = useState([Diccionario['lacosa'], Diccionario['cuerdas_podridas'], Diccionario['lacosa'], Diccionario['cuerdas_podridas']])
  return (
    <>
      <ManoJugador cartas={cartas} />
    </>
  )
}

export default App
