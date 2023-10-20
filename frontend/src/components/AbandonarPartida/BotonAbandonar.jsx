/*Implementar botón que le permita al usuario abandonar el lobby en el que se encuentra y
volver a la pantalla principal (/home) con la lista de partidas. Cuando el jugador
clickee en el botón, saltar una alerta para que confirme o cancele su decisión.
Enviar al back:
idJugador*/
import styles from "./BotonAbandonar.module.css"
import swal from 'sweetalert'//paquete para estilos de alertas
import { httpRequest } from '../../services/HttpService.js'

export default function BotonAbandonar({idJugador,idLobby,websocket}) {
    const handleClick= ()=>{
        const AbandonarLobby= async () => {
            try {
                const mensaje = JSON.stringify({action: 'abandonar_lobby', data: idJugador});
                websocket.send(mensaje);
                const data = await httpRequest({
                  method: 'POST',
                  service: `lobbys/${idLobby}/${idJugador}`
                });
                //alert("Se envió el mensaje por socket");
                //window.sessionStorage.setItem('Host', false);
                window.location="/home"
              } catch (error) {
                  console.log(error);
                // swal({
                  //   title:"No se ha podido Abandonar el lobby",
                  //   icon:"error",
                  // })
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