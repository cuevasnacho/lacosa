import { useState } from 'react'
import './App.css'
import FormCrearPartida from '../../components/Formularios/CrearPartida/FormCrearPartida.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <FormCrearPartida />
    </>
  )
}

export default App
