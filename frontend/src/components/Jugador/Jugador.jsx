import styles from "./Jugador.module.css";

function Jugador({ username, esTurno, eliminado }) {
    let jugadorClase;
    if (eliminado) jugadorClase = `${styles.jugador} ${styles.eliminado}`;
    else if (esTurno) jugadorClase = `${styles.jugador} ${styles.turno}`;
    else jugadorClase = styles.jugador;

    return (
        <div className={jugadorClase}>
            <p>{username}</p>
        </div>
    );
}

export default Jugador;
