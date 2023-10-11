import { httpRequest } from '../../services/HttpService.js'
import "./EstiloBoton.css"
import lock from "../../assets/lock-icon.svg"
import publica from "../../assets/public-icon.svg"
import { useState } from 'react'


export default function TablaFila(elem) {
  const {lobby_id,lobby_name,host_name,is_private,number_of_players,max_players}=elem.elem
  const [partidas,setPartidas] = useState([])
  
  let cantjug=" "+ number_of_players + "/" + max_players ;

  const unirPartida = async () => {
    const user_id = window.sessionStorage.getItem('user_id');
    console.log(user_id);
    try {
        const data = await httpRequest({
          method: 'PUT',
          service: `lobbys/${lobby_id}/${user_id}`
      });
        setPartidas([...partidas, data]);
        
        window.sessionStorage.setItem('Host',false);
        window.sessionStorage.setItem('Partida', JSON.stringify({
          lobby_min: 0,
          lobby_max: max_players,
        }));
        
        window.location=`/lobby/${lobby_id}`
      } catch (error) {
        console.log(error);
        
        }
    };     
  return (
    <tr>
        {(is_private)?<><td><img src={publica}></img></td></>:<><td><img src={lock}></img></td></>}
        <td>{lobby_name}</td>
        <td>{host_name}</td>
        <td>{cantjug}</td>
        <td><button className="boton-unirse" onClick={()=>unirPartida()}>Unirse</button></td>
    </tr>
  )
}