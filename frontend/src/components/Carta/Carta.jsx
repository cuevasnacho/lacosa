import React from "react";
import styles from "./Carta.module.css";

/*
    El tamaño por defecto de las cartas en el mazo es 125 de ancho.
    Cuando se roba una carta el tamaño es de 250.
*/

function Carta({carta}) {
    return (
        <div className={styles.carta}>
            <img src={carta.imagen} width={carta.tamaño}  />
        </div>
    );
}

export default Carta;