import React, { useState } from 'react';
import Carta from '../Carta/Carta.jsx';
import style from './ManoJugador.module.css';
import CustomButton from '../Boton/CustomButton';

function ManoJugador({ cartas }) {
  const [cartaHover, setCartaHover] = useState(null);
  const [cartasMano, setCartasMano] = useState(cartas);
  
  const handleMouseEnter = (nombreCarta) => {
    setCartaHover(nombreCarta);
  };

  const handleMouseLeave = () => {
    setCartaHover(null);
  };

  function JugarCarta() {
    alert('Jugaste la Carta');
  }

  function DescartarCarta() {
    alert('Descartaste la Carta');
  }

  return (
    <div className={style.ManoJugador}>
      {cartas.map((carta, index) => (
        <div
          key={index}
          style={{ position: 'relative' }}
          onMouseEnter={() => handleMouseEnter(carta.nombre)}
          onMouseLeave={handleMouseLeave}
        >
          <Carta carta={carta} />

          {cartaHover === carta.nombre && (
            <div style={{ position: 'absolute', top: 0, left: 0 }}>
              <CustomButton label="Jugar" onClick={JugarCarta} />
              <CustomButton label="Descartar" onClick={DescartarCarta(cartas, nombreCarta)} />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default ManoJugador;
