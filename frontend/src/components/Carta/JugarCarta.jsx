import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { httpRequest } from "../../services/HttpService";
import { ToastContainer, toast } from 'react-toastify';
import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'reactstrap';
import { playCard, getHand } from '../Partida/functions.jsx';
import styles from './JugarCarta.module.css';

function JugarCarta({carta, socket, jugadores, actualizar, mano, stage, actstage, data}) {
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
      
      setTimeout(() => {
        getHand(actualizar);
      }, 100);

    }
    else
    {
      toast.error("Primero tenes que robar una carta", {theme: "colored"})
    }
  }

  async function intercambiar(oponent_id) {
    const player_id = JSON.parse(window.sessionStorage.getItem('user_id'));
    const response = await httpRequest({
      method: 'GET',
      service: `intercambio/valido/${player_id}/${oponent_id}/${carta.id}/${data.motive}`,
      headers: {Accept: '*/*',}
    });
    console.log(response);
    if (response) {
      actstage(0);
    }
  }
  
  return(
    <>
    <ToastContainer />
    <div className={styles.boton}>
      {(stage == 2 || stage == 3) && (
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
      {(stage == 5) && (
        <Dropdown isOpen={dropdownm} toggle={abrirCerrarMenu} direction="up">
          <DropdownToggle caret>
            Intercambiar
          </DropdownToggle>
          <DropdownMenu dark>
            {jugadores.map((jugador, index) => (
              <DropdownItem
                key={index}
                onClick={() => intercambiar(jugador.id)}>
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