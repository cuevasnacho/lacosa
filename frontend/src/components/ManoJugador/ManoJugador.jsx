import React, { useState } from 'react';
import Carta from '../Carta/Carta.jsx';
import style from './ManoJugador.module.css';
import CustomButton from '../Boton/CustomButton';

function ManoJugador({ cartas, esTurno }) {
  const [cartasMano, setCartasMano] = useState(cartas);

  function actualizarMano(nuevaMano) {
    setCartasMano(nuevaMano);
  }

  return (
    <div className={style.ManoJugador}>
      {cartasMano.map((carta, index) => (
        <div
          key={index}
          style={{ position: 'relative' }}
        >
          <Carta carta={carta} esTurno={esTurno} actualizar={actualizarMano} mano={cartasMano} />
        </div>
      ))}
    </div>
  );
}

export default ManoJugador;
