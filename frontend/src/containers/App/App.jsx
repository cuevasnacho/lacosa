import { useState } from 'react'
import Carta from '../../components/Carta/Carta.jsx'
import '../../components/Carta/Diccionario.jsx'
import './App.css'

function App() {
  const [count, setCount] = useState(0);

  const ejemplo = {
    id: 1,
    template: "string",
    tipo: 0,
    imagen: analisis,
    tamaño: 250
  };
  return (
    <>
      <Carta carta={ejemplo} />
    </>
  )
}

export default App
