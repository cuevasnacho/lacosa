import CustomButton from '../Boton/CustomButton.jsx'
import { useParams } from 'react-router-dom';
import styles from './Lobby.module.css';
import { httpRequest } from '../../services/HttpService.js';
import JugadoresLobby from '../Lobby/JugadoresLobby.jsx';

function Lobby() {
    const {idLobby} = useParams();

    const esHost = window.localStorage.getItem('Host');
    //const esHost = true;

    function Menu() {
        /* No hay un endpoint del back para volver al home*/
        alert("Volver al menu principal");
    }

    const refrescar = async () => {
        try {
          const response = await httpRequest({
            method: 'GET',
            service: `lobbys/${lobby_id}/refrescar`,
          });
          
          window.localStorage.setItem('cantidadJugadores', response.lobby_pcount);

          window.localStorage.setItem(JSON.stringify('jugadores', response.lobby_names));
          
          window.location.reload();
    
        } catch (error) {
          console.log(error);
        }
    };

    function IniciarPartida(idLobby) {
        const cantidadJugadores = parseInt(window.localStorage.getItem('cantidadJugadores'));  
        const cantidadMinima = parseInt(window.localStorage.getItem('minPlayers'));
        
        if (cantidadMinima <= cantidadJugadores) 
        {
            alert("Partida iniciada");

            try 
            {
                const response = httpRequest({
                    method: 'PUT',
                    service: 'partida/iniciar/' + idLobby,
                });
                const idPartida = JSON.stringify(response.match_id);
                
                window.location = '/partida/' + idPartida;
            } 
            catch (error) 
            {
                console.log(error);                
            }
        }  
        else 
        {
            alert("No se puede iniciar la partida, faltan jugadores");
        }
    }

    return(
        <>
            <div className={styles.container}>
                <div className={styles.jugadores}>
                    <h1>Jugadores</h1>   
                    <h3> {window.localStorage.getItem('cantidadJugadores')} </h3> 
                    <JugadoresLobby jugadores={JSON.parse(window.localStorage.getItem('jugadores'))}/>
                </div>
                
                <div className={styles.botones}>
                    <CustomButton label="Volver al menu principal" onClick={Menu} />
                    {esHost && <CustomButton label="Iniciar Partida" onClick={() => IniciarPartida(idLobby)} />}
                    <CustomButton label="Refrescar" onClick={() => refrescar()} />
                </div>
            </div>
        </>
    );
}    
    
export default Lobby;