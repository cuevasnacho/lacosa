import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'reactstrap';
import { playCard, getHand } from '../Partida/functions.jsx';
import styles from './JugarCarta.module.css';

function JugarCarta({carta, socket, jugadores, actualizar, mano, stage}) {
  const [dropdownm, setDropdown] = useState(false);
  const esJugar = (stage == 2 || stage == 3);
  const esIntercambio = stage == 5;

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

  async function intercambiar() {
    alert('intercambio');
  }
  
  return(
    <>
    <ToastContainer />
    <div className={styles.boton}>
      {( esJugar &&
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
      )}
      {( esIntercambio &&
        <Dropdown isOpen={dropdownm} toggle={abrirCerrarMenu} direction="up">
          <DropdownToggle caret>
            Intercambiar
          </DropdownToggle>
          <DropdownMenu dark>
            {jugadores.map((jugador, index) => (
              <DropdownItem
                key={index}
                onClick={() => intercambiar()}>
                {jugador.username}
              </DropdownItem>
            ))}
          </DropdownMenu>
        </Dropdown>
      )}
    </div>
    </>
  );
}


export default JugarCarta;