from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit 
from definitions import player_roles

from db.database import Player as db_player

router = APIRouter()



class Player(BaseModel):

    player_name: str
    player_ingame: Optional[bool] = False
    player_role: Optional[player_roles] = None 
    player_exchangeL: Optional[bool] = True
    player_exchangeR: Optional[bool] = True
    player_position: Optional[int] = None
    player_dead: Optional[bool] = False
    player_isHost: Optional[bool] = True # ojo que por defecto es host


class PlayerOut(BaseModel):
    player_id : int
    player_name : str

@router.post("/player", response_model=PlayerOut)
async def crear_jugador(new_player: Player, name : str):
    if len(name) > 20: #FALTAN VALIDAR LOS CAMPOS DE PLAYER
            message = "Nombe demasiado largo"
            status_code = 406 # no acceptable
            return JSONResponse(content=message, status_code=status_code)
    with db_session:
        new_player = db_player(player_name= name, player_ingame = False, player_isHost=False)
        commit()
    return new_player



        
