// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";

function Jugadores({ jugadores }) {
  const left = jugadores[0];
  const right = jugadores[jugadores.length-1];
  const middle = jugadores.slice(1,-1);

  return (
    <>
      <div className={styles.jugadoresContainer}>
        {middle.map((jugador, index) => (
          <Jugador key={index} username={jugador.username} esTurno={jugador.esTurno} />
        ))}
      </div>
      <div className={styles.jugadorLeft}>
        <Jugador username={left.username} esTurno={left.esTurno}/>
      </div>
      <div className={styles.jugadorRight}>
        <Jugador username={right.username} esTurno={right.esTurno}/>
      </div>
    </>
  );
}

export default Jugadores;
