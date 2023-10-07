import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';

function Carta({ carta, esTurno }) {
    const [isHover, setIsHover] = useState(false);

    function jugarCarta() {
        alert('Jugue la carta');
    }

    function descartarCarta() {
        alert('Descarte la carta');
    }

    const cartaState = esTurno ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && esTurno && (
                <div className={styles.botones}>
                    <button className={styles.boton} onClick={jugarCarta}>Jugar</button>
                    <button className={styles.boton} onClick={descartarCarta}>Descartar</button>
                </div>
            )}
        </div>
    );
}

export default Carta;