import { useState } from 'react';
import { useParams } from 'react-router-dom';
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

  function iniciarPartida() {
    if (minJugadores <= jugadores.length && jugadores.length <= maxJugadores) {
      alert("inicie la partida");
      // ws.send();
    }
    else {
      alert("La cantidad de jugadores no es la permitida");
    }
  }
  
  function Menu() {
    /* No hay un endpoint del back para volver al home*/
    alert("Volver al menu principal");
  }

  function mandarMensaje () {
    const mensaje = JSON.stringify({action: 'recibir_mensaje', data: 'Recibi tu mensaje'});
    ws.send(mensaje);
  }

  useEffect(() => {
    const url = `ws://localhost:8000/ws/lobbys/${idLobby}/${idPlayer}`;
    const ws = new WebSocket(url);

    ws.onopen = (event) => {
      ws.send("Connect");
    };

    // recieve message every start page
    ws.onmessage = (e) => {
      const info = JSON.parse(e.data);
      setJugadores(info.data); 
      console.log(esHost);
      console.log(infoPartida);
      console.log(minJugadores);
      console.log(maxJugadores);
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