/*Implementar botón que le permita al usuario abandonar el lobby en el que se encuentra y
volver a la pantalla principal (/home) con la lista de partidas. Cuando el jugador
clickee en el botón, saltar una alerta para que confirme o cancele su decisión.
Enviar al back:
idJugador*/
import styles from "./BotonAbandonar.module.css"
import { httpRequest } from '../../services/HttpService.js'

export default function BotonAbandonar({idJugador,idLobby,websocket}) {
    const abandonarLobby = async () => {
      try {
          const mensaje = JSON.stringify({action: 'abandonar_lobby', data: idJugador});
          websocket.send(mensaje);
          await httpRequest({
            method: 'POST',
            service: `lobbys/${idLobby}/${idJugador}`
          });
          window.location="/home";
        } catch (error) {
          console.log(error);
        }
      };
  return (
    <button onClick={abandonarLobby} className={styles.terror}>Abandonar</button>
  )
}
