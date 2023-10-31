import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import  JugarCarta  from './JugarCarta.jsx';
import {useSelector, useDispatch} from 'react-redux';
import { getTurno } from "../../slices/turnoSlice";
import { descartarCarta } from './DescartarCarta.jsx';
import { setMano } from "../../slices/manoJugadorSlice";


function Carta({ carta, esTurno , actualizar, mano, socket, jugadores}) {
    const [isHover, setIsHover] = useState(false);

    const turno = useSelector(getTurno);
    const cartaState = turno ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;
    const dispatch = useDispatch();

   function handleDescartar() {
        dispatch(setMano(descartarCarta(carta, socket)));
    }

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img alt={carta.cartaNombre} src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && turno && carta.cartaNombre != 'lacosa' &&(
                <div className={styles.botones}>
                    <JugarCarta carta={carta} 
                        socket={socket} />
                    <button className={styles.boton} onClick={() => 
                        handleDescartar()}>Descartar</button>
                </div>
            )}
        </div>
    );
}

export default Carta;