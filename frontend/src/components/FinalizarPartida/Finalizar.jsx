import { Link } from "react-router-dom"
import  "./Finalizar.css"
import { useEffect,useState } from "react"
export default function Finalizar() {
    const [jugadores,setJugadores]=useState([])
    const [ganador,setGanador]=useState("")
    useEffect(() => {
        const getJugadores = async () => {
            let headers = {
                Accept: '*/*', 
            }
            try 
            {
              const data = await fetch("http://localhost:3000/jugadoresDB"),
                res=await data.json()
              console.log(res)
              setJugadores(res.jugadores);
              setGanador(res.ganador)
            } 
            catch (error) {
              console.log(error);
            }
          }
          getJugadores()
     }, [])
    
  return (
    <article className="modal">
        <div className='modal-container'>
        <h1 className="titulo-tabla">Victoria para los {ganador}</h1>
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
            </div>
            <Link className="boton-terror" to="/home">Volver Inicio</Link>
        </div>
    </article>
  )
}
