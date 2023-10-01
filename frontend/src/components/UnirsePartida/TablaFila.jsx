import { httpRequest } from '../../services/HttpService.js'
import "./EstiloBoton.css"
import lock from "../../assets/lock-icon.svg"
import publica from "../../assets/public-icon.svg"
import { useState } from 'react'


export default function TablaFila(elem) {
  const {idPartida,nombrePartida,host,cantjug,privada}=elem.elem
  const [partidas,setPartidas]=useState([])
    
    const unirPartida = async () => {
        let {user_id} =JSON.parse(window.sessionStorage.getItem("logged"))
        const datosPartida = {
            user_id,
            idPartida,
        }
        try {
          const data = await httpRequest({
            method: 'POST',
            service: 'unirse',
            payload: datosPartida
          });
          setPartidas([...partidas, data]);
          //window.location=`/lobby`
        } catch (error) {
          console.log(error);
        }
      };
    
    
        
  return (
    <tr>
        {(privada)?<><td><img src={publica}></img></td></>:<><td><img src={lock}></img></td></>}
        <td>{nombrePartida}</td>
        <td>{host}</td>
        <td>{cantjug}</td>
        <td><button className="boton-unirse" onClick={()=>unirPartida()}>Unirse</button></td>
    </tr>
  )
}