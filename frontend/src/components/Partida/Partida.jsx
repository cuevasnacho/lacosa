import { useEffect, useState } from 'react';
import styles from './Partida.module.css';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Jugadores from '../Jugador/Jugadores.jsx';
import Mazo from '../Mazo/Mazo.jsx';
import MazoDescarte from '../Mazo/MazoDescarte.jsx';

function Partida () {
  // const { ws } = socket;
  // const user_id = JSON.parse(sessionStorage.getItem('user_id'));
  // const username = JSON.parse(sessionStorage.getItem('username'));

  const [matchState, setMatchState] = useState({});
  const [mazoDescarteState, setMazoDescarteState] = useState(1);  // Dice que carta se va a mostrar en el mazo de descarte
  const [turno, setTurno] = useState(true);   // Indica si es mi turno o no
  const [jugadores, setJugadores] = useState([]); // username: string, id: int, esTurno: bool, posicion: int, eliminado: bool	
  const [cartas, setCartas] = useState([]); // cartas de la mano del jugador
  const [listo, setListo] = useState(false); // cuando todos los jugadores estan listos comienza la partida

/*
  ws.onmessage = function (event) {
    const info = JSON.parse(event.data);
    switch (info.action) {
      case 'cartas':
        datos = info.data.cartas;
        setCartas(datos);
        return;

      case ''

      default:
        return;
    }
  }
*/
  const cartass = [{cartaNombre: 'analisis', id: 2, tipo: 0},
                  {cartaNombre: 'lacosa', id: 3, tipo: 0},
                  {cartaNombre: 'lanzallamas', id: 5, tipo: 0},
                  {cartaNombre: 'cuerdas_podridas', id: 1, tipo: 1}];
  

  const jugadoress = [ {username: 'juan', esTurno: false, position: 7},
                      {username: 'pedro', esTurno: false, position: 1},
                      {username: 'tute', esTurno: false, position: 2},
                      {username: 'nacho', esTurno: false, position: 3},
                      {username: 'cabeza', esTurno: false, position: 4},
                      {username: 'negro', esTurno: false, position: 5},
                      {username: 'quito', esTurno: false, position: 6}];

  const sortedJugadores = jugadoress.sort((a,b) => a.position - b.position);

  return (
    <div className={styles.container}>
      {turno && (<div className={styles.tuTurno}/>)}
      <div className={styles.detalleMesa}/>
      <Mazo esTurno={turno}/>
      <MazoDescarte mazoDescarteState={mazoDescarteState}/>
      <ManoJugador cartas={cartass} esTurno={turno}/>
      <Jugadores jugadores={sortedJugadores}/>
    </div>
  );
}

export default Partida;