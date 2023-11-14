from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit , ObjectNotFound
from pony.orm import Set, select
from definitions import match_status
from api.match.match_websocket import manager
from api.messages import start_next_turn

from db.database import Lobby as db_lobby
from db.database import Match as db_match
from db.database import Player as db_player


router = APIRouter()

class nextPlayer(BaseModel):
    player_next_id : int



def adjacent_players(cause_position,player_counter,target_position):
    left = (cause_position - 1) % player_counter == target_position 
    right = (cause_position + 1) % player_counter == target_position
    return left or right

@router.get("/partida/{id_match}/next")
async def next_player(id_match : int): #id del player que esta jugando ahora   

    with db_session:
        try:
            fetch_lobby = db_lobby[id_match]
        except ObjectNotFound:
            return JSONResponse(content="el lobby no existe", status_code=404)
        
        fetch_match = fetch_lobby.lobby_match

        player_counter = fetch_lobby.lobby_pcount
        match_direction = fetch_match.match_direction
        current_player = fetch_match.match_currentP

        current_player_obj = db_player[current_player]
        current_player_pos = current_player_obj.player_position

        if match_direction:
            next_player_pos = (current_player_pos + 1) % player_counter
            next_player_obj = db_player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == id_match)
            while next_player_obj.player_dead == True:
                next_player_pos = (next_player_pos + 1) % player_counter
                next_player_obj = db_player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == id_match)
            next_player_id = next_player_obj.player_id
            fetch_match.match_currentP = next_player_id
        else:
            next_player_pos = (current_player_pos - 1) % player_counter
            next_player_obj = db_player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == id_match)
            while next_player_obj.player_dead == True:
                next_player_pos = (next_player_pos - 1) % player_counter
                next_player_obj = db_player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == id_match)
            next_player_id = next_player_obj.player_id
            fetch_match.match_currentP = next_player_id
                            
    await start_next_turn(id_match,next_player_id)
    return JSONResponse(content={"next_player" : next_player_id}, status_code=200)