from pony.orm import db_session, ObjectNotFound
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api.player.steal_card import get_match
from typing import List
from db.database import Player, Match
from pony.orm import db_session, commit
import json 
from definitions import player_roles

router = APIRouter()

class player_response(BaseModel):
    username  : str
    id : int  
    esTurno   : bool 
    posicion  : int
    eliminado : bool
    puerta_izq : bool
    puerta_der : bool
    cuarentena : bool

class player_response_sol(BaseModel):
    username  : str
    id : int  
    esTurno   : bool 
    posicion  : int
    eliminado : bool
    puerta_izq : bool
    puerta_der : bool
    cuarentena : bool
    infected : bool


class status_response(BaseModel):
    jugador : player_response_sol
    jugadores :  List[player_response]

@db_session
def generate_status_response(match_id,id_player):
    players = Player.select(lambda player : player.player_current_match_id.match_id == match_id)
    players_data = []

    match = Match.select(lambda match : match.match_id == match_id).first()
    player_turn = match.match_currentP

    for player in players:

        if player.player_id == id_player:
            response = player_response_sol(username= player.player_name,
                                   id = player.player_id,
                                   esTurno = (player_turn == player.player_id),
                                   posicion= player.player_position,
                                   eliminado = player.player_dead,
                                   puerta_izq = player.player_exchangeL,
                                   puerta_der = player.player_exchangeR,
                                   cuarentena = player.player_quarentine_count > 0,
                                   infected = player.player_role == player_roles.INFECTED.value)
            player_view = response.dict()

        response = player_response(username= player.player_name,
                                   id = player.player_id,
                                   esTurno = (player_turn == player.player_id),
                                   posicion= player.player_position,
                                   eliminado = player.player_dead,
                                   puerta_izq = player.player_exchangeL,
                                   puerta_der = player.player_exchangeR,
                                   cuarentena = player.player_quarentine_count > 0,
                                   infected = player.player_role == player_roles.INFECTED.value)
            
        players_data.append(response)
    
    full_response = {'jugador' : player_view, 'jugadores' : [obj.dict() for obj in players_data]}

    return full_response

@router.get("/partida/status/{match_id}/{player_id}")
async def get_status(match_id: int, player_id : int):
    try:
        content = generate_status_response(match_id,player_id)
        return JSONResponse(content = content, status_code = 200) 

    except ObjectNotFound as e:
        content = str(e)
        return JSONResponse(content=content, status_code=404)

    except Exception as e:
        print(f"Error al acceder a los datos: {e}")
        content = f"Error al acceder a los datos de la partida {match_id}"
        return JSONResponse(content = content, status_code = 410) #comportamiento inesperado