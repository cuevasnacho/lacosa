
from db import database
from pony.orm import db_session, ObjectNotFound
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from definitions import match_status
from pydantic import BaseModel
from api.player.steal_card import get_match
from typing import List

router = APIRouter()

class player_response(BaseModel):
    username  : str
    id : int  
    esTurno   : bool 
    posicion  : int
    eliminado : bool

class status_response(BaseModel):
    jugador : player_response
    jugadores :  List[player_response]

@db_session
def generate_status_response(match_id):
    match = get_match(match_id)        
    players_data = [] 

    players = list(match.match_players)

    if len(players) == 0:
        raise ObjectNotFound("No hay jugadores asociados a la partida")

    for player in players :
        enTurno = match.match_currentP.player_id = player.player_id
        player_data = player_response(username = player.player_name,
                                      id = player.player_id,
                                      esTurno= enTurno,
                                      posicion = player.player_position,
                                      eliminado = player.player_dead)
        if enTurno:
            player_in_turn = player_data
        else:
            players_data.append(player_data)

    ended = match.match_status == match_status.FINISHED.value

    full_status = status_response(jugador = player_in_turn,
                                  jugadores = player_data)

    return full_status

@router.get("/partida/status/{match_id}")
async def get_status(match_id: int) -> status_response:
    try:
        full_status = generate_status_response(match_id)
            
        return full_status

    except ObjectNotFound as e:
        content = str(e)
        return JSONResponse(content=content, status_code=404)

    except Exception as e:
        print(f"Error al acceder a los datos: {e}")
        content = f"Error al acceder a los datos de la partida {match_id}"
        return JSONResponse(content = content, status_code = 410) #comportamiento inesperado
