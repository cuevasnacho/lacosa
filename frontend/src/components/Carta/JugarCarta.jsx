import { httpRequest } from "../../services/HttpService";
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import {Dropdown, DropdownItem, DropdownMenu, DropdownToggle} from 'reactstrap';
import { descartarCarta } from "./DescartarCarta";
import styles from './JugarCarta.module.css'

function JugarCarta({carta, ws, jugadores}) {
  
  const player_id = JSON.parse(sessionStorage.getItem('user_id'));
  const [dropdownm, setDropdown] = useState(false);

  function abrirCerrarMenu() {
    setDropdown(!dropdownm);
  }

  async function jugar(target_id){
    
    await httpRequest({
      method: 'PUT',
      service: `carta/jugar/${player_id}/${carta.id}/${target_id}`,
    });

    ws.send({action: 'play_card', data: {card: carta.cartaNombre ,player: player_id, target: target_id}});
  }
  
  return(
    <div className={styles.boton}>
    <Dropdown isOpen={dropdownm} toggle={abrirCerrarMenu} direction="up">
    <DropdownToggle caret>
      Jugar Carta
    </DropdownToggle>
      <DropdownMenu dark>
        { jugadores.map((jugador, index) => (
          <DropdownItem 
                        key={index} 
                        onClick={() => jugar(jugador.id)}>
                        {jugador.username} {jugador.id}
          </DropdownItem>
          ))}
      </DropdownMenu>
    </Dropdown>
    </div>
  );
}
/*

  const datos ={
    action:'jugar_carta',
    data:
    {
      carta_id:carta.id,
      target_id:target
    } 
    }  
      const data = JSON.stringify(datos);
      ws.send(data);
  */

export default JugarCarta;