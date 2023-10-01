import './App.css'
import lacosa from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/alejate/lacosa.png'
import cuerdas_podridas from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/panico/cuerdas_podridas.png'
import ManoJugador from '../../components/ManoJugador/ManoJugador.jsx'


function App() {
  const cartitas = [lacosa, cuerdas_podridas, lacosa, cuerdas_podridas];

  return (
    <ManoJugador cartas={cartitas} />
  )
}

export default App
