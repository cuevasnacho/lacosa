import styles from "./JugadoresLobby.module.css";
import Person from '@mui/icons-material/Person'

function Jugadores({ jugadores }) {
  return (
    <div className={styles.jugadoresContainer}>
      {jugadores.map((jugador, index) => (
        <div key={index} className={styles.jugadorContainer}>
          <div className={styles.jugador}>
            <Person fontSize="large" style={{ color: 'black' }} />
          </div>
          <p className={styles.jugadorNombre}>
            {jugador}
          </p>
        </div>
      ))}
    </div>
  );
}

export default Jugadores;
