import CustomButton from '../Boton/CustomButton.jsx'
import { useParams, useNavigate} from 'react-router-dom';
import styles from './Lobby.module.css';
import { httpRequest } from '../../services/HttpService.js';

function Lobby() {
    const navigate = useNavigate();
    const {idLobby} = useParams(); /* idLobby === idPartida */ 

    const esHost = window.localStorage.getItem('Host');
    //const esHost = true;

    function Menu() {
        /* No hay un endpoint del back para volver al home*/
        alert("Volver al menu principal");
        navigate('/home');
    }

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
                
                navigate('/partida/' + idLobby);
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

    async function refrescar() {
        const refresco = await httpRequest({
            method: 'POST',
            service: 'lobby/' + idLobby + '/refrescar',
            body: idLobby
        });
        window.localStorage.setItem('jugadores', JSON.stringify(refresco.players));
        window.localStorage.setItem('cantidadJugadores', JSON.stringify(refresco.lobby_pcount));
    }
    
    return(
        <>
            <div className={styles.container}>
                <div className={styles.jugadores}>
                    <h1>Jugadores</h1>   
                    <h3> {window.localStorage.getItem('cantidadJugadores')} </h3> 
                </div>
                
                <div className={styles.botones}>
                    <CustomButton label="Volver al menu principal" onClick={Menu} />
                    {esHost && <CustomButton label="Iniciar Partida" onClick={() => IniciarPartida(idLobby)} />}
                    <CustomButton label="Refrescar" onClick={refrescar} />
                </div>

            </div>
        </>
    );
}    
    
export default Lobby;