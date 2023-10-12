import { Link } from "react-router-dom"
import  "./Finalizar.css"
export default function Finalizar({jugadoresDB}) {
    const jugadores = jugadoresDB.jugadores
    const equipoGanador = jugadoresDB.ganador
  return (
    <article className="modal">
        <div className='modal-container'>
            <h1 className="titulo-tabla">Victoria para los {equipoGanador}</h1>
            <div className="container-tabla">      
                <div className='tabla-unirsePartida'>
                    <table>
                        <thead>
                            <tr>
                                <th>Nombre del Jugador</th>
                                <th>Equipo</th>
                            </tr>
                        </thead>
                        <tbody> 
                            {jugadores.length > 0 ?(
                                jugadores.map((jugadores,index=uuid()) => (
                                <tr key={index}>
                                    <td>{jugadores.nombre_jugador}</td>
                                    <td>{jugadores.equipo}</td>  
                                </tr>
                                )))
                                : (
                                <tr>
                                    <td colSpan={2}>No hay jugadores ganadores</td>
                                </tr>
                                )}
                        </tbody>
                    </table>
                </div> 
                <Link className="boton-terror" to="/home">Volver Inicio</Link>
            </div>
        </div>
    </article>
  )
}
