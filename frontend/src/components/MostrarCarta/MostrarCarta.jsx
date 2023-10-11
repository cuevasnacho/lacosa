/** Hacer animación de jugar carta. 

No se puede mostrar todavía a todos los jugadores. (websockets)

Mostrar la carta un poco mas grande que las demas carta a todos los jugadores y que aparezca en el centro de la pantalla por 2 segundos.
.*/
import { useState } from "react";
import Diccionario from "../Carta/Diccionario"
import styles from "./MostrarCarta.module.css"
export default function MostrarCarta({nombreCarta}) {
    const [verf,setVerf] = useState(true)
    setInterval(() => {
        setVerf(false)
    }, 2500);
  return (
    <>
    {verf && 
    <div>
        <img className={styles.carta} src={Diccionario[nombreCarta]}></img>
    </div>
    }   
    </>
  )
}
