import { useState } from 'react'
import Carta from '../../components/Carta/Carta.jsx'
import './App.css'
import lacosa from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/lacosa.png'
import cuerdas_podridas from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/panico/cuerdas_podridas.png'


function App() {

  const carta_lacosa = {
    id: 1,
    template: "string",
    tipo: 0,
    imagen: lacosa,
    ubicacion: "mano"
  };

  const carta_cuerdas_podridas = {
    id: 2,
    template: "string",
    tipo: 1,
    imagen: cuerdas_podridas,
    ubicacion: "mano"
  };

  return (
    <>
      <Carta carta={carta_cuerdas_podridas} />
    </>
  )
}

export default App
