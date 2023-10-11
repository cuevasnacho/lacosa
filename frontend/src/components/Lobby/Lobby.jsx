import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { httpRequest } from '../../services/HttpService.js';
import styles from './Lobby.module.css';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';
import React, { useEffect } from 'react';

function Lobby(params) {
  const { ws } = params;      
  
  const esHost = JSON.parse(window.sessionStorage.getItem('Host'));
  const infoPartida = JSON.parse(window.sessionStorage.getItem('Partida'));
  const minJugadores = infoPartida.lobby_min;
  const maxJugadores = infoPartida.lobby_max;

  const { idLobby } = useParams();
  const idPlayer = parseInt(window.sessionStorage.getItem('user_id'));

  const [jugadores, setJugadores] = useState([]);

  async function iniciarPartida () {
    if (minJugadores <= jugadores.length && jugadores.length <= maxJugadores) {
      const response = await httpRequest({
        method: 'PUT',
        service: `partida/iniciar/${idLobby}`,
      });
      
      const match = JSON.parse(response);
      const mensaje = JSON.stringify({action: 'start_match', match_id: match.match_id})
      ws.send(mensaje);
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

    // recieve message every start page
    ws.onmessage = async (e) => {
      const info = JSON.parse(e.data);
      switch (info.action) {
        case 'lobby_players':
          setJugadores(info.data);
          break;

        case 'start_match':
          window.location = `/partida/${info.data}`;
      }
    };

    //clean up function when we close page
    return () => ws.close();
  }, []);

  return(
    <>
      <div className={styles.container}>
        <div className={styles.jugadores}>
          <h1>Jugadores</h1>   
          <h3> {jugadores.length} </h3> 
          <JugadoresLobby jugadores={jugadores}/>
          { esHost && (
          <button className={styles.botonIniciar} type='button' onClick={iniciarPartida}>Iniciar Partida</button>
          )}
        </div>
      </div>
    </>
  );
}    
  
export default Lobby;