// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";
//
import puerta from "../../media/designs/puertaAtrancada.svg"
//
function Jugadores({ jugadores,jugador }) {
  console.log(jugadores);
  let left, middle, right;
  const length = jugadores.length;
  if (length < 4) {
    left = {username: 'null', esTurno: false, eliminado: false};
    middle = [{username: 'null', esTurno: false, eliminado: false}];
    right = {username: 'null', esTurno: false, eliminado: false};
  }
  else {
    left = jugadores[0];
    middle = jugadores.slice(1,-2);
    right = jugadores[length-2];
  }

  return (
    <>
      <div className={styles.jugadoresContainer} data-testid="middle">
        {middle.map((jugador, index) => (
          <Jugador key={index} username={jugador.username} esTurno={jugador.esTurno} eliminado={jugador.eliminado}/>
        ))}
      </div>
      <div className={styles.jugadorLeft} data-testid="left">
        <Jugador username={left.username} esTurno={left.esTurno} eliminado={left.eliminado}/>
        {(jugador && !jugador.puerta_izq) && <img className={styles.puertaLeft} src={puerta}></img>}
      </div>
      <div className={styles.jugadorRight} data-testid="right">
        {(jugador && !jugador.puerta_der) && <img className={styles.puertaRight} src={puerta}></img>}
        <Jugador username={right.username} esTurno={right.esTurno} eliminado={right.eliminado}/>
      </div>
    </>
  );
}

export default Jugadores;
