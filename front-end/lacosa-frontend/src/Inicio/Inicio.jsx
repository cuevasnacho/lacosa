import { useState } from 'react';
import styles from './Inicio.module.css';
import InicioForm from '../InicioForm/InicioForm';
import Popup from '../Popup/Popup';

const onCreateUser = (data) => {
  if(data.user == '') {
    return (
      alert("Please enter a username!")
    );
  }
  else {
    return (
      alert(`${data.user}`)
    );
  }
}

const Inicio = () => {
  const [open, setOpen] = useState(false);
  
  return (
    <>
      <div className={styles.page}>
        <div className={styles.sqcenter}>
          <button onClick={() => setOpen(true)}>Reglas</button>
          {open ? <Popup title="Reglas" text="These are the rules" closePopup={() => setOpen(false)}/> : null}
          <InicioForm onCreateUser={onCreateUser} />
        </div>
      </div> 
    </>
  )
};

export default Inicio;