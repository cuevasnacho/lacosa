import React from "react"
import styles from "./Carta.module.css"

function Carta({carta}) {
    
    return (
        <div className={styles.carta}>
            <img src={carta} width={130}/>
        </div>
    );
}

export default Carta;