import { httpRequest } from "../../services/HttpService";

function sortPlayers(jugadores) {
    const sortedPlayers = jugadores.sort((a,b) => a.position - b.position);
    return sortedPlayers;
}

async function nextTurn(id_match, socket, actual_player_username) {
  await httpRequest({
    method: 'GET',
    service: `partida/${id_match}/next`,
  });

  const mensaje = JSON.stringify({action: 'next_turn', data: actual_player_username});
  socket.send(mensaje);
}



export { sortPlayers, nextTurn };
