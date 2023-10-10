import React from "react"
import styles from "./Carta.module.css"

function Carta({ carta, isSelected, onSelect }) {
    
    return (
        <div className={isSelected ? styles.selected : styles.notSelected} onClick={handleClick}>
            <img src={carta} width={130}/>
        </div>
    );
}

export default Carta;