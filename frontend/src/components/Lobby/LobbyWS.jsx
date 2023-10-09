import { useParams } from 'react-router-dom';
import Lobby from './Lobby.jsx';

const LobbyWS = function () {
    const {idLobby} = useParams();
    const ws = new WebSocket(`ws://localhost:8000/ws/lobbys/${idLobby}/refrescar`);

  return (
    <Lobby ws={ws} />
  );
};

export default LobbyWS;