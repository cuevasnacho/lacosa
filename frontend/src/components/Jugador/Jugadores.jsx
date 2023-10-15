// Jugadores.jsx
import React from 'react';
import Jugador from "./Jugador";
import styles from "./Jugadores.module.css";

function mod(i, n) {
  return ((i % n) + n) % n;
}

function Jugadores({ jugadores }) {
  
  let left,right,middle;
  if (jugadores.length >= 3){
    const user_id = parseInt(window.sessionStorage.getItem('user_id'));
    console.log(jugadores);
    console.log(user_id);
    const user_obj = jugadores.find(jugador => jugador.id === user_id);
    const user_pos = user_obj.posicion;
    let middleLeft = [];
    let middleRight = [];
    
    if (user_pos == 0)
      middleRight = jugadores.slice(2,jugadores.length-1).reverse();
    else if (user_pos == jugadores.length-1)
      middleRight = jugadores.slice(1,jugadores.length-2).reverse();
    else{
      if (mod(user_pos-1, jugadores.length) < user_pos)
        middleLeft = jugadores.slice(0,mod(user_pos-1, jugadores.length)).reverse();
    
      if (mod(user_pos+2, jugadores.length) > user_pos)
        middleRight = jugadores.slice(mod(user_pos+2, jugadores.length)).reverse();
    }

    left = jugadores[mod(user_pos-1, jugadores.length)];
    right = jugadores[mod(user_pos+1, jugadores.length)];
    middle = middleLeft.concat(middleRight);
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
