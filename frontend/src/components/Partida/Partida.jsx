import Mesa from '../Mesa/Mesa.jsx';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Diccionario from '../Carta/Diccionario.jsx';
import styles from './Partida.module.css';
import mazo from '../../media/designs/cartas/misteriosa.png';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { httpRequest } from '../../services/HttpService.js';

const Partida = function () {
  const usuario = JSON.parse(sessionStorage.getItem('logged'));

  const navigate = useNavigate();

  const volverHome = () => {
    navigate('/home');
  }

  const levantarCarta = async () => {
    try {
      const response = await httpRequest({
        method: 'POST',
        service: 'levantar',
        payload: usuario.user_id
      });
      
      mycards = JSON.parse(sessionStorage.getItem('cards'));
      mycards.push(response.id_carta);
      window.sessionStorage.setItem('cards', JSON.stringify(mycards));

      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const [cartas, setCartas] = useState([Diccionario['lacosa'], Diccionario['lanzallamas']]);

  return (
    <div className={styles.container}>
      <div className={styles.manojugador}>
        <ManoJugador cartas={cartas} jugarCarta/>
      </div>
      <div className={styles.mazos}>
        <button type='button' onClick={levantarCarta}/>
        <img src={mazo} width={130}/>
      </div>
      <div className={styles.jugadores}>

      </div>
    </div>
  )
}

export default Partida;