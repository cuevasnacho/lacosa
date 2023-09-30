import {v4 as uuid} from 'uuid';
import TablaFila from './TablaFila';
import { useState,useEffect } from 'react'
import {useParams} from "react-router"
import { httpRequest } from '../../services/HttpService.js'
import videobg from "../../media/background-video.mp4"
import "./UnirsePartida.css"
import "./EstiloBoton.css"


function UnirsePartida() {
    const {idJugador,nombreJug} = useParams()
    const [partidas, setPartidas] = useState([])
    const [mostrarTabla,setMostrar]=useState(false)   

     useEffect(() => {
        const fetchpPartidas = async () => {
            try {
              const data = await httpRequest({ method: 'GET', service: 'Partidas' });
              setPartidas(data);
            } catch (error) {
              console.log(error);
            }
          }
            window.localStorage.setItem("idJug",idJugador)
            window.localStorage.setItem("nomJug",nombreJug)
            fetchpPartidas()
     }, [])

     setInterval(() => {
        setMostrar(true)
     }, 1100);
  return (
 
    <div>
        <video className='videobg' src={videobg} autoPlay loop muted />
        {(mostrarTabla) &&
        <div className='contenedor-tabla'>
            <h4> {nombreJug}</h4>
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
                            
                            {(partidas.length > 0)?(partidas.map((elem,index=uuid())=>
                                <TablaFila 
                                    key={index} elem={elem}
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
