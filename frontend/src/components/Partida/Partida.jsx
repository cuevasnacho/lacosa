import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import { arrangePlayers } from './functions.jsx';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from './Partida.module.css';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Jugadores from '../Jugador/Jugadores.jsx';
import Mazo from '../Mazo/Mazo.jsx';
import MazoDescarte from '../Mazo/MazoDescarte.jsx';
import Chat from '../Chat/Chat.jsx';
import Finalizar from '../FinalizarPartida/Finalizar.jsx';
import LogPartida from '../LogPartida/LogPartida.jsx';

function Partida () {
  const idPlayer = JSON.parse(sessionStorage.getItem('user_id'));
  const { idPartida } = useParams();
  const [websocket, setWebsocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [jugadas,setJugadas]=useState([])
  const [jugador,setJugador] = useState({})
  const [playerState, setPlayerState] = useState({});
  const [manoJugador, setManoJugador] = useState([]);   // Indica las cartas que tengo en la mano
  const [matchState, setMatchState] = useState([]); // username: string, id: int, esTurno: bool, posicion: int, eliminado: bool	
  const [mazoDescarteState, setMazoDescarteState] = useState(2);  // Dice que carta se va a mostrar en el mazo de descarte
  const [isOver, setIsOver] = useState(false);

  async function getStatus() {
    const responseStatus = await httpRequest({
      method: 'GET',
      service: `partida/status/${idPartida}/${idPlayer}`,
    });
    const status = responseStatus;
    setJugador(status.jugador)
    const jugadores = arrangePlayers(status.jugadores);
    setMatchState(jugadores);
    setPlayerState(status.jugador);
  }

  async function initializeGame() {
    getStatus();

    window.sessionStorage.setItem('match_id', idPartida);

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
      initializeGame();
    };

    setWebsocket(ws);
    //funcion agregada (va guardando el historial completo de jugadas)
    const receiveJugada=(jugada)=>setJugadas((state)=>[...state,jugada])
    let jugada="";
    // recieve message every start page
    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'play_card':
          const tipo_carta_descartada = info.data.tipo ? 1 : 0;
          setMazoDescarteState(tipo_carta_descartada);
          toast(`${info.data.player} jugó la carta ${info.data.card} sobre ${info.data.target}`, {theme: 'dark'});
          jugada = {msj:`${info.data.player} jugó la carta ${info.data.card} sobre ${info.data.target}`}
          receiveJugada(jugada)
          break;

        case 'next_turn':
          getStatus();
          toast(`Finalizo  el turno de ${info.data}`, {theme: 'dark'});
          break;
        
        case 'show_cards':
          const cartas = info.data;
          let mensaje_cartas = "Cartas: ";
          for (let i = 0; i < cartas.length; i++) {
            mensaje_cartas = mensaje_cartas.concat(cartas[i] + ", ");
            console.log(cartas[i]);
          }
          toast(`${mensaje_cartas}`, {theme: 'dark'});
          break;

        case 'message':
          const message = JSON.parse(e.data).data;
          console.log(message)
          setMessages([...messages, message]);
          break;

        case 'notify_defense':
          toast(`Podes defenderte de ${info.data.atacante_username} con ${info.data.card_defense_name}`);
          break;
          
        case 'end_game':
          const respuesta = info.data;
          console.log(respuesta);
          setIsOver(respuesta);
          break;
      }
    };
   
    //clean up function when we close page
    return () => ws.close();
  }, [messages,mazoDescarteState]);

  return (
    <div className={styles.container}>
      {isOver && <Finalizar idpartida = {idPartida} idjugador={idPlayer}/>}
      <ToastContainer />
      {playerState.esTurno && (<div className={styles.tuTurno}/>)}
      <div className={styles.detalleMesa}/>
      <Mazo esTurno={playerState.esTurno} mano={manoJugador} actualizarMano={setManoJugador}/>
      <MazoDescarte mazoDescarteState={mazoDescarteState}/>
      <ManoJugador 
        cartas={manoJugador} 
        esTurno={playerState.esTurno} 
        actualizar={setManoJugador} 
        socket={websocket} 
        jugadores={matchState}/>
      <Jugadores jugadores={matchState} jugador={jugador}/>
      <Chat ws={websocket} messages={messages}/>
      <LogPartida messages={jugadas}></LogPartida>
    </div>
  );
}
export default Partida;
