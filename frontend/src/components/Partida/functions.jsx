import { httpRequest } from "../../services/HttpService";

function sortPlayers(jugadores) {
    const sortedPlayers = jugadores.sort((a,b) => a.posicion - b.posicion);
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

function mod(i, n) {  // positive modulo
  return ((i % n) + n) % n;
}

function arrangePlayers(jugadoresDesordenados) {
  const jugadores = sortPlayers(jugadoresDesordenados);
  console.log(jugadores);
  let left,right,middle,player;
  const length = jugadores.length;

  if (length >= 3) {  // if players available
    const user_id = parseInt(window.sessionStorage.getItem('user_id'));
    const user_obj = jugadores.find(jugador => jugador.id === user_id);
    const user_pos = user_obj.posicion;
    let middleLeft = [];
    let middleRight = [];
    
    if (user_pos == 0)
      middleRight = jugadores.slice(2,length-1).reverse();

    else if (user_pos == length-1)
      middleRight = jugadores.slice(1,length-2).reverse();

    else{
      if (mod(user_pos-1, length) < user_pos)
        middleLeft = jugadores.slice(0,mod(user_pos-1, length)).reverse();
    
      if (mod(user_pos+2, length) > user_pos)
        middleRight = jugadores.slice(mod(user_pos+2, length)).reverse();
    }

    left = [jugadores[mod(user_pos-1, length)]];
    right = [jugadores[mod(user_pos+1, length)]];
    middle = middleLeft.concat(middleRight);
    player = [jugadores[user_pos]];
  }
  else {  // if no players in game
    const arrangedPlayers = [
      {username: 'null', esTurno: false, eliminado: false},
      {username: 'null', esTurno: false, eliminado: false},
      {username: 'null', esTurno: false, eliminado: false},
      {username: 'null', esTurno: false, eliminado: false}];
    return arrangedPlayers;
  }
  return left.concat(middle, right, player);
}

export { nextTurn, arrangePlayers };
