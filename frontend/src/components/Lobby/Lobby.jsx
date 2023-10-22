import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import styles from './Lobby.module.css';
import React, { useEffect } from 'react';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';
import Chat from '../Chat/Chat.jsx';
import BotonAbandonar from '../AbandonarPartida/BotonAbandonar.jsx';

function Lobby() {
  const esHost = JSON.parse(window.sessionStorage.getItem('Host'));
  const infoPartida = JSON.parse(window.sessionStorage.getItem('Partida'));
  const minJugadores = infoPartida.lobby_min;
  const maxJugadores = infoPartida.lobby_max;

  const { idLobby } = useParams();
  const idPlayer = parseInt(window.sessionStorage.getItem('user_id'));

  const [messages, setMessages] = useState([]);
  const [jugadores, setJugadores] = useState([]);
  const [websocket, setWebsocket] = useState(null);

  async function iniciarPartida () {
    if (minJugadores <= jugadores.length && jugadores.length <= maxJugadores) {
      const response = await httpRequest({
        method: 'PUT',
        service: `partida/iniciar/${idLobby}`,
      });

      const mensaje = JSON.stringify({action: 'start_match', match_id: response.match_id})
      console.log(mensaje);
      websocket.send(mensaje);

    }
    else {
      alert("La cantidad de jugadores no es la permitida");
    }
  }


  useEffect (() => {
    const url = `ws://localhost:8000/ws/lobbys/${idLobby}/${idPlayer}`;
    const ws = new WebSocket(url);

    ws.onopen = (event) => {
      const mensaje = JSON.stringify({action: 'lobby_players'});
      ws.send(mensaje);
    };

    setWebsocket(ws);
    // recieve message every start page
    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'lobby_players':
          setJugadores(info.data);
          //console.log(parseInt(window.localStorage.getItem('new_host_id')))
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
          const message = JSON.parse(e.data).data;
          setMessages([...messages, message]);
          break;
      }
        };

    //clean up function when we close page
    return () => ws.close();
  }, [messages]);

      return(
    <>
      <div className={styles.container}>
        <div className={styles.jugadores}>
          <h1>La partida comenzara pronto</h1>   
          <h4>Hay {jugadores.length} jugadores en el lobby</h4> 
          <JugadoresLobby jugadores={jugadores}/>
          { esHost && (
          <button className={styles.botonIniciar} type='button' onClick={iniciarPartida}>Iniciar Partida</button>
          )}
          <BotonAbandonar idJugador={idPlayer} idLobby={idLobby} websocket={websocket}></BotonAbandonar>
        </div>
        <Chat ws={websocket} messages={messages} />
      </div>
    </>
  );
}

export default Lobby;
