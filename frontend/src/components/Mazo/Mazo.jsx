import styles from './Mazo.module.css';

function Mazo ({esTurno}) {
  const levantarCarta = function () {
    alert("levante una carta");
  };
  
  const mazoState = esTurno ? `${styles.mazo} ${styles.mazoTurno}` : styles.mazo;

  return (
    <button 
      className={mazoState} 
      type='button' 
      onClick={levantarCarta} />
  );
}

export default Mazo;