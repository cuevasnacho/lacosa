import { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import styles from './Lobby.module.css';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';
import Chat from '../Chat/Chat.jsx';
import BotonAbandonar from '../AbandonarPartida/BotonAbandonar.jsx';
import { ToastContainer, toast } from 'react-toastify';

function Lobby() {
  const esHost = JSON.parse(window.sessionStorage.getItem('Host'));
  const infoPartida = JSON.parse(window.sessionStorage.getItem('Partida'));
  const minJugadores = infoPartida.lobby_min;
  const maxJugadores = infoPartida.lobby_max;

  const { idLobby } = useParams();
  const idPlayer = parseInt(window.sessionStorage.getItem('user_id'));

  const [messages, setMessages] = useState([]);
  const [jugadores, setJugadores] = useState([]);
  const websocket = useRef(null);

  async function iniciarPartida () {
    if (minJugadores <= jugadores.length && jugadores.length <= maxJugadores) {
      const response = await httpRequest({
        method: 'PUT',
        service: `partida/iniciar/${idLobby}`,
      });

      const mensaje = JSON.stringify({action: 'start_match', match_id: response.match_id})
      websocket.current.send(mensaje);
    }
    else {
      toast.error('La cantidad de jugadores no es la permitida', {theme: 'colored'});
    }
  }


  useEffect (() => {
    const url = `ws://localhost:8000/ws/lobbys/${idLobby}/${idPlayer}`;
    const ws = new WebSocket(url);

    ws.onopen = () => {
      const mensaje = JSON.stringify({action: 'lobby_players'});
      ws.send(mensaje);
    };

    // recieve message every start page
    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
      console.log(info.action);
      switch (info.action) {
        case 'lobby_players':
          setJugadores(info.data);
          break;

        case 'start_match':
          console.log(info.data);
          window.location = `/partida/${info.data}`;
          break;

        case 'host_left':
          alert('El host ha abandonado la partida');
          window.location = '/home';
          break;

        case 'player_left':
          setJugadores(info.data);
          break;

        case 'message':
          const message = info.data;
          setMessages((prevMessages) => [...prevMessages, message]);
          break;

        default:
          break;
      }
    };
    
    websocket.current = ws;

    //clean up function when we close page
    return () => ws.close();
  }, []);

    return(
    <>
    <ToastContainer limit={2}/>
      <div className={styles.container}>
        <div className={styles.jugadores}>
          <h1>La partida comenzara pronto</h1>   
          <h4>Hay {jugadores.length} jugadores en el lobby</h4> 
          <JugadoresLobby jugadores={jugadores}/>
          { esHost && (
          <button className={styles.botonIniciar} type='button' onClick={iniciarPartida}>Iniciar Partida</button>
          )}
          <BotonAbandonar idJugador={idPlayer} idLobby={idLobby} websocket={websocket.current}></BotonAbandonar>
        </div>
        <Chat ws={websocket.current} messages={messages} />
      </div>
    </>
  );
}

export default Lobby;
