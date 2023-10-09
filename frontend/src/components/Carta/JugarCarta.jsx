import styles from "./JugarCarta.module.css"

export default function JugarCarta(carta,ws) {
    const jugarCarta = ()=>{
        const data = JSON.stringify({ action: 'jugar_carta', data: carta.id });
        ws.send(data);
    }
  return (
    <button onClick={jugarCarta} className= {styles.terror}>Jugar</button>
  )
}