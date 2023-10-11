import Partida from './Partida.jsx';

const InfoPartida = function () {
  const user_id = parseInt(window.sessionStorage.getItem('user_id'));
  const ws = new WebSocket(`ws://localhost:8000/ws/${user_id}`);

  return (
    <Partida ws={ws} />
  );
};

export default InfoPartida;