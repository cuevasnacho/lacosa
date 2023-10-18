/*Implementar botón que le permita al usuario abandonar el lobby en el que se encuentra y
volver a la pantalla principal (/home) con la lista de partidas. Cuando el jugador
clickee en el botón, saltar una alerta para que confirme o cancele su decisión.
Enviar al back:
idJugador*/
import styles from "./BotonAbandonar.module.css"
import swal from 'sweetalert'//paquete para estilos de alertas
import { httpRequest } from '../../services/HttpService.js'

export default function BotonAbandonar({idJugador,idLobby}) {
    const handleClick= ()=>{
        const AbandonarLobby= async () => {
            try {
                const data = await httpRequest({
                  method: 'POST',
                  service: `lobbys/${idLobby}/${idJugador}`
              });
                window.localStorage.setItem("new_host_id", data.new_host_id);
                window.sessionStorage.setItem('Host', false);
                window.location="/home"
              } catch (error) {
                swal({
                  title:"No se ha podido Abandonar el lobby",
                  icon:"error",
                })
                }
            };
        swal({
            title:"¿Seguro que quieres abandonar el lobby?",
            buttons:["No","Si"],

        }).then(respuesta=>{
            if(respuesta){
                AbandonarLobby()
            }
        })
    }
  return (
    <button onClick={handleClick} className={styles.terror}>Abandonar</button>
  )
}
