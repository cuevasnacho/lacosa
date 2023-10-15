// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";

function Jugadores({ jugadores }) {
  let left,right,middle;
  if (jugadores.length >= 3){
    left = jugadores[0];
    right = jugadores[jugadores.length-1];
    middle = jugadores.slice(1,-1);
  }
  else{
    left = {username: 'null', esTurno: false, eliminado: false};
    right = {username: 'null', esTurno: false, eliminado: false};
    middle = [{username: 'null', esTurno: false, eliminado: false}];
  }
  return (
    <>
      <div className={styles.jugadoresContainer}>
        {middle.map((jugador, index) => (
          <Jugador key={index} username={jugador.username} esTurno={jugador.esTurno} eliminado={jugador.eliminado}/>
        ))}
      </div>
      <div className={styles.jugadorLeft}>
        <Jugador username={left.username} esTurno={left.esTurno} eliminado={left.eliminado}/>
      </div>
      <div className={styles.jugadorRight}>
        <Jugador username={right.username} esTurno={right.esTurno} eliminado={right.eliminado}/>
      </div>
    </>
  );
}

export default Jugadores;
