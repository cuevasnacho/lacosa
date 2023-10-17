import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import { descartarCarta } from './DescartarCarta.jsx';

function Carta({ carta, esTurno , actualizar, mano}) {
    const [isHover, setIsHover] = useState(false);

    function jugarCarta() {
        if(carta.cartaNombre === 'lacosa')
            alert(`No puedes jugar la carta ${carta.cartaNombre}`);
        else
        {
            alert(`Jugue la carta ${carta.id} ${carta.cartaNombre}`);
            descartarCarta(actualizar, mano);
        }
    }
    
    const cartaState = esTurno ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img alt={carta.cartaNombre} src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && esTurno && (
                <div className={styles.botones}>
                    <button className={styles.boton} onClick={jugarCarta}>Jugar</button>
                    <button className={styles.boton} onClick={() => descartarCarta(actualizar, mano, carta)}>Descartar</button>
                </div>
            )}
        </div>
    );
}

export default Carta;