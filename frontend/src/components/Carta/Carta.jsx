import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import { descartarCarta } from './DescartarCarta.jsx';
import  JugarCarta  from './JugarCarta.jsx';

function Carta({ carta, esTurno , actualizar, mano, socket, jugadores}) {
    const [isHover, setIsHover] = useState(false);
    
    const cartaState = esTurno ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img alt={carta.cartaNombre} src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && esTurno && (
                <div className={styles.botones}>
                    <JugarCarta carta={carta} socket={socket} jugadores={jugadores}/>
                    <button className={styles.boton} onClick={() => descartarCarta(actualizar, mano, carta, socket)}>Descartar</button>
                </div>
            )}
        </div>
    );
}

export default Carta;