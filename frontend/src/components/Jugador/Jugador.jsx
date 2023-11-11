import styles from "./Jugador.module.css";
import Person from '@mui/icons-material/Person'

function Jugador({ username, esTurno, eliminado }) {
    let jugadorClase;
    if (eliminado) jugadorClase = `${styles.jugador} ${styles.eliminado}`;
    else if (esTurno) jugadorClase = `${styles.jugador} ${styles.turno}`;
    else jugadorClase = styles.jugador;

    return (
        <div className={styles.container}>
            <div className={jugadorClase}>
                <Person fontSize="large" style={{ color: 'white' }} />
            </div>
            <p className={styles.nombre}> 
                {username}
            </p>
        </div>
    );
}

export default Jugador;
