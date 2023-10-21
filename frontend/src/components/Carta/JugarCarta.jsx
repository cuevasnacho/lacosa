import { httpRequest } from "../../services/HttpService";
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import {Dropdown, DropdownItem, DropdownMenu, DropdownToggle} from 'reactstrap';
import { descartarCarta } from "./DescartarCarta";
import styles from './JugarCarta.module.css'
import MostrarCarta from '../MostrarCarta/MostrarCarta'

function JugarCarta({carta, socket, jugadores, funcionDescartar, mano}) {
  
  const player_id = JSON.parse(sessionStorage.getItem('user_id'));
  const username = window.sessionStorage.getItem('username');
  const [dropdownm, setDropdown] = useState(false);

  function abrirCerrarMenu() {
    setDropdown(!dropdownm);
  }

  async function jugar(target_id, target_username, mano){
    if (mano.length > 4 ) 
    {
      const response = await httpRequest({
        method: 'PUT',
        service: `carta/jugar/${player_id}/${carta.id}/${target_id}`,
      });
      
      // response[0] es el jugador que jugo la carta
      // response[1] es el jugador al que le juegan la carta
      const cartas_mostrar = response[0].card_name;
      const mensaje = JSON.stringify({
        action: 'play_card',
        data: {
          card: carta.cartaNombre,
          player: username, 
          target: target_username, 
          tipo: carta.tipo,
        }});
  
      const mensaje_cartas = JSON.stringify({
        action: 'show_cards',
        data: {
          card: carta.cartaNombre,
          mostrar: cartas_mostrar
        }
      })

      socket.send(mensaje);
      socket.send(mensaje_cartas);

      const se_puede_defender = response[1].player_defense;
      const defensor_id = response[1].player_id;
      const card_used_name = carta.cartaNombre;
      const card_defense_name = response[1].card_name[0];

      if (se_puede_defender) {
        const notify_defense = JSON.stringify({action: 'notify_defense', 
                                              data: 
                                              {defensor_id: defensor_id,
                                              card_used_name: card_used_name,
                                              atacante_id: player_id,
                                              atacante_username: username,
                                              card_defense_name: card_defense_name}});
                                    
        socket.send(notify_defense);
      }

      
      
      descartarCarta(funcionDescartar, mano, carta, socket);
      
      return(
        <>
        <MostrarCarta nombreCarta={carta.cartaNombre} />
        </>
      );
    }
    else
    {
      toast.error("Primero tenes que robar una carta", {theme: "colored"})
    
    }
  }
  
  return(
    <>
    <ToastContainer />
    <div className={styles.boton}>
      <Dropdown isOpen={dropdownm} toggle={abrirCerrarMenu} direction="up">
        <DropdownToggle caret>
          Jugar Carta
        </DropdownToggle>
        <DropdownMenu dark>
          {jugadores.map((jugador, index) => (
            <DropdownItem
              key={index}
              onClick={() => jugar(jugador.id, jugador.username, mano)}>
              {jugador.username} {jugador.id}
            </DropdownItem>
          ))}
        </DropdownMenu>
      </Dropdown>
    </div>
    </>
  );
}


export default JugarCarta;