import { useState } from 'react';

import Mesa from '../Mesa/Mesa.jsx';
import ManoJugador from '../ManoJugador/ManoJugador.jsx';

const Partida = function (socket) {
  const { ws } = socket;
  const user_id = JSON.parse(localStorage.getItem('user_id'));
  const username = JSON.parse(localStorage.getItem('username'));

  const [match_state, set_match_state] = useState([]);

  ws.onmessage = function (event) {
    const info = JSON.parse(event.data);
    switch (info.action) {
      case 'estado_jugadores':
        setEstado(info.data);
        return;

      default:
        return;
    }
  }

  return (
    <div className={styles.container}>
      <ManoJugador ws={ws} cartas={cartas} />
    </div>
  );
}

export default Partida;