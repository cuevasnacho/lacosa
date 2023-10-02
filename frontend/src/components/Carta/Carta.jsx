import React from "react"
import styles from "./Carta.module.css"
import back_alejate from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/back_alejate.png'
import back_panico from '/home/ignacio/lacosa/frontend/src/media/designs/cartas/back_panico.png'


function Carta({carta}) {
    
    return (
        <div className={styles.carta}>
            <img src={carta} width={180}/>
        </div>
    );
}

export default Carta;