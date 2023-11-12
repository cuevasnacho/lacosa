import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import { arrangePlayers, nextTurn, getHand, intercambiarDefensa } from './functions.jsx';
import { Flip, ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from './Partida.module.css';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';
import Jugadores from '../Jugador/Jugadores.jsx';
import Mazo from '../Mazo/Mazo.jsx';
import MazoDescarte from '../Mazo/MazoDescarte.jsx';
import Chat from '../Chat/Chat.jsx';
import Finalizar from '../FinalizarPartida/Finalizar.jsx';
import LogPartida from '../LogPartida/LogPartida.jsx';
import Defensa from '../Carta/Defensa.jsx';

function Partida () {
  const idPlayer = JSON.parse(sessionStorage.getItem('user_id'));
  const username = window.sessionStorage.getItem('username');
  const { idPartida } = useParams();
  const websocket = useRef(null);
  const [messages, setMessages] = useState([]);
  const [jugadas,setJugadas]=useState([])
  const [jugador,setJugador] = useState({})
  const [stage, setStage] = useState(0);
  const [playerState, setPlayerState] = useState({});
  const [isLaCosa, setIsLaCosa] = useState(false);
  const [socketData, setSocketData] = useState({});
  const [manoJugador, setManoJugador] = useState([]);   // Indica las cartas que tengo en la mano
  const [matchState, setMatchState] = useState([]); // username: string, id: int, esTurno: bool, posicion: int, eliminado: bool	
  const [mazoDescarteState, setMazoDescarteState] = useState(2);  // Dice que carta se va a mostrar en el mazo de descarte
  const [isOver, setIsOver] = useState(false);
  const [defenseData, setDefenseData] = useState(null);

  async function getStatus() {
    const responseStatus = await httpRequest({
      method: 'GET',
      service: `partida/status/${idPartida}/${idPlayer}`,
    });
    const status = responseStatus;
    setJugador(status.jugador)
    console.log({status})
    const jugadores = arrangePlayers(status.jugadores);
    setMatchState(jugadores);
    setPlayerState(status.jugador);
    getHand(setManoJugador);
  }

  async function initializeGame() {
    getStatus();
    window.sessionStorage.setItem('match_id', idPartida);
    const cards = await getHand(setManoJugador);
    setIsLaCosa(cards.some(card => card.cartaNombre === 'lacosa'));
  }

  function toastStage(text) {
    toast(text, {
      position: toast.POSITION.TOP_LEFT, theme: 'dark'
    })
  }

  function declarar() {
    websocket.current.send(JSON.stringify({action: 'end_game', data: true}))
  }
  
  useEffect (() => {
    const url_pasivo = `ws://localhost:8000/ws/match/pasivo/${idPartida}/${idPlayer}`;
    const ws = new WebSocket(url_pasivo);

    ws.onopen = () => {
      initializeGame();
      websocket.current = ws;
    };

    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'message':
          const message = info.data;
          setMessages((prevMessages) => [...prevMessages, message]);
          break;

        case 'end_game':
          const respuesta = info.data;
          setIsOver(respuesta);
          break;

        case 'play_card':
          const tipo_carta_descartada = info.data.tipo ? 1 : 0;
          setMazoDescarteState(tipo_carta_descartada);
          getStatus();

          const jugada = `${info.data.player} jugó la carta ${info.data.card} sobre ${info.data.target}`;
          toast(jugada, {theme: 'dark'});
          setJugadas((prevJugadas) => [...prevJugadas, {msj: jugada}]);
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
          }
          toast(`${mensaje_cartas}`, {theme: 'dark'});
          setJugadas((prevJugadas) => [...prevJugadas, {msj: mensaje_cartas}]);
          break;

      }
    };

  return () => {ws.close();}
  }, []);

  useEffect (() => {
    const url_activo = `ws://localhost:8000/ws/match/activo/${idPartida}/${idPlayer}`;
    const ws_activo = new WebSocket(url_activo);

    // recieve message every start page
    ws_activo.onmessage = (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'iniciar_turno':
          toastStage('Es tu turno!');
          setStage(1);
          getStatus();
          break;

        case 'forzar_jugada':
          toastStage(info.action);
          setStage(2);
          break;

        case 'elegir_jugada':
          toastStage('Jugá o descartá una carta');
          setStage(3);
          break;

        case 'iniciar_defensa':
          toastStage('Podés defenderte');
          setStage(4);
          setDefenseData(info.data);
          getStatus();
          break;

        case 'iniciar_intercambio':
          toastStage('Intercambiá una carta');
          setSocketData(info.data);
          setStage(5);
          getStatus();
          break;

        case 'sol_intercambio':
          toastStage('Intercambiá una carta');
          setSocketData(info.data);
          const oponent_id = parseInt(info.data.oponent_id);
          const card_id = parseInt(info.data.card_id);
          setStage(6);

          intercambiarDefensa(oponent_id, card_id)
            .then(canDefend => {
              if (canDefend) {
                // proceso de defensa
              }
              else {
                setStage(7);
              }
            });
          getStatus();
          break;
        
        case 'fin_turno':
          toastStage('Finalizo tu turno');
          setStage(0);
          nextTurn(idPartida, websocket.current, username);
          break;

        case 'cuarentena':
          toastStage('Estás en cuarentena');
          break;
      }
    };
   
    // clean up function when we close page
    return () => {ws_activo.close();}
  }, []);

  return (
    <div className={styles.container}>
      {isOver && <Finalizar idpartida = {idPartida} idjugador={idPlayer}/>}
      <ToastContainer limit={5} pauseOnFocusLoss={false} hideProgressBar autoClose={3000} pauseOnHover={false} transition={Flip}/>
      {stage == 4 && <Defensa 
        dataSocket={defenseData} 
        manoJugador={manoJugador}
        setStage={setStage}
        setManoJugador={setManoJugador}
        socket={websocket.current}
        setJugadas={setJugadas}/>}
      {playerState.esTurno && (<div className={styles.tuTurno}/>)}
      <div className={styles.detalleMesa}>
        { isLaCosa && 
        (<button 
          type='button' 
          onClick={declarar}
          className={styles.botonDeclarar}>
            Declarar
        </button>
        )}
      </div>
      <Mazo stage={stage} mano={manoJugador} actualizarMano={setManoJugador}/>
      <MazoDescarte mazoDescarteState={mazoDescarteState}/>
      <ManoJugador 
        cartas={manoJugador} 
        stage={stage}
        actstage={setStage}
        data={socketData}
        actualizar={setManoJugador} 
        socket={websocket.current} 
        jugadores={matchState}/>
      <Jugadores jugadores={matchState} jugador={jugador}/>
      <Chat ws={websocket.current} messages={messages}/>
      <LogPartida messages={jugadas}></LogPartida>
    </div>
  );
}
export default Partida;
