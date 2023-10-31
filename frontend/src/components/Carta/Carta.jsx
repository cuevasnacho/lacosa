import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import { descartarCarta } from './DescartarCarta.jsx';
import  JugarCarta  from './JugarCarta.jsx';
import Stages from "../Partida/Stages.jsx";

function Carta({ carta, stage, actualizar, mano, socket, jugadores}) {
    const [isHover, setIsHover] = useState(false);
    
    const cartaState = (stage == Stages[jugar_carta]) ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img alt={carta.cartaNombre} src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && 
            (stage == Stages[jugar_carta] && carta.cartaNombre != 'lacosa') && (
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
            (stage == Stages[forzar] && carta.tipo) && (
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