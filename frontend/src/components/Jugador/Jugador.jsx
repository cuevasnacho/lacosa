import styles from "./Jugador.module.css";
import Person from '@mui/icons-material/Person'
import PersonOff from '@mui/icons-material/PersonOff'

function Jugador({cuarentena, username, esTurno, eliminado }) {
    let jugadorClase;
    if (eliminado) jugadorClase = `${styles.jugador} ${styles.eliminado}`;
    else if(cuarentena && esTurno) jugadorClase=`${styles.jugador} ${styles.cuarentenaTurno}`;
    else if (esTurno) jugadorClase = `${styles.jugador} ${styles.turno}`;
    else if(cuarentena) jugadorClase = `${styles.jugador} ${styles.cuarentena}`
    else jugadorClase = styles.jugador;

    return (
        <div className={styles.container}>
            <div className={jugadorClase}>
                {eliminado && <PersonOff fontSize="large" style={{ color: 'white' }} />}
                {!eliminado && <Person fontSize="large" style={{ color: 'white' }} />}
            </div>
            <p className={styles.nombre}> 
                {username}
            </p>
        </div>
    );
}

export default Jugador;
