import styles from "./Jugador.module.css";

function Jugador({ username, esTurno }) {
    const jugadorClase = esTurno ? `${styles.jugador} ${styles.turno}` : styles.jugador;

    return (
        <div className={jugadorClase}>
            <p>{username}</p>
        </div>
    );
}

export default Jugador;
