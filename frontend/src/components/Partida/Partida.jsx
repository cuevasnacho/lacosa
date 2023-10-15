import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import { sortPlayers } from './functions.js';
import styles from './Partida.module.css';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Jugadores from '../Jugador/Jugadores.jsx';
import Mazo from '../Mazo/Mazo.jsx';
import MazoDescarte from '../Mazo/MazoDescarte.jsx';

function Partida () {

  const idPlayer = JSON.parse(sessionStorage.getItem('user_id'));
  const { idPartida } = useParams();
  // const [websocket, setWebsocket] = useState(null);

  const [playerState, setPlayerState] = useState({});
  const [manoJugador, setManoJugador] = useState([]);   // Indica las cartas que tengo en la mano
  const [matchState, setMatchState] = useState([]); // username: string, id: int, esTurno: bool, posicion: int, eliminado: bool	
  const [mazoDescarteState, setMazoDescarteState] = useState(1);  // Dice que carta se va a mostrar en el mazo de descarte

  const initializeGame = async (ws) => {
    const responseStatus = await httpRequest({
      method: 'GET',
      service: `partida/status/${idPartida}/${idPlayer}`,
    });
    const status = responseStatus;
    const jugadores = sortPlayers(status.jugadores);
    setMatchState(jugadores);
    setPlayerState(status.jugador);

    const responseCards = await httpRequest({
      method: 'GET',
      service: `players/${idPlayer}/${idPartida}`,
    });
    const cards = responseCards.cartas;
    setManoJugador(cards);
  }

  useEffect (() => {
    const url = `ws://localhost:8000/ws/match/${idPartida}/${idPlayer}`;
    const ws = new WebSocket(url);

    ws.onopen = (event) => {
      initializeGame(ws);
    };

    // setWebsocket(ws);
    // recieve message every start page
    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
    };
  
    //clean up function when we close page
    return () => ws.close();
  }, []);


  return (
    <div className={styles.container}>
      {playerState.esTurno && (<div className={styles.tuTurno}/>)}
      <div className={styles.detalleMesa}/>
      <Mazo esTurno={playerState.esTurno} mano={manoJugador} actualizarMano={setManoJugador}/>
      <MazoDescarte mazoDescarteState={mazoDescarteState}/>
      <ManoJugador cartas={manoJugador} esTurno={playerState.esTurno} actualizar={setManoJugador}/>
      <Jugadores jugadores={matchState}/>
    </div>
  );
}

export default Partida;
