import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';

function Carta({ carta }) {
    const [isHover, setIsHover] = useState(false);

    function jugarCarta() {
        alert('Jugue la carta');
    }

    function descartarCarta() {
        alert('Descarte la carta');
    }

    return (
        <div 
            className={styles.carta} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img src={Diccionario[carta]} width={130}/>
            { isHover && (
                <div className={styles.botones}>
                    <button className={styles.boton} onClick={jugarCarta}>Jugar</button>
                    <button className={styles.boton} onClick={descartarCarta}>Descartar</button>
                </div>
            )}
        </div>
    );
}

export default Carta;