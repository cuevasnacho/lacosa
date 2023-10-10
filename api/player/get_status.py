
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
    position : int
    isDead  : bool
    name    : str 

class status_response(BaseModel):
    players :  List[player_response]
    actual_turn : int
    finished : bool


@router.get("/partida/status/{match_id}")
async def get_status(match_id: int) -> status_response:
    with db_session:
        try:
            match = get_match(match_id)        
            players_data = [] 

            players = list(match.match_players)

            if len(players) == 0:
                raise ObjectNotFound("No hay jugadores asociados a la partida")

            for player in players :
                player_data = player_response(position = player.player_position,
                                            isDead = player.player_dead,
                                            name = player.player_name)
                players_data.append(player_data)

            ended = match.match_status == match_status.FINISHED.value

            full_status = status_response(players = players_data,
                                        actual_turn = match.match_currentP,
                                        finished = ended)
            
            return full_status

        except ObjectNotFound as e:
            content = str(e)
            return JSONResponse(content=content, status_code=404)

        except Exception as e:
            print(f"Error al acceder a los datos: {e}")
            content = f"Error al acceder a los datos de la partida {match_id}"
            return JSONResponse(content = content, status_code = 410) #comportamiento inesperado
