import { useState } from 'react';
import { useParams } from 'react-router-dom';
import styles from './Lobby.module.css';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';
import React, { useEffect } from 'react';

function Lobby(params) {
    const { ws } = params;      
    const esHost = window.sessionStorage.getItem('Host');
    const {idLobby} = useParams();

    const [jugadores, setJugadores] = useState([]);

    function Menu() {
        /* No hay un endpoint del back para volver al home*/
        alert("Volver al menu principal");
    }

    function mandarMensaje () {
        const mensaje = JSON.stringify({action: 'recibir_mensaje', data: 'Recibi tu mensaje'});
        ws.send(mensaje);
    }

    useEffect(() => {
        const url = `ws://localhost:8000/ws/lobbys/${idLobby}`;
        const ws = new WebSocket(url);
    
        ws.onopen = (event) => {
          ws.send("Connect");
        };
    
        // recieve message every start page
        ws.onmessage = (e) => {
            const info = JSON.parse(e.data);
            setJugadores(info.data); 
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
                </div>
            </div>
        </>
    );
}    
    
export default Lobby;