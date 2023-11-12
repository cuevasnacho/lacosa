import styles from "./Jugador.module.css";

function Jugador({cuarentena, username, esTurno, eliminado }) {
    let jugadorClase;
    if (eliminado) jugadorClase = `${styles.jugador} ${styles.eliminado}`;
    else if(cuarentena && esTurno) jugadorClase=`${styles.jugador} ${styles.cuarentenaTurno}`;
    else if (esTurno) jugadorClase = `${styles.jugador} ${styles.turno}`;
    else if(cuarentena) jugadorClase = `${styles.jugador} ${styles.cuarentena}`
    else jugadorClase = styles.jugador;

    return (
        <div className={jugadorClase}>
            <p>{username}</p>
        </div>
    );
}

export default Jugador;
