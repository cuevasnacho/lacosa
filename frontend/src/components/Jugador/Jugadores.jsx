// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";

function Jugadores({ jugadores }) {
  return (
    <div className={styles.jugadoresContainer}>
      {jugadores.map((jugador, index) => (
        <Jugador key={index} username={jugador.username} esTurno={jugador.esTurno} />
      ))}
    </div>
  );
}

export default Jugadores;
