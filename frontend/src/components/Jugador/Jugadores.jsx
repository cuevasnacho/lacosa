// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";

function mod(i, n) {  // positive modulo
  return ((i % n) + n) % n;
}

function Jugadores({ jugadores }) {
  let left,right,middle;
  const length = jugadores.length;

  if (length >= 3) {  // if players available
    const user_id = parseInt(window.sessionStorage.getItem('user_id'));
    const user_obj = jugadores.find(jugador => jugador.id === user_id);
    const user_pos = user_obj.posicion;
    let middleLeft = [];
    let middleRight = [];
    
    if (user_pos == 0)
      middleRight = jugadores.slice(2,length-1).reverse();

    else if (user_pos == length-1)
      middleRight = jugadores.slice(1,length-2).reverse();

    else{
      if (mod(user_pos-1, length) < user_pos)
        middleLeft = jugadores.slice(0,mod(user_pos-1, length)).reverse();
    
      if (mod(user_pos+2, length) > user_pos)
        middleRight = jugadores.slice(mod(user_pos+2, length)).reverse();
    }

    left = jugadores[mod(user_pos-1, length)];
    right = jugadores[mod(user_pos+1, length)];
    middle = middleLeft.concat(middleRight);
  }
  else {  // if no players in game
    left = {username: 'null', esTurno: false, eliminado: false};
    right = {username: 'null', esTurno: false, eliminado: false};
    middle = [{username: 'null', esTurno: false, eliminado: false}];
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
      </div>
      <div className={styles.jugadorRight} data-testid="right">
        <Jugador username={right.username} esTurno={right.esTurno} eliminado={right.eliminado}/>
      </div>
    </>
  );
}

export default Jugadores;
