import {v4 as uuid} from 'uuid';
import TablaFila from './TablaFila';
import { useState,useEffect } from 'react'
import { httpRequest } from '../../services/HttpService.js'
import videobg from "../../media/background-video.mp4"
import "./UnirsePartida.css"
import "./EstiloBoton.css"
import { Link } from 'react-router-dom'

function UnirsePartida() {
    const [partidas, setPartidas] = useState([])
    
    /* No usar JSON.parse */
    let {username} = window.sessionStorage.getItem('username');

     useEffect(() => {
        const fetchpPartidas = async () => {
            let headers = {
                Accept: '*/*', 
            }
            try 
            {
              const data = await httpRequest({ method: 'GET',headers:headers, service: 'partidas/listar' });
              console.log(data);
              setPartidas(data);
            } 
            catch (error) {
              console.log(error);
            }
          }
          
            fetchpPartidas()
     }, [])
  return (
 
    <div>
        <video className='videobg' src={videobg} autoPlay loop muted />
        <div className='contenedor-tabla'>
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
            <Link to={"/crear"} className='boton-crear'>Crear Partida</Link>
        </div>             
    </div>
  )
}
export default UnirsePartida

