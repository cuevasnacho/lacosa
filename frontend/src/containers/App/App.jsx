import { useState } from 'react'
import Carta from '../../components/Carta/Carta'
import lacosa from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/lacosa.png'

import './App.css'

function App() {
  const [count, setCount] = useState(0);

  const ejemplo = {
    id: 1,
    template: "string",
    tipo: 0,
    imagen: lacosa
  };
  return (
    <>
      <Carta carta={ejemplo} />
    </>
  )
}

export default App
