from pydantic import *
from api.player.player import get_jugador
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pony.orm import db_session
from db.database import Lobby,Player
from api.websocket import ConnectionManager
from definitions import player_roles

router = APIRouter()

manager = ConnectionManager()

show_cards_to_all = ['whiskey']

@router.get("/partida/resultado/{match_id}")
def match_result(match_id : int):
    players = Player.select(lambda player : player.player_current_match_id.match_id == match_id)
    lacosa = Player.select(lambda player : player.player_current_match_id.match_id == match_id 
                           and player.player_role == player_roles.player_roles.THE_THING.value).first()
    winners = []
    (winners.append(lacosa.player_name)) if not lacosa.player_dead else winners
   
    for player in players:
        if lacosa.player_dead:
            #si la cosa esta muerta -> ganan los humanos y devuevlo a los vivos
            if player.player_role == player_roles.player_roles.HUMAN.value:
                winners.append(player.player_name)
        else:
            #si la cosa esta viva -> gana la cosa y los infectados
            if player.player_role == player_roles.player_roles.INFECTED.value:
                winners.append(player.player_name)
            winner_team
    winner_team = "Humanos" if lacosa.player_dead else ("La cosa" if len(winners) == 1 else "La cosa e infectados")
    response = {'jugadores' : winners, 'ganadores' : winner_team}