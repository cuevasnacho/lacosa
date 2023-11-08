import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'reactstrap';
import { descartarCarta } from "./DescartarCarta";
import { playCard, getHand } from '../Partida/functions.jsx';
import styles from './JugarCarta.module.css';

function JugarCarta({carta, socket, jugadores, actualizar, mano}) {
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
      console.log("se hizo play card");
      
      setTimeout(() => {
        getHand(actualizar);
      }, 100);

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