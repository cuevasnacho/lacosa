import Carta from '../Carta/Carta.jsx';
import style from './ManoJugador.module.css';
import CustomButton from '../Boton/CustomButton';

function ManoJugador({ cartas, esTurno , actualizar, socket, jugadores}) {
  console.log(cartas);  
  return (
    <div className={style.ManoJugador}>
      {cartas.map((carta, index) => (
        <div
          key={index}
          style={{ position: 'relative' }}
          data-testid={carta.nombre}
        >
          <Carta  carta={carta} 
                  esTurno={esTurno} 
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
