import { useState } from 'react';
import styles from './Inicio.module.css';
import InicioForm from '../InicioForm/InicioForm';
import Popup from '../Popup/Popup';
import videobg from '../../media/videobg.mp4';
import logo from '../../media/designs/logo.png';

const Inicio = () => {
  const [open, setOpen] = useState(false);

  const rules = "Al comienzo del juego, todos los jugadores son humanos, excepto el que recibe la carta de 'La Cosa' en la primera ronda.\nA partir de ese momento, ese jugador asume el papel de La Cosa y no puede descartar ni intercambiar esta carta.\nA) Los Humanos:\nSu objetivo es trabajar juntos para identificar qué jugador es La Cosa y asarlo con una carta de 'Lanzallamas'.\nB) La Cosa y los Infectados.\nUn Humano se convertirá en La Cosa en el primer turno. Su objetivo es destruir a todos los Humanos, convirtiéndolos en aliados Infectados o eliminándolos de la partida.";

  return (
    <>
      <div className={styles.page}>
        <div className={styles.sqcenter}>
          <div className={styles.leftsq}>
            <img src={logo} alt="logolacosa" width={200}/>
            <button onClick={() => setOpen(true)}>Reglas</button>
          </div>
          {open ? 
          <Popup 
            title="Reglas" 
            text={rules} 
            closePopup={() => setOpen(false)}
          /> : null}
          <InicioForm />
        </div>
      </div> 
      <video src={videobg} type="video/mp4" autoPlay loop muted />
    </>
  )
};

export default Inicio;