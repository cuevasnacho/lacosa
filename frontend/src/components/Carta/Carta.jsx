import React from "react"
import styles from "./Carta.module.css"

function Carta({carta}) {
    
    return (
        <div className={styles.carta}>
            <button type="button" onClick={descartar}>Descartar</button>
            <button type="button" onClick={jugarCarta}>Jugar</button>
            <img src={carta} width={180}/>
        </div>
    );
}

export default Carta;