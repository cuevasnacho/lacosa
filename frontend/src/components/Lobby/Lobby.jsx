import { useState } from 'react';
import { useParams } from 'react-router-dom';
import styles from './Lobby.module.css';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';
import React, { useEffect } from 'react';

function Lobby(params) {
    const { ws } = params;      
    const esHost = window.sessionStorage.getItem('Host');

    const [jugadores, setJugadores] = useState([]);

    function Menu() {
        /* No hay un endpoint del back para volver al home*/
        alert("Volver al menu principal");
    }

    ws.onmessage = function (event) {
        const info = JSON.parse(event.data);
        console.log(event);
        console.log(info);
        console.log(info.action);
        console.log(info.data);
        
        switch (info.action) {
            case 'lobby_players':
                setJugadores(info.data); 
                return;
            default:
                return;
        }
    }

    function mandarMensaje () {
        const mensaje = JSON.stringify({action: 'recibir_mensaje', data: 'Recibi tu mensaje'});
        ws.send(mensaje);
    }

    useEffect(() => {
        mandarMensaje();
      }, []); // El segundo argumento vacío [] asegura que se ejecute solo una vez al montar el componente
    
    
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