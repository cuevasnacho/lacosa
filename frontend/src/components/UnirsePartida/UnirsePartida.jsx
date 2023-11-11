import {v4 as uuid} from 'uuid';
import TablaFila from './TablaFila';
import { useState,useEffect } from 'react'
import { httpRequest } from '../../services/HttpService.js'
import videobg from "../../media/videobg.mp4"
import "./UnirsePartida.css"
import "./EstiloBoton.css"
import { Link } from 'react-router-dom'

function UnirsePartida() {
    const [partidas, setPartidas] = useState([])
    
    /* No usar JSON.parse */
    let username = window.sessionStorage.getItem('username');
    console.log(username)
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
 
    <div className='page'>
        <video className='videobg' src={videobg} autoPlay loop muted />
        <h4>{username}</h4>
        <div className='contenedor-tabla'>
            <h3 className='titulo-tabla'>Lista de Partidas</h3>
                <div className='tabla-unirsePartida'>
                    <table>
                        <thead>
                            <tr>
                                <th className="columna-publica"></th>
                                <th className="columna-nombre-lobby">Nombre de Partida</th>
                                <th className="columna-nombre-host">Host</th>
                                <th className="columna-cantidad">CantJug</th>
                                <th className="columna-unirse-lobby"></th>
                            </tr>
                        </thead>
                        <tbody> 
                            {(partidas.length > 0)?(partidas.map((elem,index=uuid())=>
                                <TablaFila 
                                    key={index} elem={elem}
                                ></TablaFila>)):
                            (<tr>
                                <td colSpan={4}/>
                                <td>No hay partidas disponibles</td>
                            </tr>)
                            }
                        </tbody>
                    </table> 
                </div>
            <Link to={"/crear"} className='boton-crear'>Nueva Partida</Link>
        </div>             
    </div>
  )
}
export default UnirsePartida

