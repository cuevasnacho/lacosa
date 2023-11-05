import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import { descartarCarta } from './DescartarCarta.jsx';
import  JugarCarta  from './JugarCarta.jsx';

function Carta({ carta, stage, actualizar, mano, socket, jugadores}) {
    const [isHover, setIsHover] = useState(false);
    
    const cartaState = (stage == 3) ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img alt={carta.cartaNombre} src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && 
            (stage == 3 && carta.cartaNombre != 'lacosa') && (
                <div className={styles.botones}>
                    <JugarCarta carta={carta} 
                        socket={socket} 
                        jugadores={jugadores} 
                        funcionDescartar={actualizar} 
                        mano={mano}/>
                    <button className={styles.boton} onClick={() => 
                        descartarCarta(actualizar, mano, carta, socket)}>Descartar</button>
                </div>
            )}
            { isHover && 
            (stage == 2 && carta.tipo) && (
                <div className={styles.botones}>
                    <JugarCarta carta={carta} 
                        socket={socket} 
                        jugadores={jugadores} 
                        funcionDescartar={actualizar} 
                        mano={mano}/>
                </div>
            )}
        </div>
    );
}

export default Carta;