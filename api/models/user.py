from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException, APIRouter, Query, status
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit 
from definitions import player_roles

from db.database import Player as db_player

router = APIRouter()



class PlayerIn(BaseModel):
    player_name: str

class PlayerOut(BaseModel):
    player_id : int
    player_name : str


@db_session()
def get_jugador(player_id):
    try:
        player = db_player[player_id]
        return player
    except ObjectNotFound:
        message = "El jugador no existe"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)

@router.post("/players/", status_code=status.HTTP_201_CREATED)
async def Crear_Jugador(new_player: PlayerIn) -> PlayerOut:
    if len(player_name) > 20: 
        message = "Nombe demasiado largo"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    with db_session:
        new_player = db_player(player_name= player_name, player_ingame = False, player_isHost=True, player_role = None,
        player_position=None, player_exchangeL=True, player_exchangeR=True, player_dead = False)
        commit() #OJO QUE PLAYER POR DEFECTO ES HOST
        return PlayerOut(player_id=new_player.player_id, player_name=new_player.player_name)


@router.get("/players/{player_id}")
async def Buscar_Jugador(player_id : int):
    player =get_jugador(player_id)
    return{
    "player_name": player.player_name,
    "player_ingame": player.player_ingame,
    "player_role": player.player_role,
    "player_exchangeL": player.player_exchangeL,
    "player_exchangeR": player.player_exchangeR,
    "player_position": player.player_position,
    "player_dead": player.player_dead,
    "player_isHost": player.player_isHost
    }




        
