// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";

function mod(i, n) {
  return ((i % n) + n) % n;
}

function Jugadores({ jugadores }) {
  const user_id = parseInt(window.sessionStorage.getItem('user_id'));
  const user_obj = jugadores.find(jugador => jugador.id === user_id);
  const user_pos = user_obj.posicion;
  
  let left,right,middle;
  if (jugadores.length >= 3){
    const middleLeft = jugadores.slice(0,mod(user_pos-1, jugadores.length));
    const middleRight = jugadores.slice(mod(user_pos+2, jugadores.length));
    left = jugadores[mod(user_pos-1, jugadores.length)];
    right = jugadores[mod(user_pos+1, jugadores.length)];
    middle = middleLeft.concat(middleRight.reverse());
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
