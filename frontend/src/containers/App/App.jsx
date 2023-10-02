import { useState } from 'react'
import Carta from '../../components/Carta/Carta.jsx'
import './App.css'
import lacosa from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/lacosa.png'
import cuerdas_podridas from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/panico/cuerdas_podridas.png'


function App() {

  return (
    <>
      <Carta carta={cuerdas_podridas} />
    </>
  )
}

export default App
