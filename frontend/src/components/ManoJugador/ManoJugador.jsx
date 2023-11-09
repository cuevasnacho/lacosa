import Carta from '../Carta/Carta.jsx';
import style from './ManoJugador.module.css';

function ManoJugador({ cartas, stage , data, actualizar, socket, jugadores}) {
  return (
    <div className={style.ManoJugador}>
      {cartas.map((carta, index) => (
        <div
          key={index}
          style={{ position: 'relative' }}
          data-testid="carta"
        >
          <Carta  carta={carta} 
                  stage={stage} 
                  data={data}
                  actualizar={actualizar} 
                  mano={cartas} 
                  socket={socket} 
                  jugadores={jugadores}/>
        </div>
      ))}
    </div>
  );
}

export default ManoJugador;
