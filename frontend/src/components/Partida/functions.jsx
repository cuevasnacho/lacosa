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

async function playCard(carta, target, socket) {
  const player_id = JSON.parse(sessionStorage.getItem('user_id'));
  const username = window.sessionStorage.getItem('username');
  
  let headers = { Accept: '*/*' };
  const response = await httpRequest({
    headers : headers,
    method: 'PUT',
    service: `carta/jugar/${player_id}/${carta.id}/${target.target_id}`,
  });
  
  // response[0] es el jugador que jugo la carta
  // response[1] es el jugador al que le juegan la carta
  const cartas_mostrar = response[0].card_name;
  const mensaje = JSON.stringify({
    action: 'play_card',
    data: {
      card: carta.cartaNombre,
      player: username, 
      target: target.target_username,
      tipo: carta.tipo,
    }});

  const mensaje_cartas = JSON.stringify({
    action: 'show_cards',
    data: {
      card: carta.cartaNombre,
      mostrar: cartas_mostrar
    }
  });

  socket.send(mensaje);
  socket.send(mensaje_cartas);
  
  return;
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

export { nextTurn, arrangePlayers, playCard };
