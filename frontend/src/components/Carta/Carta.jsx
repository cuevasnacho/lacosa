import React from "react"
import styles from "./Carta.module.css"
import back_alejate from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/back_alejate.png'
import back_panico from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/back_panico.png'

/*
    El width por defecto de las cartas en el mazo es 125 de ancho.
    Cuando se roba una carta el tamaño es de 250.

    Ejemplo de carta:
    const carta_analisis = {
        id: 1,
        template: "string",
        tipo: 0,
        ubicacion: "mazo",
        imagen: analisis,
    };
*/

// Definir una constante diccionario con los valores anteriores
const ubicacion = {
    mano: 125,
    levantada: 250,
    mazo: 225
};

function Carta({carta}) {
    var width = ubicacion[carta.ubicacion];

    if (carta.ubicacion === 'mazo') 
        carta.imagen = carta.tipo === 0 ? back_alejate : back_panico;

    return (
        <div className={styles.carta}>
            <img src={carta.imagen} width={width}/>
        </div>
    );
}

export default Carta;