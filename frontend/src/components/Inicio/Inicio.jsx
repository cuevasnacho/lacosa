import { useState } from 'react';
import styles from './Inicio.module.css';
import InicioForm from '../InicioForm/InicioForm';
import Popup from '../Popup/Popup';
import videobg from '../../media/background-video.mp4';

const Inicio = () => {
  const [open, setOpen] = useState(false);
  
  return (
    <>
      <div className={styles.page}>
        <div className={styles.sqcenter}>
          <button onClick={() => setOpen(true)}>Reglas</button>
          {open ? <Popup title="Reglas" text="Just the rules" closePopup={() => setOpen(false)}/> : null}
          <InicioForm />
        </div>
      </div> 
    </>
  )
};

export default Inicio;