import {v4 as uuid} from 'uuid';
import TablaFila from './TablaFila';
import { useState,useEffect } from 'react'
import { helpHttp } from '../../helpers/helpHTTP';
import videobg from "../../assets/background-video.mp4"
import "./UnirsePartida.css"
import "./EstiloBoton.css"


function UnirsePartida(idJugador) {
     const [partidas, setPartidas] = useState([])
     const [verfERR, setVerfERR] = useState(false)
     const [mostrarTabla,setMostrar]=useState(false)   
     let api = helpHttp(),
     endpoit = "http://localhost:3000/Partidas"
     idJugador="jugador"
     useEffect(() => {
        api.get(endpoit).then((res)=>{
            if(!res.err){
                setPartidas(res)
            }else{
                setVerfERR(true)
            }
        })      
     }, [])

     setInterval(() => {
        setMostrar(true)
     }, 1100);
  return (
 
    <div>
        <video className='videobg' src={videobg} autoPlay loop muted />
        {(mostrarTabla) &&
        <div className='contenedor-tabla'>
            <h4> {idJugador}</h4>
            <h3 className='titulo-tabla'>Lista de Partidas</h3>
                <div className='tabla-unirsePartida'>
                    <table>
                        <thead>
                            <tr>
                                <th></th>
                                <th>Nombre de Partida</th>
                                <th>Host</th>
                                <th>CantJug</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {(verfERR)?(<tr><td colSpan="3">Hubo un Error </td></tr>):
                            (partidas.length > 0)?(partidas.map((elem,index=uuid())=>
                                <TablaFila 
                                    key={index} elem={elem} idJugador={idJugador}
                                ></TablaFila>)):
                                (<tr><td colSpan="3">No hay partidas disponibles</td></tr>)
                            } 
                        </tbody>
                    </table> 
                </div>
            <button className="boton-crear">Crear Partida</button>
        </div>             
        }
    </div>
  )
}
export default UnirsePartida
