import styles from './Mazo.module.css';
import {robarCarta} from './RobarCarta'

function Mazo ({esTurno, mano, actualizarMano}) {
  
  const mazoState = esTurno ? `${styles.mazo} ${styles.mazoTurno}` : styles.mazo;

  const handleRobarCarta = () => {
    if (mano.length <= 4) {
      robarCarta(mano, actualizarMano);
    }
    else {
      alert("No se puede robar mas cartas");
    }
  };

  return (
    <button 
      className={mazoState} 
      type='button' 
      onClick={handleRobarCarta} />
  );
}

export default Mazo;