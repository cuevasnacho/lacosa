import { useState } from 'react';
import styles from './Partida.module.css';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Carta from '../Carta/Carta.jsx';

function Partida () {
  // const { ws } = socket;
  // const user_id = JSON.parse(localStorage.getItem('user_id'));
  // const username = JSON.parse(localStorage.getItem('username'));

  const [matchState, setMatchState] = useState([]);
  const [mazoDescarteState, setMazoDescarteState] = useState(1);

  const toggleState = () => {
    setMazoDescarteState((prevState) => (prevState === 3 ? 1 : prevState + 1));
  };

  const levantarCarta = function () {
    alert("levante una carta");
  }

  const descarteError = function () {
    alert("este es el mazo de descarte!");
  }
/*
  ws.onmessage = function (event) {
    const info = JSON.parse(event.data);
    switch (info.action) {
      case 'estado_jugadores':
        setMatchState(info.data);
        return;

      default:
        return;
    }
  }
*/
  const cartas = ['analisis', 'lacosa', 'aterrador', 'cuerdas_podridas'];

  return (
    <div className={styles.container}>
      <button 
        className={styles.mazo} 
        type='button' 
        onClick={levantarCarta} />
      <button
        className={`${styles.mazoDescarte} ${styles[`mazoDescarteState${mazoDescarteState}`]}`}
        type='button' 
        onClick={toggleState} />
      <ManoJugador cartas={cartas} />
    </div>
  );
}

export default Partida;