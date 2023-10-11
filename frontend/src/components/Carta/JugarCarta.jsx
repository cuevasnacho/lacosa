import styles from "./JugarCarta.module.css"

export default function JugarCarta(carta,target,ws) {
    const jugarCarta = ()=>{
      const datos ={
        action:'jugar_carta',
        data:{
          carta_id:carta.id,
          target_id:target
        } 
      }  
      const data = JSON.stringify(datos);
      ws.send(data);
    }
  return (
    <button onClick={jugarCarta} className= {styles.terror}>Jugar</button>
  )
}