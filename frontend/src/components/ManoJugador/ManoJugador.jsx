import Carta from '../Carta/Carta.jsx';
import style from './ManoJugador.module.css';
import { getMano } from '../../slices/manoJugadorSlice.js';
import { useSelector } from 'react-redux';

function ManoJugador({ cartas, esTurno , actualizar, socket, jugadores}) {
  let mano = useSelector(getMano);
  return (
    <div className={style.ManoJugador}>
      {mano.map((carta, index) => (
        <div
          key={index}
          style={{ position: 'relative' }}
          data-testid="carta"
        >
          <Carta  carta={carta} 
                  esTurno={esTurno} 
                  actualizar={actualizar} 
                  mano={mano} 
                  socket={socket} 
                  jugadores={jugadores}/>
        </div>
      ))}
    </div>
  );
}

export default ManoJugador;
