import { helpHttp } from '../../helpers/helpHTTP';
import "./EstiloBoton.css"
import lock from "../../assets/lock-icon.svg"
import publica from "../../assets/public-icon.svg"

export default function TablaFila(elem) {
  const {idPartida,nombrePartida,host,cantjug,privada}=elem.elem
  let api = helpHttp(),
  endpoit = "http://localhost:3000/Partids",
  idJugador=window.localStorage.getItem("idJugador")

  const unirPartida = () =>{
    const datosPartida = {
        idJugador,
        idPartida,
    }
    const options = {
        method:"POST",
        body:datosPartida,
        headers:{"content-type":"application/json"}
    }
    api.post(endpoit,options).then((res)=>{
        if(!res.err){
          //window.location="ruta del lobby"   
        }else{
          console.alert(`No se pudo unirse a la partida ${res.err}`)
        }
    })
 }
  return (
    <tr>
        {(privada)?<><td><img src={publica}></img></td></>:<><td><img src={lock}></img></td></>}
        <td>{nombrePartida}</td>
        <td>{host}</td>
        <td>{cantjug}</td>
        <td><button className="boton-unirse"  onClick={()=>unirPartida()}>Unirse</button></td>
    </tr>
  )
}