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
  const username = sessionStorage.getItem('username');
  const [dropdownm, setDropdown] = useState(false);

  function abrirCerrarMenu() {
    setDropdown(!dropdownm);
  }

  async function jugar(target_id, target_username, mano){
    if (mano.length > 4 ) 
    {
      await httpRequest({
        method: 'PUT',
        service: `carta/jugar/${player_id}/${carta.id}/${target_id}`,
      });
      
      const mensaje = JSON.stringify({action: 'play_card', data: 
      {card: carta.cartaNombre ,player: username, target: target_username, tipo: carta.tipo}});
      socket.send(mensaje);
      
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