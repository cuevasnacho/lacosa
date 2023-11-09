import React from "react";
import { useState } from 'react';
import { httpRequest } from "../../services/HttpService";
import { descartarCarta } from './DescartarCarta.jsx';
import { getHand } from "../Partida/functions.jsx";
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import  JugarCarta  from './JugarCarta.jsx';

function Carta({ carta, stage, data, actualizar, mano, socket, jugadores}) {
    const [isHover, setIsHover] = useState(false);
    
    const cartaState = (stage == 3) ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;
    
    async function resIntercambiar() {
        const player_id = JSON.parse(window.sessionStorage.getItem('user_id'));
    
        const response = await httpRequest({
            method: 'GET',
            service: `intercambio/valido/${player_id}/${data.oponent_id}/${carta.id}/${data.motive}`,
        });
        if (response) {
            console.log(data);
            await httpRequest({
                method: 'PUT',
                service: `intercambio/cartas/${player_id}/${carta.id}/${data.oponent_id}/${data.card_id}/${data.motive}`,
            });
            getHand(actualizar);
        }
    }

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img alt={carta.cartaNombre} src={Diccionario[carta.cartaNombre]} width={130}/>

            { (isHover && (stage == 3 || stage == 5)) && (
                <div className={styles.botones}>
                    <JugarCarta carta={carta} 
                        socket={socket} 
                        jugadores={jugadores} 
                        actualizar={actualizar} 
                        mano={mano}
                        stage={stage}
                        data={data}/>
                    <button className={styles.boton} onClick={() => 
                        descartarCarta(actualizar, mano, carta, socket)}>Descartar</button>
                </div>
            )}

            { (isHover && stage == 2 && carta.tipo) && (
                <div className={styles.botones}>
                    <JugarCarta carta={carta} 
                        socket={socket} 
                        jugadores={jugadores} 
                        actualizar={actualizar} 
                        mano={mano}
                        stage={stage}
                        data={data}/>
                </div>
            )}
            {(isHover && stage == 7) && (
                <button type='button' className={styles.botonIntercambio} onClick={() => resIntercambiar()}>
                Intercambiar
                </button>
            )}
        </div>
    );
}

export default Carta;