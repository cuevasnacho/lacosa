import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'reactstrap';
import { descartarCarta } from "./DescartarCarta";
import { playCard } from '../Partida/functions.jsx';
import styles from './JugarCarta.module.css';

function JugarCarta({carta, socket, jugadores, funcionDescartar, mano}) {
  const username = window.sessionStorage.getItem('username');
  const [dropdownm, setDropdown] = useState(false);

  function abrirCerrarMenu() {
    setDropdown(!dropdownm);
  }

  async function jugar(target_id, target_username, mano){
    if (mano.length > 4 ) 
    {
      const target = {
        target_id: target_id,
        target_username: target_username,
      }
      playCard(carta, target, socket);
      
      const se_puede_defender = response[1].player_defense;
      const defensor_id = response[1].player_id;
      const card_used_name = carta.cartaNombre;
      const card_defense_name = response[1].card_name[0];

      if (se_puede_defender) {
        const notify_defense = JSON.stringify({action: 'notify_defense', 
                                              data: 
                                              {defensor_id: defensor_id,
                                              attack_card_name: card_used_name,
                                              atacante_id: player_id,
                                              atacante_username: username,
                                              card_defense_name: card_defense_name}});
                                    
        socket.send(notify_defense);
      }

      const mensaje_no_defense = JSON.stringify({action: 'no_defense', 
                                                data: {defensor_id: defensor_id, 
                                                  attack_card_name: carta.cartaNombre}});
      socket.send(mensaje_no_defense);
      
      const isover = response[0].end_game;
      console.log(isover);
      const mensaje_isover = JSON.stringify({
        action : 'end_game',
        data : isover
      });

      descartarCarta(funcionDescartar, mano, carta, socket);
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
              {jugador.username}
            </DropdownItem>
          ))}
        </DropdownMenu>
      </Dropdown>
    </div>
    </>
  );
}


export default JugarCarta;