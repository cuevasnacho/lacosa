import Mesa from '../Mesa/Mesa.jsx';
import { useNavigate } from 'react-router-dom';

const Partida = function () {
  const usuario = JSON.parse(sessionStorage.getItem('logged'));

  const navigate = useNavigate();

  const volverHome = () => {
    navigate('/home');
  }

  return (
    <>
      <ManoJugador cartas={""}/>
      <Mesa />
    </>
  )
}

export default Partida;