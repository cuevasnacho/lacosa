from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import *
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit 
from pony.orm import Set, select
from definitions import match_status

from db.database import Lobby as db_lobby
from db.database import Match as db_match
from db.database import Player as db_player


router = APIRouter()


@router.post("/partida/{id_match}/next")
@db_session
async def next_player(id_match : str, id_player : int): #id del player que esta jugando ahora   
    match = db_match.get(lambda match : match.match_id == id_match) #busco el sentido de la ronda
    lobby = db_lobby.get(lambda lobby : lobby.lobby_id = id_match) #busco players con el lobby-match asociado
    match_direction = match.match_direction
    if match_direction == True: #gira a la derecha
        player_next = db_player.select(lambda player : player.player_lobby.lobby_id == id_match
                                 and player.player_id == id_player + 1)


        content = {"player_id" : player_next.player_id}
        return JSONResponse(content= json.loads(json.dumps(content)), status_code=200)
    else: #gira a la izquierda
         player_next = db_player.select(lambda player : player.player_lobby.lobby_id == id_match
                                 and player.player_id == id_player -1)


        content = {"player_id" : player_next.player_id}
        return JSONResponse(content= json.loads(json.dumps(content)), status_code=200)