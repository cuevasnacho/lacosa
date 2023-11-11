import { httpRequest } from '../../services/HttpService.js'
import "./EstiloBoton.css"
import lock from "../../assets/lock-icon.svg"
import publica from "../../assets/public-icon.svg"
import visibility_on from "../../assets/visibility_on.svg"
import visibility_off from "../../assets/visibility_off.svg"
import { useState } from 'react'

export default function TablaFila(elem) {
  const {lobby_id,lobby_name,host_name,is_private,number_of_players,max_players}=elem.elem;
  const [partidas,setPartidas] = useState([]);
  const [password, setPassword] = useState("");
  const [pass_visible, setPassVisibility] = useState(false);
  const [pass_type, setPassType] = useState("password");
  const [show_input, setInput] = useState(false);

  let cantjug=" "+ number_of_players + "/" + max_players ;

  function changePassVis() {
    if (pass_visible) setPassType("password");
    else setPassType("text");
    
    setPassVisibility(!pass_visible);
  }

  const unirPartida = async () => {
    if (show_input) {
    const user_id = window.sessionStorage.getItem('user_id');
    console.log(user_id);
    try {
        const data = await httpRequest({
          method: 'PUT',
          service: `lobbys/${lobby_id}/${user_id}/${password}`
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
    }
    else {
      setInput(true);
    }
    };     
  return (
    <tr>
        {(is_private)?
          <>
            <td className="columna-publica">
              <img className="public_image" src={lock}></img>
            </td></> :
          <>
            <td className="columna-publica">
              <img className="public_image" src={publica}></img>
            </td>
          </>
        }
        <td className="columna-nombre-lobby">{lobby_name}</td>
        <td className="columna-nombre-host">{host_name}</td>
        <td className="columna-cantidad">{cantjug}</td>
        <td className="columna-unirse-lobby">
          <div className="enter-lobby-field">
            { (is_private && show_input) && (
              <div className="password-field">
                { (pass_visible) ?
                  <img 
                    className="visibility" 
                    src={visibility_off} 
                    onClick={(changePassVis)} /> :
                  <img 
                    className="visibility" 
                    src={visibility_on}
                    onClick={(changePassVis)} />
                }
                <input 
                  type={pass_type}
                  required 
                  minLength='4' 
                  maxLength='20' 
                  onChange={(e) => setPassword(e.target.value)}
                  className="password-input"
                  autoComplete='off'
                  />
                  { (show_input) &&
                    <button 
                      type='button' 
                      className="boton-cerrar-input"
                      onClick={() => setInput(false)}>
                        X
                    </button>
                  }
              </div>
            )}
            <button className="boton-unirse" onClick={()=>unirPartida()}>Unirse</button>
          </div>
        </td>
    </tr>
  )
}
