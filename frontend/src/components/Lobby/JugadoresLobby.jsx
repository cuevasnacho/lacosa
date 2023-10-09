import styles from "./JugadoresLobby.module.css";

function Jugadores({ jugadores }) {
  return (
    <>
    <div className={styles.jugadoresContainer}>
      {jugadores.map((jugador, index) => (
        <div className={styles.jugador}>
            <p>{jugador}</p>
        </div>
      ))}
    </div>
    </>
  );
}

export default Jugadores;
