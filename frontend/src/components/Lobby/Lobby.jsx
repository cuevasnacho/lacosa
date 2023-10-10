import { useState, useEffect } from 'react';
import styles from './Lobby.module.css';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';

function Lobby() {
    const esHost = window.sessionStorage.getItem('Host');
    const partida = JSON.parse(window.sessionStorage.getItem('Partida'));
    const minJugadores = parseInt(partida.lobby_min);
    const maxJugadores = parseInt(partida.lobby_max);

    const [jugadores, setJugadores] = useState([]);

    const menu = () => {
        /* No hay un endpoint del back para volver al home*/
        alert("Volver al menu principal");
    }

    const iniciarPartida = () => {
        if (minJugadores <= jugadores.length && jugadores.length <= maxJugadores) {
            const mensaje = JSON.stringify({action: 'iniciar_partida', data: 'Iniciar'});
            ws.send(mensaje);
        }
        else {
            alert("La cantidad de jugadores no es valida para comenzar la partida");
        }
    }

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/ws/lobbys/${idLobby}/refrescar`);

        ws.onmessage = (event) => {
          console.log("Received:", event.data);
          const data = JSON.parse(event.data);
          
          switch (data.action) {
            case 'lobby_players':
                setJugadores(data.players_names);
                break;
            default:
                break;
          }
        };
    
        return () => {
          ws.close();
        };
    }, []);
    
    return(
        <>
            <div className={styles.container}>
                <div className={styles.jugadores}>
                    <h1>Jugadores</h1>   
                    <h3> {jugadores.length} </h3> 
                    <JugadoresLobby jugadores={jugadores}/>
                    {esHost && (
                        <button className={styles.botonIniciar} type='button' onClick={iniciarPartida}>Iniciar Partida</button>
                    )}
                </div>
            </div>
        </>
    );
}    
    
export default Lobby;
